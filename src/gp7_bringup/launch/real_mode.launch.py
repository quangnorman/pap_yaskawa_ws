"""Launch file to bring up the real Yaskawa GP7 with MoveIt, RViz, and task_executor.

STARTUP ORDER
=============
1. yaskawa_robot_controller / servo_on1
   - MotoROS2 servo-on executable.  Must run before any motion is attempted.
   - Blocks until complete (robot enters servo-ready state).

2. robot_state_publisher  [3 s after servo_on exits]
   - Publishes the TF tree from /robot_description.
   - Remaps /joint_states -> /robot1/joint_states so it re-publishes the
     real joint states under the canonical topic that MoveIt listens to.

3. move_group  [5 s after robot_state_publisher starts]
   - MoveIt planning node.  Also remaps /joint_states -> /robot1/joint_states.
   - Uses the real controller config (moveit_controllers_real.yaml)
     so planned trajectories are sent to /robot1/follow_joint_trajectory.

4. rviz  [2 s after move_group starts]
   - Visualises the robot model, planning scene, and planned paths.

5. task_executor_node  [2 s after move_group starts]
   - High-level task executor (named targets, joint targets, pose targets, sequences).
   - Uses base_link as the planning reference frame (no world offset).

REQUIREMENTS (run separately / outside this launch)
==================================================
- ROS_DOMAIN_ID must be set to 1 before launching:  export ROS_DOMAIN_ID=1
- micro-ros-agent must be running to bridge ESP32 firmware to ROS 2:
    docker run --rm --net=host -it microros/micro-ros-agent:humble serial --dev /dev/ttyUSB0
- The MotoROS2 driver on the YRC1000micro controller must be reachable on the
  configured network / serial interface; this launch assumes the driver is
  already running and exposing:
      /robot1/joint_states
      /robot1/follow_joint_trajectory
      /robot1/robot_status
- servo_on1 is the MotoROS2 servo-on helper from the yaskawa_robot_controller
  package; build that package before launching.
"""

import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, LogInfo, RegisterEventHandler, TimerAction
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description() -> LaunchDescription:
    # -------------------------------------------------------------------------
    # Packages
    # -------------------------------------------------------------------------
    desc_pkg = "gp7_description"
    moveit_pkg = "gp7_moveit_config"
    executor_pkg = "gp7_task_executor"

    desc_share = get_package_share_directory(desc_pkg)
    moveit_share = get_package_share_directory(moveit_pkg)
    executor_share = get_package_share_directory(executor_pkg)

    # -------------------------------------------------------------------------
    # Launch arguments
    # -------------------------------------------------------------------------
    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz alongside move_group and task_executor",
    )
    start_task_executor_arg = DeclareLaunchArgument(
        "start_task_executor",
        default_value="true",
        description="Launch the gp7_task_executor node",
    )

    # -------------------------------------------------------------------------
    # Robot description — process xacro manually (proven pattern from sim_moveit).
    # -------------------------------------------------------------------------
    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    robot_description = xacro.process_file(xacro_file).toxml()

    # -------------------------------------------------------------------------
    # MoveIt configuration
    #
    # NOTE: moveit_configs_utils.to_dict() auto-discovers ALL installed planner
    # plugins on the system (ompl, pilz, chomp).  We build the config with
    # planning_pipelines('ompl') so the OMPL section is populated, then strip the
    # pilz_industrial_motion_planner and chomp top-level keys so only OMPL is
    # available at runtime.  This prevents CHOMP or Pilz from accidentally being
    # selected by RViz or move_group.
    # -------------------------------------------------------------------------
    controller_yaml_path = os.path.join(moveit_share, "config", "moveit_controllers_real.yaml")

    moveit_config = (
        MoveItConfigsBuilder("gp7_yaskawa", package_name=moveit_pkg)
        .robot_description(file_path=os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro"))
        .robot_description_semantic(
            file_path=os.path.join(moveit_share, "config", "gp7_yaskawa.srdf")
        )
        .robot_description_kinematics(
            file_path=os.path.join(moveit_share, "config", "kinematics.yaml")
        )
        .trajectory_execution(file_path=controller_yaml_path)
        .planning_pipelines("ompl")
        .to_moveit_configs()
    )
    moveit_params = moveit_config.to_dict()

    # Strip auto-discovered plugins that are NOT needed for real robot mode.
    # These keys are added by to_dict() because the packages exist on the system,
    # but we only want OMPL.
    moveit_params.pop("pilz_industrial_motion_planner", None)
    moveit_params.pop("chomp", None)
    # Ensure planning_pipelines only contains 'ompl' (remove chomp/pilz if present).
    if "planning_pipelines" in moveit_params:
        moveit_params["planning_pipelines"] = ["ompl"]

    moveit_params["use_sim_time"] = False

    # -------------------------------------------------------------------------
    # DEBUG: log key config values at launch time
    # -------------------------------------------------------------------------
    debug_log = LogInfo(msg=(
        f"[real_mode] DEBUG — robot_description length: {len(robot_description)} chars | "
        f"planning_pipelines: {moveit_params.get('planning_pipelines')} | "
        f"controller_yaml: {controller_yaml_path}"
    ))

    # -------------------------------------------------------------------------
    # Step 1: servo_on1 — MotoROS2 servo-on helper
    # Blocks until the robot reaches servo-ready state.
    # -------------------------------------------------------------------------
    servo_on = ExecuteProcess(
        cmd=["ros2", "run", "yaskawa_robot_controller", "servo_on1"],
        output="screen",
        shell=False,
    )

    # -------------------------------------------------------------------------
    # Step 2: robot_state_publisher
    # Remaps /joint_states -> /robot1/joint_states so the real hardware joint
    # states are available on the canonical topic MoveIt listens to.
    # -------------------------------------------------------------------------
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": robot_description},
            {"use_sim_time": False},
        ],
        remappings=[("/joint_states", "/robot1/joint_states")],
    )

    # -------------------------------------------------------------------------
    # Step 3: move_group
    # Remaps /joint_states -> /robot1/joint_states so MoveIt reads the real
    # robot state.  Uses moveit_controllers_real.yaml which points trajectories
    # at /robot1/follow_joint_trajectory.
    # -------------------------------------------------------------------------
    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        name="move_group",
        output="screen",
        parameters=[
            moveit_params,
            {"robot_description": robot_description},
            {"publish_robot_description_semantic": True},
            {"use_sim_time": False},
            # Force OMPL-only pipeline and explicit request adapters so every
            # trajectory contains velocity + time_from_start data.
            {"planning_pipelines": ["ompl"]},
            {"default_planning_pipeline": "ompl"},
            {
                "ompl": {
                    "planning_plugin": "ompl_interface/OMPLPlanner",
                    "request_adapters": (
                        "default_planner_request_adapters/AddTimeOptimalParameterization "
                        "default_planner_request_adapters/FixWorkspaceBounds "
                        "default_planner_request_adapters/FixStartStateBounds "
                        "default_planner_request_adapters/FixStartStateCollision "
                        "default_planner_request_adapters/FixStartStatePathConstraints"
                    ),
                }
            },
            {"default_velocity_scaling_factor": 0.5},
            {"default_acceleration_scaling_factor": 0.5},
        ],
        remappings=[("/joint_states", "/robot1/joint_states")],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # -------------------------------------------------------------------------
    # Step 4: RViz
    # -------------------------------------------------------------------------
    rviz_config = os.path.join(moveit_share, "config", "moveit.rviz")
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
            {
                "planning_pipelines": ["ompl"],
                "default_planning_pipeline": "ompl",
                "default_planner_request_adapters": (
                    "default_planner_request_adapters/AddTimeOptimalParameterization "
                    "default_planner_request_adapters/FixWorkspaceBounds "
                    "default_planner_request_adapters/FixStartStateBounds "
                    "default_planner_request_adapters/FixStartStateCollision "
                    "default_planner_request_adapters/FixStartStatePathConstraints"
                ),
                "default_velocity_scaling_factor": 0.5,
                "default_acceleration_scaling_factor": 0.5,
                "use_sim_time": False,
            },
        ],
        condition=IfCondition(LaunchConfiguration("use_rviz")),
    )

    # -------------------------------------------------------------------------
    # Step 5: task_executor_node
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
                "use_sim_time": False,
            },
        ],
        condition=IfCondition(LaunchConfiguration("start_task_executor")),
    )

    # -------------------------------------------------------------------------
    # Step 6: trajectory_debug_node
    # Subscribes to /execute_trajectory (the internal MoveIt -> controller topic)
    # and prints every trajectory point so we can confirm velocities are present.
    # Remove this node once the robot consistently executes trajectories.
    # -------------------------------------------------------------------------
    trajectory_debug = Node(
        package="gp7_bringup",
        executable="trajectory_debug_node",
        name="trajectory_debug_node",
        output="screen",
        condition=IfCondition(LaunchConfiguration("start_task_executor")),
    )

    # -------------------------------------------------------------------------
    # Sequenced startup
    # -------------------------------------------------------------------------

    # servo_on exits -> wait 3 s -> launch rsp
    rsp_launch = TimerAction(period=3.0, actions=[rsp])
    rsp_on_servo_exit = RegisterEventHandler(
        OnProcessExit(target_action=servo_on, on_exit=[rsp_launch])
    )

    # rsp starts -> wait 5 s -> launch move_group
    mg_launch = TimerAction(
        period=5.0,
        actions=[
            LogInfo(msg="[real_mode] starting move_group..."),
            move_group,
        ],
    )
    mg_on_rsp_start = RegisterEventHandler(
        OnProcessStart(target_action=rsp, on_start=[mg_launch])
    )

    # move_group starts -> wait 2 s -> launch rviz + task_executor + debug
    final_launch = TimerAction(
        period=2.0,
        actions=[
            LogInfo(msg="[real_mode] starting RViz, task_executor, and trajectory_debug..."),
            rviz,
            task_executor,
            trajectory_debug,
        ],
    )
    final_on_mg_start = RegisterEventHandler(
        OnProcessStart(target_action=move_group, on_start=[final_launch])
    )

    # -------------------------------------------------------------------------
    # Return
    # -------------------------------------------------------------------------
    return LaunchDescription([
        LogInfo(msg="[real_mode] Starting GP7 real robot bringup..."),
        LogInfo(msg="[real_mode] Startup order: servo_on1 -> rsp -> move_group -> RViz/task_executor"),
        use_rviz_arg,
        start_task_executor_arg,
        debug_log,

        # Step 1: servo_on1
        servo_on,

        # Step 1 -> 2: after servo_on exits, launch rsp after 3 s
        rsp_on_servo_exit,

        # Step 2 -> 3: after rsp starts, launch move_group after 5 s
        mg_on_rsp_start,

        # Step 3 -> 4+5+6: after move_group starts, launch rviz + executor + debug after 2 s
        final_on_mg_start,
    ])
