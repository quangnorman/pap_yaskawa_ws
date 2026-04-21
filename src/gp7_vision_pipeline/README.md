# gp7_vision_pipeline

Perception-only nodes for the GP7 workspace (Intel RealSense D435, YOLO box detection, future 3D box extent in **`base_link`**). **Does not** send motion commands or spawn Gazebo models; the arm is driven only via MoveIt 2 / `gp7_task_executor`.

## YOLO box detector (RealSense)

**Node:** `yolo_box_detector_node`  
**Launch:** `launch/yolo_box_detector.launch.py`  
**Parameters:** `config/yolo_box_detector.yaml`

### Pipeline

Intel RealSense D435 (color + **aligned** depth) → time-synced pair → Ultralytics YOLO on color → highest-confidence **`target_class_name`** detection → median depth in a small ROI at the bbox center → publish **`gp7_vision_pipeline/BoxDetection`** and optional debug image.

### Subscribed topics (defaults)

| Topic | Message |
|-------|---------|
| `/camera/color/image_raw` | `sensor_msgs/Image` (color) |
| `/camera/aligned_depth_to_color/image_raw` | `sensor_msgs/Image` (depth aligned to color) |
| `/camera/color/camera_info` | `sensor_msgs/CameraInfo` (optional; logged if missing; detections still publish) |

### Published topics

| Topic | Message |
|-------|---------|
| `/vision/box_detection` | `gp7_vision_pipeline/BoxDetection` |
| `/vision/debug_image` | `sensor_msgs/Image` (`bgr8`, overlays) |

### Parameters (`yolo_box_detector_node`)

| Parameter | Description |
|-----------|-------------|
| `color_topic` | Color image topic |
| `depth_topic` | Aligned depth topic |
| `camera_info_topic` | Camera info (not required for distance; used for future intrinsics work) |
| `sync_queue_size` | Approximate sync queue size |
| `sync_slop` | Approximate sync time slop (seconds) |
| `model_path` | Path to `best.pt` (Ultralytics) |
| `conf_threshold` | YOLO confidence threshold |
| `iou_threshold` | YOLO NMS IoU threshold |
| `device` | `cpu` or CUDA device string (e.g. `0`) |
| `publish_debug_image` | Publish `/vision/debug_image` |
| `depth_roi_half_size` | Square ROI half-extent (pixels) for median depth |
| `target_class_name` | Class name to keep (case-insensitive), default `box` |

### Custom message: `BoxDetection.msg`

`std_msgs/Header header`, `string class_name`, `float32 confidence`, bbox ints (`x_min` … `height_px`), `float32 distance_m` (meters, or **`-1.0`** if invalid / no depth). When no target is detected, `class_name` is empty, `confidence` is `0`, bbox centers are **`-1`**, `distance_m` is **`-1.0`**.

### Other nodes

| Executable | Purpose |
|------------|---------|
| `vision_pipeline_placeholder` | Parameter shell for future pipeline. |
| `realsense_depth_debug` | RGB + aligned depth + `CameraInfo` verification; center-pixel depth. |

## Dependencies

- ROS 2 Humble: `rclpy`, `sensor_msgs`, `std_msgs`, `cv_bridge`, `message_filters`
- System: `python3-opencv`, `python3-numpy`
- **Python (pip):** `ultralytics` (YOLO). Example: `pip install ultralytics`

If `cv_bridge` fails to import (e.g. NumPy 2 vs ROS Humble binaries), use a Python environment where **`numpy<2`** matches your distro `cv_bridge`, or use the system Python that ships with ROS.

## Build

```bash
source /opt/ros/humble/setup.bash
cd /home/norman/pap_yaskawa_ws
colcon build --packages-select gp7_vision_pipeline
source install/setup.bash
```

## Run RealSense (aligned depth)

```bash
source /opt/ros/humble/setup.bash
source /home/norman/pap_yaskawa_ws/install/setup.bash
ros2 launch realsense2_camera rs_launch.py align_depth.enable:=true
```

Remap or edit YAML if your camera namespace differs from `/camera/...`.

## Run detector

```bash
source /opt/ros/humble/setup.bash
source /home/norman/pap_yaskawa_ws/install/setup.bash
ros2 launch gp7_vision_pipeline yolo_box_detector.launch.py
```

Place weights at `model/box_train_v2/weights/best.pt` or override `model_path` in the YAML / CLI.

## View debug image

```bash
ros2 run rqt_image_view rqt_image_view
```

Subscribe to `/vision/debug_image`.

## Echo detection topic

```bash
ros2 topic echo /vision/box_detection
```

## Legacy launch / sim configs

```bash
ros2 launch gp7_vision_pipeline vision_pipeline.launch.py
```

See `config/vision_sim_rgbd.yaml` for Gazebo-style depth topic names vs RealSense.

## TF / frames

Results use the **color image header** (`header.frame_id`, typically the optical or color optical frame from the driver). Downstream nodes should project to `base_link` / `world` using your calibrated TF (`world`, `base_link`, `camera_link`, `camera_color_optical_frame`, etc.).

## Package layout notes

- **`msg/BoxDetection.msg`** is built with **`rosidl_generate_interfaces`** in this package. Because that conflicts with `ament_python_install_package` for the same project name, **Python modules are installed via CMake** (`install(DIRECTORY gp7_vision_pipeline/ ...)`) next to the generated `msg` package.
- **`setup.py` / `setup.cfg`**: present for tooling consistency; the **ament_cmake** `CMakeLists.txt** is the build entry point used by `colcon`.
