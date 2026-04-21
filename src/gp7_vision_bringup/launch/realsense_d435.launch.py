"""Start Intel RealSense D435 via ``realsense2_camera/rs_launch.py``.

Launch arguments are loaded from ``config/d435_realsense_launch_args.yaml``.
Requires: ``sudo apt install ros-humble-realsense2-camera`` (or build from source).

Usage::

    ros2 launch gp7_vision_bringup realsense_d435.launch.py
"""

from __future__ import annotations

import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def _include_realsense(context, *args, **kwargs):
    bringup_share = get_package_share_directory("gp7_vision_bringup")
    cfg_path = os.path.join(bringup_share, "config", "d435_realsense_launch_args.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    launch_args = data.get("launch_arguments", {})
    pairs = [(str(k), str(v)) for k, v in launch_args.items()]

    rs_launch = PathJoinSubstitution(
        [FindPackageShare("realsense2_camera"), "launch", "rs_launch.py"]
    )
    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rs_launch),
            launch_arguments=pairs,
        )
    ]


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([OpaqueFunction(function=_include_realsense)])
