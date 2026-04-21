# gp7_task_executor_msgs

ROS 2 service definitions for **`gp7_task_executor`**.

## Services

| Type | Purpose |
|------|---------|
| `srv/MoveToNamedTarget` | Move to a named SRDF group state (e.g., "home") |
| `srv/MoveToJointTarget` | Move to a joint-space goal |
| `srv/MoveToPoseTarget` | Move to a pose goal for the end-effector |

## Usage

These services are used by `gp7_task_executor` to command the GP7 robot through MoveIt 2.

## Build

```bash
colcon build --packages-select gp7_task_executor_msgs
source install/setup.bash
```

After building, the service types are available:

```bash
ros2 pkg list | grep gp7_task_executor_msgs
ros2 srv show gp7_task_executor_msgs/srv/MoveToNamedTarget
ros2 srv show gp7_task_executor_msgs/srv/MoveToJointTarget
ros2 srv show gp7_task_executor_msgs/srv/MoveToPoseTarget
```
