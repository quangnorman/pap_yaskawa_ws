"""Gazebo Classic + GP7 + MoveIt + simulated RGB-D camera + sim vision debug topics.

Adds a static ``gp7_sim_rgbd_camera`` model, a static box target, and TF chain:

  ``world`` → ``camera_link`` → ``camera_color_optical_frame``

Where ``camera_link`` is the camera mechanical/body frame and
``camera_color_optical_frame`` is the vision/image (optical) frame.

Hardware RealSense bringup stays in ``gp7_vision_bringup/vision_debug.launch.py`` — not used here.

Box target defaults (world top-face center):
  x=0.0, y=-0.7, z_top=0.05

Camera defaults (world → camera_link):
  x=0.0, y=-0.7, z=1.0 with roll=0, pitch=pi/2, yaw=-pi/2,
so the optical axis is vertical downward and centered over the box.

Usage::

    ros2 launch gp7_gazebo_classic sim_moveit_vision_rgbd.launch.py
    ros2 launch gp7_gazebo_classic sim_moveit_vision_rgbd.launch.py launch_vision:=false
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
    RegisterEventHandler,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EqualsSubstitution
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
import xacro


def generate_launch_description() -> LaunchDescription:
    desc_pkg = "gp7_description"
    bringup_pkg = "gp7_bringup"
    moveit_pkg = "gp7_moveit_config"
    gazebo_classic_pkg = "gp7_gazebo_classic"
    vision_bringup_pkg = "gp7_vision_bringup"

    desc_share = get_package_share_directory(desc_pkg)
    bringup_share = get_package_share_directory(bringup_pkg)
    gazebo_classic_share = get_package_share_directory(gazebo_classic_pkg)
    vision_bringup_share = get_package_share_directory(vision_bringup_pkg)

    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    controller_yaml_path = os.path.join(bringup_share, "config", "gp7_controller.yaml")
    initial_positions_path = os.path.join(desc_share, "config", "initial_positions.yaml")
    robot_description_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf")
    robot_description_raw = xacro.process_file(
        xacro_file,
        mappings={
            "controller_yaml": controller_yaml_path,
            "initial_positions_file": initial_positions_path,
            "robot_description_file": robot_description_file,
        },
    ).toxml()
    robot_description = re.sub(r"<!--.*?-->", "", robot_description_raw, flags=re.DOTALL)

    gazebo_launch_file = os.path.join(
        get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"
    )
    world_file = os.path.join(gazebo_classic_share, "worlds", "table.world")
    sim_camera_sdf = os.path.join(
        gazebo_classic_share, "models", "gp7_sim_rgbd_camera", "model.sdf"
    )
    sim_box_sdf = os.path.join(
        gazebo_classic_share, "models", "gp7_sim_target_box", "model.sdf"
    )
    vision_sim_launch = os.path.join(vision_bringup_share, "launch", "vision_sim_rgbd.launch.py")

    # -------------------------------------------------------------------------
    # Launch arguments (robot spawn + sim camera + vision)
    # -------------------------------------------------------------------------
    x_arg = DeclareLaunchArgument("x", default_value="0", description="Robot spawn X (world)")
    y_arg = DeclareLaunchArgument("y", default_value="0", description="Robot spawn Y (world)")
    z_arg = DeclareLaunchArgument("z", default_value="0.0", description="Robot spawn Z (base_link rests at world z=0.0; virtual_joint origin 0 0 0.33 places the URDF base_link 330 mm above world)")
    rviz_arg = DeclareLaunchArgument("rviz", default_value="true", description="Launch RViz")
    world_arg = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            'use_sim_time': 'true',
            'debug': 'false',
            'gui': 'true',
            'paused': 'true',
            'world' : world_file
        }.items()
    ) 

    sim_cam_x = DeclareLaunchArgument(
        "sim_cam_x",
        default_value="0.0",
        description="Sim RGB-D camera X in world (m); default 0.0",
    )
    sim_cam_y = DeclareLaunchArgument(
        "sim_cam_y",
        default_value="-0.7",
        description="Sim camera Y in world (m); REP-103 right = -Y → -1.0",
    )
    sim_cam_z = DeclareLaunchArgument(
        "sim_cam_z",
        default_value="1.0",
        description="Sim camera Z in world (m); height above ground",
    )
    sim_cam_roll = DeclareLaunchArgument(
        "sim_cam_roll",
        default_value="0.0",
        description="Sim camera mount roll (rad), world→camera_link static TF + spawn",
    )
    sim_cam_pitch = DeclareLaunchArgument(
        "sim_cam_pitch",
        default_value="1.5707963267948966",
        description="Sim camera mount pitch (rad); adjusted so optical Z points straight down",
    )
    sim_cam_yaw = DeclareLaunchArgument(
        "sim_cam_yaw",
        default_value="-1.5707963267948966",
        description="Sim camera mount yaw (rad); add +90deg right rotation while keeping optical Z downward",
    )

    # Box target reference is TOP-face center in the world frame.
    box_top_x = DeclareLaunchArgument(
        "box_top_x",
        default_value="0.0",
        description="Box target reference X in world: TOP-face center (m).",
    )
    box_top_y = DeclareLaunchArgument(
        "box_top_y",
        default_value="-0.7",
        description="Box target reference Y in world: TOP-face center (m).",
    )
    box_top_z = DeclareLaunchArgument(
        "box_top_z",
        default_value="0.05",
        description="Box target reference Z in world: TOP-face center (m).",
    )

    optical_roll = DeclareLaunchArgument(
        "optical_roll",
        default_value="-1.5707963267948966",
        description="camera_link → camera_color_optical_frame roll (rad)",
    )
    optical_pitch = DeclareLaunchArgument(
        "optical_pitch",
        default_value="0.0",
        description="camera_link → camera_color_optical_frame pitch (rad)",
    )
    optical_yaw = DeclareLaunchArgument(
        "optical_yaw",
        default_value="-1.5707963267948966",
        description="camera_link → camera_color_optical_frame yaw (rad)",
    )
    launch_vision_arg = DeclareLaunchArgument(
        "launch_vision",
        default_value="true",
        description="If true, start vision_sim_rgbd (depth debug on sim topics)",
    )

    rviz_enabled = LaunchConfiguration("rviz")
    world = LaunchConfiguration("world")
    launch_vision = LaunchConfiguration("launch_vision")

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
                os.path.join(gazebo_classic_share, "models"),
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

    # Spawn the static box target.
    # Required reference is the TOP-face center at (box_top_x, box_top_y, box_top_z).
    # The SDF model origin is the geometric center, so:
    #   z_center = z_top - height/2 = box_top_z - 0.05/2 = box_top_z - 0.025
    spawn_box_target = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        arguments=[
            "-entity",
            "gp7_sim_target_box",
            "-file",
            sim_box_sdf,
            "-x",
            LaunchConfiguration("box_top_x"),
            "-y",
            LaunchConfiguration("box_top_y"),
            "-z",
            PythonExpression([LaunchConfiguration("box_top_z"), " - 0.025"]),
            "-R",
            "0.0",
            "-P",
            "0.0",
            "-Y",
            "0.0",
        ],
    )

    delayed_spawn_box_target = TimerAction(period=3.0, actions=[spawn_box_target])

    spawn_sim_camera = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        arguments=[
            "-entity",
            "gp7_sim_rgbd_camera",
            "-file",
            sim_camera_sdf,
            "-x",
            LaunchConfiguration("box_top_x"),
            "-y",
            LaunchConfiguration("box_top_y"),
            "-z",
            LaunchConfiguration("sim_cam_z"),
            "-R",
            LaunchConfiguration("sim_cam_roll"),
            "-P",
            LaunchConfiguration("sim_cam_pitch"),
            "-Y",
            LaunchConfiguration("sim_cam_yaw"),
        ],
    )

    delayed_spawn_sim_camera = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_robot,
            on_exit=[TimerAction(period=5.0, actions=[spawn_sim_camera])],
        )
    )

    static_tf_world_to_camera = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_tf_world_to_camera_link",
        output="log",
        arguments=[
            "--frame-id",
            "world",
            "--child-frame-id",
            "camera_link",
            "--x",
            LaunchConfiguration("box_top_x"),
            "--y",
            LaunchConfiguration("box_top_y"),
            "--z",
            LaunchConfiguration("sim_cam_z"),
            "--roll",
            LaunchConfiguration("sim_cam_roll"),
            "--pitch",
            LaunchConfiguration("sim_cam_pitch"),
            "--yaw",
            LaunchConfiguration("sim_cam_yaw"),
        ],
    )

    static_tf_camera_to_optical = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_tf_camera_link_to_optical",
        output="log",
        arguments=[
            "--frame-id",
            "camera_link",
            "--child-frame-id",
            "camera_color_optical_frame",
            "--x",
            "0",
            "--y",
            "0",
            "--z",
            "0",
            "--roll",
            LaunchConfiguration("optical_roll"),
            "--pitch",
            LaunchConfiguration("optical_pitch"),
            "--yaw",
            LaunchConfiguration("optical_yaw"),
        ],
    )

    vision_sim_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(vision_sim_launch),
        condition=IfCondition(EqualsSubstitution(launch_vision, "true")),
    )

    start_tf_and_vision_after_camera = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_sim_camera,
            on_exit=[
                TimerAction(
                    period=1.0,
                    actions=[static_tf_world_to_camera, static_tf_camera_to_optical, vision_sim_include],
                )
            ],
        )
    )

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
            box_top_x,
            box_top_y,
            box_top_z,
            sim_cam_x,
            sim_cam_y,
            sim_cam_z,
            sim_cam_roll,
            sim_cam_pitch,
            sim_cam_yaw,
            optical_roll,
            optical_pitch,
            optical_yaw,
            launch_vision_arg,
            # gazebo,
            robot_state_publisher,
            delayed_spawn_robot,
            delayed_spawn_box_target,
            delayed_controller_loading,
            delayed_spawn_sim_camera,
            start_tf_and_vision_after_camera,
            start_wait_after_arm_spawner,
            move_group_after_controllers,
            rviz_after_move_group,
            # Publishes the world -> base_link transform (0, 0, 0.33).
            # This is now handled EXCLUSIVELY by the URDF virtual_joint.
            # This node is removed — keeping only URDF as the single source of truth.
            # Node(
            #     package="tf2_ros",
            #     executable="static_transform_publisher",
            #     name="static_tf_world_base_link",
            #     output="screen",
            #     arguments=[
            #         "--x", "0", "--y", "0", "--z", "0.33",
            #         "--roll", "0", "--pitch", "0", "--yaw", "0",
            #         "--frame-id", "world",
            #         "--child-frame-id", "base_link",
            #     ],
            # ),
            # static_tf_world_base_link,  # removed: world->base_link is now in URDF
        ]
    )
