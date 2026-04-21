import os
import re
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    RegisterEventHandler,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
import xacro


def generate_launch_description() -> LaunchDescription:
    # -------------------------------------------------------------------------
    # Package paths
    # -------------------------------------------------------------------------
    desc_pkg = "gp7_description"
    bringup_pkg = "gp7_bringup"
    moveit_pkg = "gp7_moveit_config"
    gazebo_classic_pkg = "gp7_gazebo_classic"

    desc_share = get_package_share_directory(desc_pkg)
    bringup_share = get_package_share_directory(bringup_pkg)
    gazebo_classic_share = get_package_share_directory(gazebo_classic_pkg)

    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    # gazebo_ros2_control forwards robot_description via CLI parameter overrides.
    robot_description = re.sub(r"<!--.*?-->", "", robot_description_raw, flags=re.DOTALL)

    gazebo_launch_file = os.path.join(
        get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"
    )
    default_world = "/usr/share/gazebo-11/worlds/empty.world"

    # -------------------------------------------------------------------------
    # Launch arguments
    # -------------------------------------------------------------------------
    x_arg = DeclareLaunchArgument("x", default_value="0", description="X position")
    y_arg = DeclareLaunchArgument("y", default_value="0", description="Y position")
    z_arg = DeclareLaunchArgument("z", default_value="0", description="Z position")
    rviz_arg = DeclareLaunchArgument("rviz", default_value="true", description="Launch RViz")
    world_arg = DeclareLaunchArgument(
        "world", default_value=default_world, description="Gazebo world file"
    )

    rviz_enabled = LaunchConfiguration("rviz")
    world = LaunchConfiguration("world")

    # -------------------------------------------------------------------------
    # Gazebo environment (same proven baseline as gazebo_display)
    # -------------------------------------------------------------------------
    gazebo_resource_path = SetEnvironmentVariable(
        name="GAZEBO_RESOURCE_PATH",
        value=":".join(
            [
                "/usr/share/gazebo-11",
                str(Path(desc_share).parent.resolve()),
                desc_share,
                gazebo_classic_share,
                bringup_share,
                os.environ.get("GAZEBO_RESOURCE_PATH", ""),
            ]
        ),
    )

    gazebo_model_path = SetEnvironmentVariable(
        name="GAZEBO_MODEL_PATH",
        value=":".join(
            [
                str(Path(desc_share).parent.resolve()),
                os.path.join(desc_share, "models"),
                os.path.expanduser("~/.gazebo/models"),
                os.environ.get("GAZEBO_MODEL_PATH", ""),
            ]
        ),
    )

    gazebo_plugin_path = SetEnvironmentVariable(
        name="GAZEBO_PLUGIN_PATH",
        value=":".join(
            [
                "/opt/ros/humble/lib",
                os.path.normpath(os.path.join(gazebo_classic_share, "..", "..", "lib")),
            ]
        ),
    )

    # -------------------------------------------------------------------------
    # Gazebo + robot spawn
    # -------------------------------------------------------------------------
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            "use_sim_time": "true",
            "debug": "false",
            "gui": "true",
            "paused": "true",
            "world": world,
        }.items(),
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        arguments=[
            "-entity",
            "gp7_yaskawa",
            "-topic",
            "robot_description",
            "-x",
            LaunchConfiguration("x"),
            "-y",
            LaunchConfiguration("y"),
            "-z",
            LaunchConfiguration("z"),
        ],
    )

    delayed_spawn_robot = TimerAction(period=3.0, actions=[spawn_robot])

    # -------------------------------------------------------------------------
    # Controllers (same proven baseline as gazebo_display)
    # -------------------------------------------------------------------------
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "120",
        ],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "120",
        ],
    )

    delayed_controller_loading = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                TimerAction(period=2.0, actions=[joint_state_broadcaster_spawner]),
                TimerAction(period=3.0, actions=[arm_controller_spawner]),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # MoveIt (start only when controller path is healthy)
    # -------------------------------------------------------------------------
    moveit_config = (
        MoveItConfigsBuilder("gp7", package_name=moveit_pkg)
        .robot_description(file_path=os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro"))
        .robot_description_semantic(file_path="config/gp7_yaskawa.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )

    moveit_params = moveit_config.to_dict()
    moveit_params.update({"use_sim_time": True})

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_params,
            {"use_sim_time": True},
            {"publish_robot_description_semantic": True},
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    wait_controllers_healthy = ExecuteProcess(
        cmd=[
            "python3",
            "-c",
            (
                "import subprocess,time,sys; "
                "deadline=time.time()+120; "
                "ok=False; "
                "\nwhile time.time()<deadline:"
                "\n  try: out=subprocess.check_output(['ros2','control','list_controllers'], text=True, stderr=subprocess.STDOUT)"
                "\n  except Exception: time.sleep(1); continue"
                "\n  if ('joint_state_broadcaster' in out and 'active' in out and 'arm_controller' in out and 'active' in out): ok=True; break"
                "\n  time.sleep(1)"
                "\nsys.exit(0 if ok else 1)"
            ),
        ],
        output="screen",
    )

    start_wait_after_arm_spawner = RegisterEventHandler(
        OnProcessStart(target_action=arm_controller_spawner, on_start=[wait_controllers_healthy])
    )

    move_group_after_controllers = RegisterEventHandler(
        OnProcessExit(target_action=wait_controllers_healthy, on_exit=[move_group])
    )

    # -------------------------------------------------------------------------
    # RViz
    # -------------------------------------------------------------------------
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(bringup_share, "rviz", "rviz.rviz")],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            {"use_sim_time": True},
        ],
        condition=IfCondition(rviz_enabled),
    )

    rviz_after_move_group = RegisterEventHandler(
        OnProcessStart(target_action=move_group, on_start=[rviz])
    )

    return LaunchDescription(
        [
            gazebo_resource_path,
            gazebo_model_path,
            gazebo_plugin_path,
            x_arg,
            y_arg,
            z_arg,
            rviz_arg,
            world_arg,
            gazebo,
            robot_state_publisher,
            delayed_spawn_robot,
            delayed_controller_loading,
            start_wait_after_arm_spawner,
            move_group_after_controllers,
            rviz_after_move_group,
        ]
    )