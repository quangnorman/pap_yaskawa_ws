# gp7_task_executor

High-level task executor for the Yaskawa GP7 robot using MoveIt 2 (C++ node).

**Architecture:** Service-based task layer. All motion goes through MoveIt 2 `MoveGroupInterface`, not direct joint streaming.

**Interfaces:** Service definitions live in **`gp7_task_executor_msgs`**.

## Services

| Service | Type | Purpose |
|---------|------|---------|
| `/move_to_named_target` | `MoveToNamedTarget` | Move to a named SRDF group state (e.g., "home") |
| `/move_to_joint_target` | `MoveToJointTarget` | Move to a joint-space goal |
| `/move_to_pose_target` | `MoveToPoseTarget` | Move to a pose goal for the end-effector |

### Service Details

#### `/move_to_named_target`

**Request:**
- `target_name` (string): Name of the SRDF group state
- `execute` (bool): If true, plan and execute. If false, plan only.

**Response:**
- `success` (bool): True if succeeded
- `message` (string): Human-readable status message

#### `/move_to_joint_target`

**Request:**
- `joint_names` (string[]): Joint names (must match the planning group)
- `positions` (float64[]): Target positions (same length as joint_names)
- `execute` (bool): If true, plan and execute. If false, plan only.

**Response:**
- `success` (bool): True if succeeded
- `message` (string): Human-readable status message

#### `/move_to_pose_target`

**Request:**
- `pose` (geometry_msgs/Pose): Target pose (position and orientation)
- `frame_id` (string): Reference frame for the pose
- `execute` (bool): If true, plan and execute. If false, plan only.

**Response:**
- `success` (bool): True if succeeded
- `message` (string): Human-readable status message

## Joint Names (GP7)

The GP7 arm has 6 joints. Joint names from SRDF:

- `joint_s`
- `joint_l`
- `joint_u`
- `joint_r`
- `joint_b`
- `joint_t`

## Named Targets

Defined in `gp7_yaskawa.srdf` under the `arm` group:

- `home`: All joints at zero position

## Parameters

| Name | Default | Description |
|------|---------|-------------|
| `move_group_name` | `arm` | MoveIt planning group |
| `base_frame` | `world` | Base reference frame |
| `ee_link` | `tool0` | End-effector link |
| `planning_time` | `2.0` | Planning time (seconds) |
| `num_planning_attempts` | `5` | Number of planning attempts |
| `max_velocity_scaling_factor` | `0.5` | Velocity scaling (0-1) |
| `max_acceleration_scaling_factor` | `0.5` | Acceleration scaling (0-1) |

## Example CLI Calls

### Move to named target (home):

```bash
ros2 service call /move_to_named_target gp7_task_executor_msgs/srv/MoveToNamedTarget "{target_name: 'home', execute: true}"
```

### Move to joint target:

```bash
ros2 service call /move_to_joint_target gp7_task_executor_msgs/srv/MoveToJointTarget "{joint_names: ['joint_s','joint_l','joint_u','joint_r','joint_b','joint_t'], positions: [0.0, -1.0, 1.0, 0.0, 0.5, 0.0], execute: true}"
```

### Move to pose target:

```bash
ros2 service call /move_to_pose_target gp7_task_executor_msgs/srv/MoveToPoseTarget "{pose: {position: {x: 0.4, y: 0.0, z: 0.3}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}, frame_id: 'world', execute: true}"
```

### Plan only (no execution):

```bash
ros2 service call /move_to_joint_target gp7_task_executor_msgs/srv/MoveToJointTarget "{joint_names: ['joint_s','joint_l','joint_u','joint_r','joint_b','joint_t'], positions: [0.5, -0.5, 0.5, 0.5, 0.5, 0.5], execute: false}"
```

## Launch

Assumes MoveIt is already running. Start the task executor with:

```bash
ros2 launch gp7_task_executor task_executor.launch.py
```

With custom parameters:

```bash
ros2 launch gp7_task_executor task_executor.launch.py \
    move_group_name:=arm \
    planning_time:=5.0 \
    max_velocity_scaling_factor:=0.3
```

## Typical System Startup

```bash
# 1) Start Gazebo + MoveIt simulation
ros2 launch gp7_gazebo_classic sim_moveit.launch.py

# 2) Start task executor (in another terminal)
ros2 launch gp7_task_executor task_executor.launch.py

# 3) Send motion commands via services
```

## Build

```bash
cd ~/pap_yaskawa_ws
colcon build --packages-select gp7_task_executor_msgs gp7_task_executor
source install/setup.bash
```

## Dependencies

- ROS 2 Humble
- MoveIt 2
- gp7_task_executor_msgs
- geometry_msgs
