"""Full stack: Gazebo Classic GP7 sim + bridge + fake vision topics (no YOLO).

Use ``scenario:=b`` for the alternate box dimensions preset.
"""

from __future__ import annotations

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    scenario_arg = DeclareLaunchArgument(
        "scenario",
        default_value="a",
        description=(
            "Test publisher preset: 'a' = 0.10×0.05×0.10 m @ z=0.45; "
            "'b' = 0.12×0.06×0.08 m @ z=0.44 (table contact z=0.40)."
        ),
    )

    def launch_setup(context, *args, **kwargs):
        scenario = LaunchConfiguration("scenario").perform(context).strip().lower()
        gp7_gazebo_share = get_package_share_directory("gp7_gazebo_classic")
        bridge_share = get_package_share_directory("gp7_vision_gazebo_bridge")

        sim_launch = os.path.join(gp7_gazebo_share, "launch", "sim_moveit_vision_rgbd.launch.py")
        bridge_params = os.path.join(bridge_share, "config", "bridge_node_params.yaml")

        if scenario in ("b", "2", "scenario_b"):
            test_pub = os.path.join(bridge_share, "config", "test_publisher_params_scenario_b.yaml")
        else:
            test_pub = os.path.join(bridge_share, "config", "test_publisher_params.yaml")

        return [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(sim_launch),
                launch_arguments={
                    "rviz": "false",
                    "launch_vision": "false",
                }.items(),
            ),
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
