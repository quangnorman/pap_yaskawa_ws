"""YOLO box detection on RealSense color frames with cached aligned depth."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import rclpy
from cv_bridge import CvBridge, CvBridgeError
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import Header

from gp7_vision_pipeline.depth_utils import bbox_clip_to_image, median_depth_meters
from gp7_vision_pipeline.detection_visualizer import draw_box_detection, draw_no_detection
from gp7_vision_pipeline.msg import BoxDetection


def _try_import_yolo():
    try:
        from ultralytics import YOLO  # type: ignore

        return YOLO
    except ImportError as exc:
        raise RuntimeError(
            "ultralytics is required. Install with: pip install ultralytics"
        ) from exc


class YoloBoxDetectorNode(Node):
    """Color-driven YOLO + latest cached depth for distance; optional CameraInfo."""

    def __init__(self) -> None:
        super().__init__("yolo_box_detector_node")
        self._bridge = CvBridge()
        self._info_lock = threading.Lock()
        self._depth_lock = threading.Lock()
        self._latest_info: Optional[CameraInfo] = None
        self._latest_depth_msg: Optional[Image] = None
        self._warned_bad_depth = False
        self._model = None
        self._model_load_error: Optional[str] = None
        self._logged_skip_model = False
        self._device = "cpu"

        self._logged_color_callback = False
        self._logged_depth_cached = False
        self._logged_first_camera_info = False
        self._warned_camera_info_missing = False

        self.declare_parameter("color_topic", "/camera/camera/color/image_raw")
        self.declare_parameter("depth_topic", "/camera/camera/aligned_depth_to_color/image_raw")
        self.declare_parameter("camera_info_topic", "/camera/camera/color/camera_info")
        self.declare_parameter("sync_queue_size", 10)
        self.declare_parameter("sync_slop", 0.1)
        self.declare_parameter(
            "model_path",
            "/home/norman/pap_yaskawa_ws/src/gp7_vision_pipeline/model/box_train_v2/weights/best.pt",
        )
        self.declare_parameter("conf_threshold", 0.5)
        self.declare_parameter("iou_threshold", 0.45)
        self.declare_parameter("device", "cpu")
        self.declare_parameter("publish_debug_image", True)
        self.declare_parameter("depth_roi_half_size", 5)
        self.declare_parameter("target_class_name", "box")

        color_topic = self.get_parameter("color_topic").get_parameter_value().string_value
        depth_topic = self.get_parameter("depth_topic").get_parameter_value().string_value
        info_topic = self.get_parameter("camera_info_topic").get_parameter_value().string_value

        self._pub_detection = self.create_publisher(BoxDetection, "/vision/box_detection", 10)
        self._pub_debug = self.create_publisher(Image, "/vision/debug_image", 10)

        self._info_sub = self.create_subscription(
            CameraInfo,
            info_topic,
            self._on_camera_info,
            qos_profile_sensor_data,
        )

        self._color_sub = self.create_subscription(
            Image,
            color_topic,
            self._on_color_image,
            qos_profile_sensor_data,
        )
        self._depth_sub = self.create_subscription(
            Image,
            depth_topic,
            self._on_depth_image,
            qos_profile_sensor_data,
        )

        self.get_logger().info("YOLO box detector (latest-depth-on-color).")
        self.get_logger().info(f"Subscribing to color topic: {color_topic}")
        self.get_logger().info(f"Subscribing to depth topic: {depth_topic}")
        self.get_logger().info(f"Subscribing to camera_info topic: {info_topic}")
        self._try_load_model()

    def _on_depth_image(self, msg: Image) -> None:
        with self._depth_lock:
            self._latest_depth_msg = msg
        if not self._logged_depth_cached:
            self._logged_depth_cached = True
            self.get_logger().info("DEPTH FRAME CACHED")

    def _try_load_model(self) -> None:
        path = self.get_parameter("model_path").get_parameter_value().string_value
        try:
            yolo_cls = _try_import_yolo()
        except RuntimeError as e:
            self._model_load_error = str(e)
            self.get_logger().error(self._model_load_error)
            return

        p = Path(path).expanduser()
        if not p.is_file():
            self._model_load_error = f"Model file not found: {p}"
            self.get_logger().error(self._model_load_error)
            return

        try:
            self._model = yolo_cls(str(p))
            self._device = self.get_parameter("device").get_parameter_value().string_value or "cpu"
            if self._device:
                self._model.to(self._device)
            self._model_load_error = None
            self.get_logger().info(f"Loaded YOLO model from {p} (device={self._device!r})")
        except Exception as exc:  # noqa: BLE001
            self._model = None
            self._model_load_error = f"Failed to load YOLO model: {exc}"
            self.get_logger().error(self._model_load_error)

    def _on_camera_info(self, msg: CameraInfo) -> None:
        with self._info_lock:
            self._latest_info = msg
        self._warned_camera_info_missing = False
        if not self._logged_first_camera_info:
            self._logged_first_camera_info = True
            self.get_logger().info("First camera_info received.")

    def _get_camera_info(self) -> Optional[CameraInfo]:
        with self._info_lock:
            return self._latest_info

    def _maybe_warn_missing_camera_info(self) -> None:
        if self._get_camera_info() is not None:
            return
        if self._warned_camera_info_missing:
            return
        self._warned_camera_info_missing = True
        self.get_logger().warning(
            "CameraInfo not available yet; continuing without it (detection and debug image still run)."
        )

    def _on_color_image(self, color_msg: Image) -> None:
        if not self._logged_color_callback:
            self._logged_color_callback = True
            self.get_logger().info("COLOR CALLBACK TRIGGERED")

        publish_debug = self.get_parameter("publish_debug_image").get_parameter_value().bool_value
        conf_thr = float(self.get_parameter("conf_threshold").value)
        iou_thr = float(self.get_parameter("iou_threshold").value)
        roi_half = int(self.get_parameter("depth_roi_half_size").value)
        target_name = (
            self.get_parameter("target_class_name").get_parameter_value().string_value.strip().lower()
        )

        self._maybe_warn_missing_camera_info()

        with self._depth_lock:
            depth_msg = self._latest_depth_msg

        depth_cv: Optional[np.ndarray] = None
        depth_enc = ""
        if depth_msg is not None:
            try:
                depth_cv = self._bridge.imgmsg_to_cv2(depth_msg, desired_encoding="passthrough")
                depth_enc = depth_msg.encoding
            except CvBridgeError as e:
                self.get_logger().warning(f"Cached depth cv_bridge error: {e}")
                depth_cv = None

        if self._model is None:
            if self._model_load_error and not self._logged_skip_model:
                self.get_logger().warning(
                    "Skipping inference until model loads successfully."
                )
                self._logged_skip_model = True
            if publish_debug:
                try:
                    bgr = self._bridge.imgmsg_to_cv2(color_msg, desired_encoding="bgr8")
                    dbg = draw_no_detection(bgr, "model not loaded")
                    self._publish_debug_image(color_msg.header, dbg)
                except CvBridgeError as e:
                    self.get_logger().warning(f"Debug image skipped (color cv_bridge): {e}")
            return

        try:
            bgr = self._bridge.imgmsg_to_cv2(color_msg, desired_encoding="bgr8")
        except CvBridgeError as e:
            self.get_logger().warning(f"Color cv_bridge error: {e}")
            return

        if depth_cv is not None and depth_cv.ndim != 2:
            if not self._warned_bad_depth:
                self.get_logger().warning(
                    f"Expected 2D depth image, got shape {depth_cv.shape}; distance may be invalid."
                )
                self._warned_bad_depth = True
            depth_cv = None

        h, w = bgr.shape[:2]
        results = self._model.predict(
            source=bgr,
            verbose=False,
            conf=conf_thr,
            iou=iou_thr,
            device=self._device,
        )
        if not results:
            if publish_debug:
                self._publish_debug_image(color_msg.header, draw_no_detection(bgr, "No detection"))
            return

        r0 = results[0]
        names = getattr(r0, "names", None) or {}
        best: Optional[Tuple[float, str, np.ndarray]] = None

        boxes = getattr(r0, "boxes", None)
        if boxes is None or len(boxes) == 0:
            if publish_debug:
                self._publish_debug_image(color_msg.header, draw_no_detection(bgr, "No detection"))
            return

        for box in boxes:
            cls_id = int(box.cls[0].item()) if box.cls is not None else -1
            cf = float(box.conf[0].item()) if box.conf is not None else 0.0
            raw_name = str(names.get(cls_id, str(cls_id)))
            if raw_name.strip().lower() != target_name:
                continue
            xyxy = box.xyxy[0].cpu().numpy()
            if best is None or cf > best[0]:
                best = (cf, raw_name, xyxy)

        if best is None:
            if publish_debug:
                self._publish_debug_image(color_msg.header, draw_no_detection(bgr, "No detection"))
            return

        conf, class_name, xyxy = best
        x_min_f, y_min_f, x_max_f, y_max_f = [float(v) for v in xyxy]
        x_min, y_min, x_max, y_max = bbox_clip_to_image(
            int(round(x_min_f)),
            int(round(y_min_f)),
            int(round(x_max_f)),
            int(round(y_max_f)),
            w,
            h,
        )
        cx = int(round((x_min + x_max) * 0.5))
        cy = int(round((y_min + y_max) * 0.5))
        width_px = int(x_max - x_min)
        height_px = int(y_max - y_min)

        distance_m = -1.0
        if depth_cv is not None and depth_cv.ndim == 2:
            distance_m = median_depth_meters(depth_cv, cx, cy, roi_half, depth_enc)

        msg = BoxDetection()
        msg.header = color_msg.header
        msg.class_name = class_name
        msg.confidence = float(conf)
        msg.x_min = x_min
        msg.y_min = y_min
        msg.x_max = x_max
        msg.y_max = y_max
        msg.center_x = cx
        msg.center_y = cy
        msg.width_px = width_px
        msg.height_px = height_px
        msg.distance_m = float(distance_m)
        self._pub_detection.publish(msg)
        self.get_logger().info("BOX DETECTION PUBLISHED")

        if publish_debug:
            dbg = draw_box_detection(
                bgr,
                x_min,
                y_min,
                x_max,
                y_max,
                class_name,
                conf,
                distance_m,
                center_x=cx,
                center_y=cy,
                width_px=width_px,
                height_px=height_px,
            )
            self._publish_debug_image(color_msg.header, dbg)

    def _publish_debug_image(self, header: Header, bgr: np.ndarray) -> None:
        try:
            out = self._bridge.cv2_to_imgmsg(bgr, encoding="bgr8")
            out.header = header
            self._pub_debug.publish(out)
            self.get_logger().info("DEBUG IMAGE PUBLISHED")
        except CvBridgeError as e:
            self.get_logger().warning(f"Debug image publish failed: {e}")


def main(args: Optional[List[str]] = None) -> None:
    rclpy.init(args=args)
    node = YoloBoxDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
