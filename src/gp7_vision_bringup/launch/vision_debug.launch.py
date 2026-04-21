"""Hardware RealSense D435 debug: driver + static TF + depth sanity node + optional RViz.

Static TF defaults: mount (0, −1, 1.5) m and RPY for **lens down**, **tail toward robot**
(see ``static_tf_camera.launch.py``). Override with ``cam_*`` launch args.

Does **not** start MoveIt / Gazebo. For simulation use ``gp7_gazebo_classic`` RGB-D launch.

Usage::

    ros2 launch gp7_vision_bringup vision_debug.launch.py
    ros2 launch gp7_vision_bringup vision_debug.launch.py depth_debug_params:=/path/to/custom.yaml
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EqualsSubstitution
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

_PI = "3.141592653589793"


def generate_launch_description() -> LaunchDescription:
    bringup_share = get_package_share_directory("gp7_vision_bringup")
    pipeline_share = get_package_share_directory("gp7_vision_pipeline")

    realsense_launch = os.path.join(bringup_share, "launch", "realsense_d435.launch.py")
    static_tf_launch = os.path.join(bringup_share, "launch", "static_tf_camera.launch.py")
    default_debug_params = os.path.join(pipeline_share, "config", "realsense_depth_debug.yaml")

    use_rviz = LaunchConfiguration("use_rviz")
    depth_debug_params = LaunchConfiguration("depth_debug_params")

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
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
                description="If true, start RViz 2 (configure Image panels manually).",
            ),
            DeclareLaunchArgument(
                "depth_debug_params",
                default_value=default_debug_params,
                description="Parameter YAML for realsense_depth_debug (topic names).",
            ),
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
                description="Disable if the RealSense driver already publishes world->camera_link.",
            ),
            IncludeLaunchDescription(PythonLaunchDescriptionSource(realsense_launch)),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(static_tf_launch),
                launch_arguments=static_tf_args.items(),
            ),
            Node(
                package="gp7_vision_pipeline",
                executable="realsense_depth_debug",
                name="realsense_depth_debug",
                output="screen",
                parameters=[depth_debug_params],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="vision_debug_rviz",
                output="screen",
                condition=IfCondition(EqualsSubstitution(use_rviz, "true")),
            ),
        ]
    )
