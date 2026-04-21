"""Simulation-only vision helpers: depth debug node with Gazebo RGB-D topic defaults.

Does **not** start RealSense. Use after Gazebo has spawned ``gp7_sim_rgbd_camera``.

Typical use: included from ``gp7_gazebo_classic/sim_moveit_vision_rgbd.launch.py``.

Usage (standalone, rare)::

    ros2 launch gp7_vision_bringup vision_sim_rgbd.launch.py
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pipeline_share = get_package_share_directory("gp7_vision_pipeline")
    default_params = os.path.join(pipeline_share, "config", "vision_sim_rgbd.yaml")

    params_file = LaunchConfiguration("vision_sim_params")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "vision_sim_params",
                default_value=default_params,
                description="YAML for realsense_depth_debug topic remaps (sim camera).",
            ),
            Node(
                package="gp7_vision_pipeline",
                executable="realsense_depth_debug",
                name="realsense_depth_debug",
                output="screen",
                parameters=[params_file, {"use_sim_time": True}],
            ),
        ]
    )
