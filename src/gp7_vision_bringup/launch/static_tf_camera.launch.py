"""Static transform: eye-to-hand ``cam_parent_frame`` → ``cam_child_frame`` (hardware path).

Default (measured): **world → camera_link**

- translation (m): ``(0.0, -0.7, 1.0)``
- RPY (rad) for ``tf2_ros/static_transform_publisher``:
  - roll = ``pi``
  - pitch = ``0.0``
  - yaw = ``0.0``

This static TF only publishes ``world → camera_link``.
The RealSense driver is expected to provide ``camera_link → camera_color_optical_frame``
(ROS optical frame convention). Here, ``camera_link`` is the camera's mechanical/body frame and
``camera_color_optical_frame`` is the vision/image frame used for image projection.

If the driver already publishes ``camera_link`` TF, you can
disable this static publisher with ``publish_static_tf:=false``.

Uses ``--roll/--pitch/--yaw`` (ROS 2 Humble ``static_transform_publisher``).

Usage::

    ros2 launch gp7_vision_bringup static_tf_camera.launch.py
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

_PI = "3.141592653589793"


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "cam_parent_frame",
                default_value="world",
                description="Eye-to-hand: camera is rigidly attached relative to this frame.",
            ),
            DeclareLaunchArgument(
                "cam_child_frame",
                default_value="camera_link",
                description="Must match RealSense root frame name from the driver.",
            ),
            DeclareLaunchArgument(
                "cam_tx",
                default_value="0.0",
                description="Mount translation X in parent frame (m).",
            ),
            DeclareLaunchArgument(
                "cam_ty",
                default_value="-0.7",
                description="Mount translation Y in parent frame (m); measured value (REP-103 right = -Y).",
            ),
            DeclareLaunchArgument(
                "cam_tz",
                default_value="1.0",
                description="Mount translation Z in parent frame (m).",
            ),
            DeclareLaunchArgument(
                "cam_roll",
                default_value=_PI,
                description="Roll (rad); measured value π — lens axis toward −parent Z (down).",
            ),
            DeclareLaunchArgument(
                "cam_pitch",
                default_value="0.0",
                description="Pitch (rad); default 0 — no tilt off vertical.",
            ),
            DeclareLaunchArgument(
                "cam_yaw",
                default_value="0.0",
                description="Yaw (rad); measured value 0 — tail/USB toward robot side per your mounting.",
            ),
            DeclareLaunchArgument(
                "publish_static_tf",
                default_value="true",
                description="If false, do not publish world->camera_link static TF (e.g. driver already publishes it).",
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="base_link_to_camera_link_static",
                output="screen",
                condition=IfCondition(LaunchConfiguration("publish_static_tf")),
                arguments=[
                    "--x",
                    LaunchConfiguration("cam_tx"),
                    "--y",
                    LaunchConfiguration("cam_ty"),
                    "--z",
                    LaunchConfiguration("cam_tz"),
                    "--roll",
                    LaunchConfiguration("cam_roll"),
                    "--pitch",
                    LaunchConfiguration("cam_pitch"),
                    "--yaw",
                    LaunchConfiguration("cam_yaw"),
                    "--frame-id",
                    LaunchConfiguration("cam_parent_frame"),
                    "--child-frame-id",
                    LaunchConfiguration("cam_child_frame"),
                ],
            ),
        ]
    )
