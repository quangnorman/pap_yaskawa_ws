import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    # -------------------------
    # Launch args
    # -------------------------
    gp7_desc_dir = get_package_share_directory("gp7_description")

    robot_ns = LaunchConfiguration("robot_ns")
    use_sim_time = LaunchConfiguration("use_sim_time")
    rviz_enable = LaunchConfiguration("rviz")
    publish_world_tf = LaunchConfiguration("publish_world_tf")

    # static TF params (world -> base_link) nếu bạn cần
    world_frame = LaunchConfiguration("world_frame")
    base_frame = LaunchConfiguration("base_frame")
    world_x = LaunchConfiguration("world_x")
    world_y = LaunchConfiguration("world_y")
    world_z = LaunchConfiguration("world_z")
    world_roll = LaunchConfiguration("world_roll")
    world_pitch = LaunchConfiguration("world_pitch")
    world_yaw = LaunchConfiguration("world_yaw")

    # ép kiểu bool chuẩn
    use_sim_time_bool = ParameterValue(use_sim_time, value_type=bool)

    # -------------------------
    # MoveIt config
    # -------------------------
    moveit_config = (
        MoveItConfigsBuilder("gp7", package_name="gp7_moveit_config")
        .robot_description(
            file_path=os.path.join(gp7_desc_dir, "urdf", "gp7_yaskawa.urdf.xacro")
        )
        .robot_description_semantic(file_path="config/gp7_yaskawa.srdf")
        .trajectory_execution(file_path="config/moveit_real_controllers.yaml")
        .to_moveit_configs()
    )

    # -------------------------
    # Remap joint_states: /joint_states -> /robot2/joint_states (robot_ns)
    # -------------------------
    # Ví dụ robot_ns=robot2 => /robot2/joint_states
    remap_js = [
        ("/joint_states", ["/", robot_ns, "/joint_states"]),
    ]

    # -------------------------
    # robot_state_publisher (TF từ URDF + joint_states)
    # -------------------------
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            {"use_sim_time": use_sim_time_bool},
        ],
        remappings=remap_js,
    )

    # -------------------------
    # OPTIONAL: static TF world -> base_link (bật nếu RViz cần world/map)
    # -------------------------
    static_world_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        output="screen",
        arguments=[
            world_x, world_y, world_z,
            world_roll, world_pitch, world_yaw,
            world_frame, base_frame
        ],
        condition=IfCondition(publish_world_tf),
    )

    # -------------------------
    # Move group
    # -------------------------
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": use_sim_time_bool},
            {"publish_robot_description_semantic": True},
        ],
        remappings=remap_js,
        arguments=["--ros-args", "--log-level", "info"],
    )

    # -------------------------
    # RViz
    # -------------------------
    rviz_config = os.path.join(
        get_package_share_directory("gp7_moveit_config"),
        "config",
        "moveit.rviz",
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
            {"use_sim_time": use_sim_time_bool},
        ],
        condition=IfCondition(rviz_enable),
    )

    # -------------------------
    # LaunchDescription
    # -------------------------
    ld = LaunchDescription()

    ld.add_action(DeclareLaunchArgument(
        "robot_ns",
        default_value="robot2",
        description="Namespace của robot thật (vd: robot2 => /robot2/joint_states)"
    ))
    ld.add_action(DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Robot thật: phải để false"
    ))
    ld.add_action(DeclareLaunchArgument(
        "rviz",
        default_value="true",
        description="Bật/tắt RViz"
    ))

    # Static TF world->base_link (tắt mặc định)
    ld.add_action(DeclareLaunchArgument(
        "publish_world_tf",
        default_value="false",
        description="Bật static TF world->base_link nếu RViz Fixed Frame là world/map"
    ))
    ld.add_action(DeclareLaunchArgument("world_frame", default_value="world"))
    ld.add_action(DeclareLaunchArgument("base_frame", default_value="base_link"))
    ld.add_action(DeclareLaunchArgument("world_x", default_value="0"))
    ld.add_action(DeclareLaunchArgument("world_y", default_value="0"))
    ld.add_action(DeclareLaunchArgument("world_z", default_value="0"))
    ld.add_action(DeclareLaunchArgument("world_roll", default_value="0"))
    ld.add_action(DeclareLaunchArgument("world_pitch", default_value="0"))
    ld.add_action(DeclareLaunchArgument("world_yaw", default_value="0"))

    ld.add_action(robot_state_publisher_node)
    ld.add_action(static_world_tf_node)
    ld.add_action(move_group_node)
    ld.add_action(rviz_node)

    return ld