"""
ROS 2 (Humble) launch file to visualize a robot model in RViz 2.

This launch starts:
  1) robot_state_publisher:
     - Publishes the TF tree for the robot using the URDF from `robot_description`.
  2) joint_state_publisher_gui:
     - Provides GUI sliders to publish /joint_states so you can move joints without a real driver.
  3) rviz2:
     - Opens RViz with a predefined configuration file.

Package layout assumptions (inside `gp7_description` / `gp7_bringup`):
  - urdf/gp7_yaskawa.urdf
  - rviz/urdf_config.rviz
"""

import os
import xacro
from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory

def generate_launch_description() -> LaunchDescription:
    """Entry point for ROS 2 launch. Must return a LaunchDescription."""

    # -------------------------------------------------------------------------
    # Resolve paths inside the package share directory
    # -------------------------------------------------------------------------
    desc_pkg = "gp7_description"
    bringup_pkg = "gp7_bringup"

    desc_share = get_package_share_directory(desc_pkg)
    bringup_share = get_package_share_directory(bringup_pkg)
    
    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    rviz_config_path = os.path.join(bringup_share, "rviz", "rviz.rviz")

    # -------------------------------------------------------------------------
    # Build the 'robot_description' parameter
    # -------------------------------------------------------------------------
    # NOTE:
    # You are intentionally invoking xacro here.
    # This is only required if the URDF contains xacro macros/includes.
    #
    # IMPORTANT:
    # Your original command uses 'xacro ' (with a trailing space).
    # If it works on your system, keep it as-is. If you ever see path issues,
    # replace it with 'xacro' (no trailing space).
    # Convert Xacro -> URDF XML string for the robot_description parameter
    robot_description = xacro.process_file(xacro_file).toxml()
    # -------------------------------------------------------------------------
    # Nodes
    # -------------------------------------------------------------------------

    # Publishes TF transforms based on the robot model and incoming joint states.
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    # Publishes /joint_states from a GUI (useful for visualization without hardware).
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
    )

    # Starts RViz 2 with the provided configuration file.
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config_path],
    )

    # -------------------------------------------------------------------------
    # Launch description
    # -------------------------------------------------------------------------
    return LaunchDescription(
        [
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz2_node,
        ]
    )
