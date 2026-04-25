"""Top-level simulation + MoveIt + task_executor launch file.

ARCHITECTURE OVERVIEW
====================
This package provides two parallel bringup stacks:

  sim_mode.launch.py  (this file)
    = Gazebo Classic (simulation) + ros2_control simulation controllers
      + MoveIt (OMPL) + RViz + gp7_task_executor

  real_mode.launch.py
    = MotoROS2 (real hardware) + MoveIt (OMPL) + RViz + gp7_task_executor

Both files share the same task_executor configuration (waypoints, planning
parameters) and the same MoveIt planning group ("arm").  The only differences
are the low-level backend (Gazebo vs. MotoROS2) and the controller namespace
(arm_controller on /controller_manager vs. robot1_controller on /robot1).

STARTUP ORDER
=============
1. Gazebo Classic + environment variables (GAZEBO_RESOURCE/MODEL/PLUGIN_PATH)
2. robot_state_publisher  [publishes /robot_description]
3. spawn_entity.py        [3 s after Gazebo — spawns robot in simulation]
4. controller spawners   [after spawn — joint_state_broadcaster, arm_controller]
5. move_group            [after controllers healthy — MoveIt planning node]
6. RViz + task_executor  [2 s after move_group starts]

LAUNCH ARGUMENTS
===============
  use_rviz             (default: true)  — launch RViz alongside move_group
  start_task_executor   (default: true) — launch gp7_task_executor node
  use_sim_time         (default: true)  — forward sim_time to all nodes
  x / y / z            (default: 0/0/0.33) — robot spawn position in Gazebo

TASK EXECUTOR SERVICES
=====================
  /move_to_named_target       — SRDF named target (e.g. "Home")
  /move_to_joint_target       — joint-space goal
  /move_to_pose_target        — pose goal (position + quaternion)
  /move_to_cartesian_target   — xyz-only goal (fixed orientation)
  /move_sequence              — sequence of named waypoints
  /move_cartesian_sequence    — sequence of cartesian points
"""

import os
import re
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    LogInfo,
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
    # Packages
    # -------------------------------------------------------------------------
    desc_pkg = "gp7_description"
    bringup_pkg = "gp7_bringup"
    moveit_pkg = "gp7_moveit_config"
    gazebo_classic_pkg = "gp7_gazebo_classic"
    executor_pkg = "gp7_task_executor"

    desc_share = get_package_share_directory(desc_pkg)
    bringup_share = get_package_share_directory(bringup_pkg)
    moveit_share = get_package_share_directory(moveit_pkg)
    gazebo_classic_share = get_package_share_directory(gazebo_classic_pkg)
    executor_share = get_package_share_directory(executor_pkg)

    # -------------------------------------------------------------------------
    # Launch arguments
    # -------------------------------------------------------------------------
    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz alongside move_group",
    )
    start_task_executor_arg = DeclareLaunchArgument(
        "start_task_executor",
        default_value="true",
        description="Launch the gp7_task_executor node",
    )
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Enable sim_time for all nodes",
    )
    x_arg = DeclareLaunchArgument(
        "x", default_value="0", description="Robot spawn X position in Gazebo"
    )
    y_arg = DeclareLaunchArgument(
        "y", default_value="0", description="Robot spawn Y position in Gazebo"
    )
    z_arg = DeclareLaunchArgument(
        "z",
        default_value="0.33",
        description="Robot spawn Z position (base_link 0.33 m above world ground)",
    )

    sim_time = LaunchConfiguration("use_sim_time")
    rviz_enabled = LaunchConfiguration("use_rviz")

    # -------------------------------------------------------------------------
    # Robot description
    #
    # We pass the simulation controller YAML so ros2_control.xacro includes the
    # ros2_control_plugin and the joint_trajectory_interface.  This robot_description
    # is the single source of truth for rsp, Gazebo spawn, move_group, and rviz.
    # -------------------------------------------------------------------------
    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    sim_controller_yaml_path = os.path.join(bringup_share, "config", "gp7_controller.yaml")
    initial_positions_path = os.path.join(desc_share, "config", "initial_positions.yaml")
    robot_description_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf")

    robot_description_raw = xacro.process_file(
        xacro_file,
        mappings={
            "controller_yaml": sim_controller_yaml_path,
            "initial_positions_file": initial_positions_path,
            "robot_description_file": robot_description_file,
        },
    ).toxml()
    # Strip XML comments so the URDF is valid when Gazebo parses it.
    robot_description = re.sub(r"<!--.*?-->", "", robot_description_raw, flags=re.DOTALL)

    # -------------------------------------------------------------------------
    # Gazebo Classic environment
    # -------------------------------------------------------------------------
    gazebo_launch_file = os.path.join(
        get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"
    )
    world_file = os.path.join(gazebo_classic_share, "worlds", "table.world")

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
    # Step 1: Gazebo Classic + robot_state_publisher
    # -------------------------------------------------------------------------
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": robot_description},
            {"use_sim_time": sim_time},
        ],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            "use_sim_time": "true",
            "debug": "false",
            "gui": "true",
            "paused": "true",
            "world": world_file,
        }.items(),
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_entity",
        output="screen",
        arguments=[
            "-entity", "gp7_yaskawa",
            "-topic", "robot_description",
            "-x", LaunchConfiguration("x"),
            "-y", LaunchConfiguration("y"),
            "-z", LaunchConfiguration("z"),
        ],
    )
    delayed_spawn = TimerAction(period=3.0, actions=[spawn_robot])

    # -------------------------------------------------------------------------
    # Step 2: ros2_control simulation controllers
    # -------------------------------------------------------------------------
    jsb_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="jsb_spawner",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager", "/controller_manager",
            "--controller-manager-timeout", "120",
        ],
    )
    arm_ctrl_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="arm_ctrl_spawner",
        output="screen",
        arguments=[
            "arm_controller",
            "--controller-manager", "/controller_manager",
            "--controller-manager-timeout", "120",
        ],
    )

    controllers_after_spawn = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                TimerAction(period=2.0, actions=[jsb_spawner]),
                TimerAction(period=3.0, actions=[arm_ctrl_spawner]),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Step 3: MoveIt move_group
    #
    # Wait until both controllers are active before starting move_group.
    # Also apply the same OMPL-only overrides as sim_moveit.launch.py so
    # trajectories always contain velocity + time_from_start data.
    # -------------------------------------------------------------------------
    sim_controller_yaml_for_moveit = os.path.join(
        moveit_share, "config", "moveit_controllers.yaml"
    )

    moveit_config = (
        MoveItConfigsBuilder("gp7_yaskawa", package_name=moveit_pkg)
        .robot_description(file_path=os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro"))
        .robot_description_semantic(
            file_path=os.path.join(moveit_share, "config", "gp7_yaskawa.srdf")
        )
        .trajectory_execution(file_path=sim_controller_yaml_for_moveit)
        .planning_pipelines("ompl")
        .to_moveit_configs()
    )
    moveit_params = moveit_config.to_dict()
    moveit_params["use_sim_time"] = True

    # Strip auto-discovered pilz/chomp plugins (same as sim_moveit.launch.py).
    moveit_params.pop("pilz_industrial_motion_planner", None)
    moveit_params.pop("chomp", None)
    if "planning_pipelines" in moveit_params:
        moveit_params["planning_pipelines"] = ["ompl"]

    ompl_explicit_params = {
        "planning_pipelines": ["ompl"],
        "default_planning_pipeline": "ompl",
        "ompl": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "request_adapters": (
                "default_planner_request_adapters/AddTimeOptimalParameterization "
                "default_planner_request_adapters/FixWorkspaceBounds "
                "default_planner_request_adapters/FixStartStateBounds "
                "default_planner_request_adapters/FixStartStateCollision "
                "default_planner_request_adapters/FixStartStatePathConstraints"
            ),
        },
        "default_velocity_scaling_factor": 0.5,
        "default_acceleration_scaling_factor": 0.5,
    }

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        name="move_group",
        output="screen",
        parameters=[
            moveit_params,
            {"robot_description": robot_description},
            {"publish_robot_description_semantic": True},
            {"use_sim_time": True},
            ompl_explicit_params,
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # Block until controllers are healthy, then launch move_group.
    wait_controllers_healthy = ExecuteProcess(
        cmd=[
            "python3", "-c",
            "import subprocess,time,sys\n"
            "deadline=time.time()+120\n"
            "ok=False\n"
            "while time.time()<deadline:\n"
            "  try: out=subprocess.check_output(['ros2','control','list_controllers'],text=True,stderr=subprocess.STDOUT)\n"
            "  except Exception: time.sleep(1); continue\n"
            "  if 'joint_state_broadcaster' in out and 'active' in out and 'arm_controller' in out and 'active' in out: ok=True; break\n"
            "  time.sleep(1)\n"
            "sys.exit(0 if ok else 1)\n"
        ],
        output="screen",
    )

    wait_after_arm = RegisterEventHandler(
        OnProcessStart(target_action=arm_ctrl_spawner, on_start=[wait_controllers_healthy])
    )
    move_group_after_controllers = RegisterEventHandler(
        OnProcessExit(target_action=wait_controllers_healthy, on_exit=[move_group])
    )

    # -------------------------------------------------------------------------
    # Step 4: RViz
    # -------------------------------------------------------------------------
    rviz_config = os.path.join(bringup_share, "rviz", "rviz.rviz")
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[
            {"robot_description": robot_description},
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            ompl_explicit_params,
            {"use_sim_time": True},
        ],
        condition=IfCondition(rviz_enabled),
    )

    # -------------------------------------------------------------------------
    # Step 5: gp7_task_executor_node
    #
    # The executor reads the robot_description parameter published on the
    # /robot_description topic (from rsp).  It connects to move_group over
    # the ROS 2 action graph, so no direct parameter passing is needed.
    # -------------------------------------------------------------------------
    task_executor = Node(
        package="gp7_task_executor",
        executable="task_executor_node",
        name="task_executor_node",
        output="screen",
        parameters=[
            {
                "move_group_name": "arm",
                "base_frame": "base_link",
                "ee_link": "tool0",
                "waypoints_config_path": os.path.join(executor_share, "config", "joint_waypoints.yaml"),
                "cartesian_points_config_path": os.path.join(executor_share, "config", "cartesian_points.yaml"),
                "pose_waypoints_config_path": os.path.join(executor_share, "config", "pose_waypoints.yaml"),
                "planning_time": 2.0,
                "num_planning_attempts": 5,
                "max_velocity_scaling_factor": 0.5,
                "max_acceleration_scaling_factor": 0.5,
                "use_sim_time": True,
            },
        ],
        condition=IfCondition(LaunchConfiguration("start_task_executor")),
    )

    # -------------------------------------------------------------------------
    # Startup sequencing
    # -------------------------------------------------------------------------

    # After move_group starts, wait 2 s then launch rviz + task_executor.
    final_launch = TimerAction(
        period=2.0,
        actions=[
            LogInfo(msg="[sim_mode] starting RViz and task_executor..."),
            rviz,
            task_executor,
        ],
    )
    final_after_mg = RegisterEventHandler(
        OnProcessStart(target_action=move_group, on_start=[final_launch])
    )

    # -------------------------------------------------------------------------
    # Return
    # -------------------------------------------------------------------------
    return LaunchDescription([
        LogInfo(msg="[sim_mode] Starting GP7 Gazebo simulation + MoveIt + task_executor..."),
        LogInfo(msg="[sim_mode] Startup order: Gazebo -> rsp -> spawn -> controllers -> move_group -> RViz/task_executor"),
        use_rviz_arg,
        start_task_executor_arg,
        use_sim_time_arg,
        x_arg,
        y_arg,
        z_arg,

        # Environment + Gazebo
        gazebo_resource_path,
        gazebo_model_path,
        gazebo_plugin_path,

        # Step 1: rsp + Gazebo
        rsp,
        gazebo,
        delayed_spawn,

        # Step 1 -> 2: controllers after spawn
        controllers_after_spawn,

        # Step 2 -> 3: wait for controllers then launch move_group
        wait_after_arm,
        move_group_after_controllers,

        # Step 3 -> 4+5: after move_group, launch rviz + task_executor
        final_after_mg,
    ])
