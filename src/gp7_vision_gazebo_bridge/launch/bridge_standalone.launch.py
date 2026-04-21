"""Bridge + test publisher only — start Gazebo yourself first.

Use when ``sim_moveit_vision_rgbd`` (or another world) is already running and
``/spawn_entity`` + ``/delete_entity`` are available.

Example::

  ros2 launch gp7_vision_gazebo_bridge bridge_standalone.launch.py scenario:=a
"""

from __future__ import annotations

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    scenario_arg = DeclareLaunchArgument(
        "scenario",
        default_value="a",
        description="Same presets as bridge_test.launch.py ('a' or 'b').",
    )

    def launch_setup(context, *args, **kwargs):
        scenario = LaunchConfiguration("scenario").perform(context).strip().lower()
        bridge_share = get_package_share_directory("gp7_vision_gazebo_bridge")
        bridge_params = os.path.join(bridge_share, "config", "bridge_node_params.yaml")

        if scenario in ("b", "2", "scenario_b"):
            test_pub = os.path.join(bridge_share, "config", "test_publisher_params_scenario_b.yaml")
        else:
            test_pub = os.path.join(bridge_share, "config", "test_publisher_params.yaml")

        return [
            Node(
                package="gp7_vision_gazebo_bridge",
                executable="box_spawn_bridge_node",
                name="box_spawn_bridge_node",
                output="screen",
                parameters=[bridge_params],
            ),
            Node(
                package="gp7_vision_gazebo_bridge",
                executable="box_test_publisher_node",
                name="box_test_publisher_node",
                output="screen",
                parameters=[test_pub],
            ),
        ]

    return LaunchDescription(
        [
            scenario_arg,
            OpaqueFunction(function=launch_setup),
        ]
    )
