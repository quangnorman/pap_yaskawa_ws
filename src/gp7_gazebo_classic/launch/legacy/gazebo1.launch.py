import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, SetEnvironmentVariable
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description() -> LaunchDescription:
    desc_pkg = "gp7_description"
    bringup_pkg = "gp7_bringup"

    desc_share = get_package_share_directory(desc_pkg)
    bringup_share = get_package_share_directory(bringup_pkg)
    controller_share = os.path.join(bringup_share, "config", "gp7_controller.yaml")

    xacro_file = os.path.join(desc_share, "urdf", "gp7_yaskawa.urdf.xacro")
    robot_description = xacro.process_file(xacro_file).toxml()


    gazebo_resource_path = SetEnvironmentVariable(
        name="GAZEBO_MODEL_PATH",
        value=[str(Path(desc_share).parent.resolve())],
    )

    gazebo_model_path = SetEnvironmentVariable(
        name="GAZEBO_MODEL_PATH",
        value=[os.path.join(desc_share, "models")]
    )

    node_robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{
        'robot_description': robot_description,
        'use_sim_time': True
    }]
)
    gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(get_package_share_directory('gazebo_ros'), 'launch'),
        '/gazebo.launch.py'
    ]),
)   
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "robot_description",
            "-entity",
            "robot_yaskawa",
        ],
        output="screen",
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

    

    load_joint_state_controller_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_state_broadcaster_spawner],
        )
    )

    load_arm_controller_after_joint_state = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[load_arm_controller],
        )
    )

    return LaunchDescription([
        gazebo_resource_path,
        gazebo,
        control_node,
        node_robot_state_publisher,
        spawn_entity,
        gazebo_model_path,
        load_joint_state_controller_after_spawn,
        load_arm_controller_after_joint_state,
        #rviz_node,
    ])