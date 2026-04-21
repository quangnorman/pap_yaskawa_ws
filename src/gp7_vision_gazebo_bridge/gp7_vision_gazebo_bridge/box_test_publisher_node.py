"""Test publisher for the vision->Gazebo bridge (no YOLO).

Publishes configurable fake box pose and size on:
  - /vision/box_pose (geometry_msgs/PoseStamped)
  - /vision/box_size (geometry_msgs/Vector3)

Vector3 mapping: x = length, y = width, z = height (meters), matching the bridge SDF box.
Pose position is the geometric center of the box in ``frame_id`` (default ``world``).
"""

from __future__ import annotations

import math
import sys
import time
from typing import Optional

import rclpy
from geometry_msgs.msg import PoseStamped, Quaternion, Vector3
from rclpy.node import Node
from rclpy.qos import QoSProfile


def _quat_from_yaw(yaw_rad: float) -> Quaternion:
    half = yaw_rad / 2.0
    q = Quaternion()
    q.w = math.cos(half)
    q.x = 0.0
    q.y = 0.0
    q.z = math.sin(half)
    return q


class BoxTestPublisherNode(Node):
    def __init__(self) -> None:
        super().__init__("box_test_publisher_node")

        self.declare_parameter("pose_topic", "/vision/box_pose")
        self.declare_parameter("size_topic", "/vision/box_size")
        self.declare_parameter("frame_id", "world")

        # Box center (m), world frame by default
        self.declare_parameter("x", 0.0)
        self.declare_parameter("y", -0.7)
        self.declare_parameter("z", 0.45)

        self.declare_parameter("yaw_rad", 0.0)

        # Box dimensions (m): length (X), width (Y), height (Z) for SDF <box><size>
        self.declare_parameter("length_m", 0.10)
        self.declare_parameter("width_m", 0.05)
        self.declare_parameter("height_m", 0.10)

        self.declare_parameter("publish_rate_hz", 1.0)
        self.declare_parameter("log_each_publish", False)

        pose_topic: str = self.get_parameter("pose_topic").get_parameter_value().string_value
        size_topic: str = self.get_parameter("size_topic").get_parameter_value().string_value
        frame_id: str = self.get_parameter("frame_id").get_parameter_value().string_value

        qos = QoSProfile(depth=1)

        self._pose_pub = self.create_publisher(PoseStamped, pose_topic, qos)
        self._size_pub = self.create_publisher(Vector3, size_topic, qos)

        rate_hz = float(self.get_parameter("publish_rate_hz").value)
        period = 1.0 / max(rate_hz, 0.01)

        self.create_timer(period, self._on_timer)
        self._frame_id = frame_id
        self._log_each = bool(self.get_parameter("log_each_publish").value)

        self.get_logger().info(
            f"Test publisher: '{pose_topic}' + '{size_topic}' at {rate_hz:.2f} Hz "
            f"(params: x,y,z, yaw_rad, length_m, width_m, height_m)."
        )

    def _on_timer(self) -> None:
        x = float(self.get_parameter("x").value)
        y = float(self.get_parameter("y").value)
        z = float(self.get_parameter("z").value)
        yaw = float(self.get_parameter("yaw_rad").value)

        length_m = float(self.get_parameter("length_m").value)
        width_m = float(self.get_parameter("width_m").value)
        height_m = float(self.get_parameter("height_m").value)

        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = self._frame_id
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation = _quat_from_yaw(yaw)

        size = Vector3()
        size.x = length_m
        size.y = width_m
        size.z = height_m

        self._pose_pub.publish(pose)
        self._size_pub.publish(size)

        if self._log_each:
            self.get_logger().info(
                f"Published test box center=({x:.3f},{y:.3f},{z:.3f}) "
                f"size=({length_m:.3f}x{width_m:.3f}x{height_m:.3f}) m"
            )


def main(argv: Optional[list[str]] = None) -> None:
    rclpy.init(args=argv)
    node = BoxTestPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main(sys.argv)
