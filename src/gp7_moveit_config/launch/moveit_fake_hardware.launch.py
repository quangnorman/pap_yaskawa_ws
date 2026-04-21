"""
Offline simulation: mock ros2_control (GenericSystem) + MoveIt 2 — no Gazebo, no MotoROS2.

Exposes /arm_controller/follow_joint_trajectory and runs move_group for plan+execute tests.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    desc_share = get_package_share_directory("gp7_description")
    bringup_share = get_package_share_directory("gp7_bringup")
    moveit_pkg = "gp7_moveit_config"

    controller_yaml = os.path.join(bringup_share, "config", "gp7_controller.yaml")
    default_model = os.path.join(desc_share, "urdf", "gp7_yaskawa_fake.urdf.xacro")

    declared_arguments = [
        DeclareLaunchArgument(
            "model",
            default_value=default_model,
            description="Path to fake-hardware xacro (mock_components).",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulation clock if true (bags); false for fake stack.",
        ),
        DeclareLaunchArgument(
            "rviz",
            default_value="false",
            description="Launch RViz if true.",
        ),
    ]

    model = LaunchConfiguration("model")
    use_sim_time = LaunchConfiguration("use_sim_time")
    rviz_enable = LaunchConfiguration("rviz")

    use_sim_bool = ParameterValue(use_sim_time, value_type=bool)
    robot_description = ParameterValue(Command(["xacro ", model]), value_type=str)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": robot_description, "use_sim_time": use_sim_bool}
        ],
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="screen",
        parameters=[
            {"robot_description": robot_description, "use_sim_time": use_sim_bool},
            controller_yaml,
        ],
    )

    # Single spawner loads JSB first then arm_controller (avoids races / "already loaded")
    controllers_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "120",
        ],
        parameters=[{"use_sim_time": use_sim_bool}],
    )

    moveit_config = (
        MoveItConfigsBuilder("gp7", package_name=moveit_pkg)
        .robot_description(
            file_path=os.path.join(desc_share, "urdf", "gp7_yaskawa_fake.urdf.xacro")
        )
        .robot_description_semantic(file_path="config/gp7_yaskawa.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )

    moveit_params = moveit_config.to_dict()
    moveit_params["use_sim_time"] = use_sim_bool

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_params,
            {"publish_robot_description_semantic": True},
        ],
        arguments=["--ros-args", "--log-level", "warn"],
    )

    rviz_config = os.path.join(
        get_package_share_directory(moveit_pkg), "config", "moveit.rviz"
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            {"use_sim_time": use_sim_bool},
        ],
    )

    # Stagger startup: controller_manager must be running before spawners
    delayed_controllers = TimerAction(period=6.0, actions=[controllers_spawner])
    delayed_move_group = TimerAction(period=18.0, actions=[move_group])
    delayed_rviz = GroupAction(
        condition=IfCondition(rviz_enable),
        actions=[TimerAction(period=22.0, actions=[rviz_node])],
    )

    ld = LaunchDescription()
    for a in declared_arguments:
        ld.add_action(a)
    ld.add_action(robot_state_publisher)
    ld.add_action(control_node)
    ld.add_action(delayed_controllers)
    ld.add_action(delayed_move_group)
    ld.add_action(delayed_rviz)
    return ld
