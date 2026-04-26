"""Launch the GP7 GUI node.

Launch arguments:
  mode  (default: none)  — 'none', 'sim', or 'real'

Usage:
  ros2 launch gp7_gui gui.launch.py
  ros2 launch gp7_gui gui.launch.py mode:=sim
  ros2 launch gp7_gui gui.launch.py mode:=real
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    mode_arg = DeclareLaunchArgument(
        "mode",
        default_value="none",
        description="Operation mode: none, sim, or real",
    )

    gui_node = Node(
        package="gp7_gui",
        executable="gp7_gui",
        name="gp7_gui_node",
        output="screen",
        arguments=[
            "--mode",
            LaunchConfiguration("mode"),
        ],
    )

    return LaunchDescription([mode_arg, gui_node])
