"""Top-level launch dispatcher for the gp7_yaskawa robot bringup.

ARCHITECTURE
============
This file is the single entry point for all bringup scenarios.  It delegates
to the appropriate backend launch file based on the `mode` argument:

  main.launch.py mode:=sim
    -> sim_mode.launch.py
       Gazebo Classic + ros2_control sim controllers
       + MoveIt (OMPL) + RViz + gp7_task_executor

  main.launch.py mode:=real
    -> real_mode.launch.py
       MotoROS2 (real YRC1000micro) + MoveIt (OMPL)
       + RViz + gp7_task_executor + trajectory_debug_node

USAGE
=====
  # Simulation mode (default)
  ros2 launch gp7_bringup main.launch.py mode:=sim

  # Real robot mode
  ros2 launch gp7_bringup main.launch.py mode:=real

  # Forward additional arguments
  ros2 launch gp7_bringup main.launch.py mode:=sim use_rviz:=false start_task_executor:=true
  ros2 launch gp7_bringup main.launch.py mode:=real use_rviz:=true start_task_executor:=true

NOTES
=====
- Both backends share the same gp7_task_executor configuration (waypoints,
  planning parameters) and the same MoveIt planning group ("arm").
- Only one backend runs at a time; use_sim_time and ROS_DOMAIN_ID must be
  set externally as needed.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from ament_index_python.packages import get_package_share_directory


def generate_launch_description() -> LaunchDescription:
    bringup_pkg = "gp7_bringup"
    bringup_share = get_package_share_directory(bringup_pkg)

    # -------------------------------------------------------------------------
    # Top-level arguments
    # -------------------------------------------------------------------------
    mode_arg = DeclareLaunchArgument(
        "mode",
        default_value="sim",
        description=(
            "Backend mode: 'sim' (Gazebo simulation) or 'real' (Yaskawa hardware). "
            "Only one backend runs at a time."
        ),
    )
    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Forward to backend launch file: launch RViz",
    )
    start_task_executor_arg = DeclareLaunchArgument(
        "start_task_executor",
        default_value="true",
        description="Forward to backend launch file: launch gp7_task_executor node",
    )

    mode = LaunchConfiguration("mode")
    use_rviz = LaunchConfiguration("use_rviz")
    start_task_executor = LaunchConfiguration("start_task_executor")

    sim_condition = IfCondition(PythonExpression(["'", mode, "' == 'sim'"]))
    real_condition = IfCondition(PythonExpression(["'", mode, "' == 'real'"]))

    # -------------------------------------------------------------------------
    # Backend launch inclusions
    # -------------------------------------------------------------------------
    sim_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [bringup_share, "/launch/sim_mode.launch.py"]
        ),
        launch_arguments={
            "use_rviz": use_rviz,
            "start_task_executor": start_task_executor,
        }.items(),
        condition=sim_condition,
    )

    real_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [bringup_share, "/launch/real_mode.launch.py"]
        ),
        launch_arguments={
            "use_rviz": use_rviz,
            "start_task_executor": start_task_executor,
        }.items(),
        condition=real_condition,
    )

    # -------------------------------------------------------------------------
    # Return
    # -------------------------------------------------------------------------
    return LaunchDescription([
        LogInfo(msg="[main] ============================================================"),
        LogInfo(
            msg="[main] Starting GP7 bringup — use 'mode:=sim' or 'mode:=real'"
        ),
        LogInfo(msg="[main] ============================================================"),
        LogInfo(
            msg="[main] Starting SIM mode (Gazebo + MoveIt + task_executor)",
            condition=sim_condition,
        ),
        LogInfo(
            msg="[main] Starting REAL mode (MotoROS2 + MoveIt + task_executor)",
            condition=real_condition,
        ),
        mode_arg,
        use_rviz_arg,
        start_task_executor_arg,

        # Dispatch
        sim_ld,
        real_ld,
    ])
