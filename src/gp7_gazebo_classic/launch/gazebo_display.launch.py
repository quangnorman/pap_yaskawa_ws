import os
import re
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, SetEnvironmentVariable, DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

import xacro

def generate_launch_description() -> LaunchDescription:
    desc_pkg = "gp7_description"
    bringup_pkg = "gp7_bringup"
    gazebo_classic_pkg = "gp7_gazebo_classic"

    desc_share = get_package_share_directory(desc_pkg)
    bringup_share = get_package_share_directory(bringup_pkg)
    gazebo_classic_share = get_package_share_directory(gazebo_classic_pkg)
    controller_share = os.path.join(bringup_share, "config", "gp7_controller.yaml")
    initial_positions_path = os.path.join(desc_share, "config", "initial_positions.yaml")

    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    controller_share = os.path.join(bringup_share, "config", "gp7_controller.yaml")
    initial_positions_path = os.path.join(desc_share, "config", "initial_positions.yaml")
    robot_description_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf")
    robot_description_raw = xacro.process_file(
        xacro_file,
        mappings={
            "controller_yaml": controller_share,
            "initial_positions_file": initial_positions_path,
            "robot_description_file": robot_description_file,
        },
    ).toxml()
    # gazebo_ros2_control passes robot_description as a CLI --param override.
    # XML comments that contain "--" can break rcl argument parsing in Humble.
    robot_description = re.sub(r"<!--.*?-->", "", robot_description_raw, flags=re.DOTALL)
    gazebo_launch_file = os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    # Keep display launch lightweight/stable: use Gazebo's default empty world.
    # world_test1 includes optional custom plugins that can fail on machines
    # where those plugin libraries are not present, preventing controller bringup.
    # world_file = "/usr/share/gazebo-11/worlds/empty.world"

    world_file = os.path.join(gazebo_classic_share, "worlds", "table.world")

    x_arg = DeclareLaunchArgument('x', default_value='0', description='X position')
    y_arg = DeclareLaunchArgument('y', default_value='0', description='Y position')
    z_arg = DeclareLaunchArgument('z', default_value='0.33', description='Robot spawn Z (base_link rests 0.33 m above world ground)')
    
    # --- ENV Gazebo ---
    gazebo_resource_path = SetEnvironmentVariable(
        name="GAZEBO_RESOURCE_PATH",
        value=":".join([
            "/usr/share/gazebo-11",
            str(Path(desc_share).parent.resolve()),
            desc_share,
            gazebo_classic_share,
            bringup_share,
            os.environ.get("GAZEBO_RESOURCE_PATH", "")
        ])
    )

    gazebo_model_path = SetEnvironmentVariable(
        name="GAZEBO_MODEL_PATH",
        value=":".join([
            str(Path(desc_share).parent.resolve()),
            os.path.join(desc_share, "models"),
            os.path.expanduser("~/.gazebo/models"),
            os.environ.get("GAZEBO_MODEL_PATH", "")
        ])
    )

    gazebo_plugin_path = SetEnvironmentVariable(
        name="GAZEBO_PLUGIN_PATH",
        value=":".join([
            "/opt/ros/humble/lib",
            os.path.normpath(os.path.join(gazebo_classic_share, "..", "..", "lib")),
        ])
    )


    def spawn_entity_node(name, model_path, x, y, z):
        return Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', name, '-file', model_path, '-x', str(x), '-y', str(y), '-z', str(z)],
            output='screen'
        )

    spawn_conveyor = spawn_entity_node('conveyor_belt', os.path.join(desc_share, 'models', 'conveyor_belt', 'model.sdf'), 0.0, 2, 0.0)


    node_robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{
        'robot_description': robot_description,
        'use_sim_time': True
    }]
)
    
    # Include Gazebo launch file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            'use_sim_time': 'true',
            'debug': 'false',
            'gui': 'true',
            'paused': 'true',
            'world' : world_file
        }.items()
    ) 

    spawn_the_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'gp7_yaskawa',
            '-topic', 'robot_description',
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z'),
        ],
        output='screen',
    )

    control_node = Node(
    package="controller_manager",
    executable="ros2_control_node",
    parameters=[
        {'robot_description': robot_description},
        controller_share
    ],
    output="screen",
)

    joint_state_broadcaster_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=[
        "joint_state_broadcaster",
        "--controller-manager",
        "/controller_manager",
        "--controller-manager-timeout",
        "120",
    ],
)
    
    load_arm_controller = Node(
    package="controller_manager",
    executable="spawner",
    arguments=[
        "arm_controller",
        "--controller-manager",
        "/controller_manager",
        "--controller-manager-timeout",
        "120",
    ],
)



    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", os.path.join(bringup_share, "rviz", "rviz.rviz")],
        output="screen",
    )

    delayed_spawn_robot = TimerAction(
        period=3.0,
        actions=[spawn_the_robot]
    )

    delayed_controller_loading = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_the_robot,
            on_exit=[
                TimerAction(period=2.0, actions=[joint_state_broadcaster_spawner]),
                TimerAction(period=3.0, actions=[load_arm_controller]),
            ],
        )
    )

    # Publishes the world -> base_link transform (0, 0, 0.33).
    # No longer needed — the URDF virtual_joint is removed.
    # base_link is spawned directly in Gazebo at z=0.33 via spawn_entity.py -z argument.
    # static_tf_world_base_link = Node(
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
    # )

    return LaunchDescription([
        gazebo_resource_path,
        gazebo_model_path,
        gazebo_plugin_path,
        gazebo,
        x_arg,y_arg,z_arg,
        # control_node,
        node_robot_state_publisher,
        # static_tf_world_base_link,  # removed: no world frame; base_link spawned at z=0.33 in Gazebo
        delayed_spawn_robot,
        delayed_controller_loading,
        # spawn_conveyor,
        # rviz_node,
    ])