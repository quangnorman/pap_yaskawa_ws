"""Headless hardware vision stack: RealSense + static TF + pipeline placeholder.

Uses same mount defaults as ``vision_debug.launch.py`` (override ``cam_*`` as needed).

Usage::

    ros2 launch gp7_vision_bringup vision_bringup.launch.py
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

_PI = "3.141592653589793"


def generate_launch_description() -> LaunchDescription:
    bringup_share = get_package_share_directory("gp7_vision_bringup")
    pipeline_share = get_package_share_directory("gp7_vision_pipeline")

    realsense_launch = os.path.join(bringup_share, "launch", "realsense_d435.launch.py")
    static_tf_launch = os.path.join(bringup_share, "launch", "static_tf_camera.launch.py")
    pipeline_launch = os.path.join(pipeline_share, "launch", "vision_pipeline.launch.py")

    static_tf_args = {
        "cam_tx": LaunchConfiguration("cam_tx"),
        "cam_ty": LaunchConfiguration("cam_ty"),
        "cam_tz": LaunchConfiguration("cam_tz"),
        "cam_roll": LaunchConfiguration("cam_roll"),
        "cam_pitch": LaunchConfiguration("cam_pitch"),
        "cam_yaw": LaunchConfiguration("cam_yaw"),
        "cam_parent_frame": LaunchConfiguration("cam_parent_frame"),
        "cam_child_frame": LaunchConfiguration("cam_child_frame"),
        "publish_static_tf": LaunchConfiguration("publish_static_tf"),
    }

    return LaunchDescription(
        [
            DeclareLaunchArgument("cam_parent_frame", default_value="world"),
            DeclareLaunchArgument("cam_child_frame", default_value="camera_link"),
            DeclareLaunchArgument("cam_tx", default_value="0.0"),
            DeclareLaunchArgument("cam_ty", default_value="-0.7"),
            DeclareLaunchArgument("cam_tz", default_value="1.0"),
            DeclareLaunchArgument("cam_roll", default_value=_PI),
            DeclareLaunchArgument("cam_pitch", default_value="0.0"),
            DeclareLaunchArgument("cam_yaw", default_value="0.0"),
            DeclareLaunchArgument(
                "publish_static_tf",
                default_value="true",
                description="Disable if driver already publishes world->camera_link.",
            ),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(realsense_launch)),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(static_tf_launch),
                launch_arguments=static_tf_args.items(),
            ),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(pipeline_launch)),
        ]
    )
