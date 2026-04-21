import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, SetEnvironmentVariable, DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from moveit_configs_utils import MoveItConfigsBuilder
import xacro

def generate_launch_description() -> LaunchDescription:
    desc_pkg = "gp7_description"
    bringup_pkg = "gp7_bringup"
    moveit_pkg = "gp7_moveit_config"
    gazebo_classic_pkg = "gp7_gazebo_classic"

    desc_share = get_package_share_directory(desc_pkg)
    bringup_share = get_package_share_directory(bringup_pkg)
    gazebo_classic_share = get_package_share_directory(gazebo_classic_pkg)
    controller_share = os.path.join(bringup_share, "config", "gp7_controller.yaml")

    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    robot_description = xacro.process_file(xacro_file).toxml()
    gazebo_launch_file = os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    world_file = os.path.join(gazebo_classic_share, "worlds", "world_test1.world")


    x_arg = DeclareLaunchArgument('x', default_value='0', description='X position')
    y_arg = DeclareLaunchArgument('y', default_value='0', description='Y position')
    z_arg = DeclareLaunchArgument('z', default_value='0', description='Z position')
    
    # --- ENV Gazebo ---
    gazebo_resource_path = SetEnvironmentVariable(
        name="GAZEBO_RESOURCE_PATH",
        value=":".join([
            "/usr/share/gazebo-11",
            str(Path(desc_share).parent.resolve()),
            desc_share,
            gazebo_classic_share,
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
            '-z', LaunchConfiguration('z')
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
    arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
)
    
    load_arm_controller = Node(
    package="controller_manager",
    executable="spawner",
    arguments=["arm_controller", "--controller-manager", "/controller_manager"],
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
        OnProcessStart(
            target_action=spawn_the_robot,
            on_start=[
                TimerAction(period=2.0, actions=[joint_state_broadcaster_spawner]),
                TimerAction(period=3.0, actions=[load_arm_controller]),
            ],
        )
    )


    # -------------------------------------------------------------------------
    # MoveIt configuration
    # -------------------------------------------------------------------------
    moveit_config = (
        MoveItConfigsBuilder("gp7", package_name=moveit_pkg)
        .robot_description(
            file_path=os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
        )
        .robot_description_semantic(file_path="config/gp7_yaskawa.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )

    moveit_parameters = moveit_config.to_dict()
    moveit_parameters.update({"use_sim_time": True})

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_parameters,
            {"use_sim_time": True},
            {"publish_robot_description_semantic": True},
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    move_group_after_arm_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=load_arm_controller,
            on_exit=[move_group],
        )
    )


    return LaunchDescription([
        gazebo_resource_path,
        gazebo_model_path,
        gazebo_plugin_path,
        gazebo,
        x_arg,y_arg,z_arg,
        # control_node,
        node_robot_state_publisher,
        delayed_spawn_robot,
        delayed_controller_loading,
        move_group_after_arm_controller,
        
        # spawn_conveyor,
        # rviz_node,
    ])