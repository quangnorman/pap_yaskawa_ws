"""
ROS 2 launch file to visualize the GP7 robot model in RViz 2.

This launch starts:
  1) robot_state_publisher
     - Publishes the TF tree using the robot_description parameter.
  2) joint_state_publisher_gui
     - Provides GUI sliders to publish /joint_states so you can move joints
       without a real driver or Gazebo.
  3) rviz2
     - Opens RViz with a predefined configuration file.

The robot description is produced by xacro from the _fake xacro file, which
has identical visuals and kinematics to the real URDF but uses
mock_components/GenericSystem instead of gazebo_ros2_control, so it has
no external controller config dependency.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    desc_pkg_share = FindPackageShare('gp7_description')
    xacro_file = PathJoinSubstitution([
        desc_pkg_share, 'urdf', 'gp7_yaskawa_fake.urdf.xacro'
    ])
    rviz_config = PathJoinSubstitution([
        desc_pkg_share, 'rviz', 'display.rviz'
    ])

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'model',
            default_value=xacro_file,
            description='Path to the robot description file (.xacro)'
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': False,
            }]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config]
        ),
    ])
