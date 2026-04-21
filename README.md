# pap_yaskawa_ws

ROS 2 **Humble** workspace for a **Yaskawa GP7** arm with **MoveIt 2**, **Gazebo Classic** simulation, **ros2_control**, and a **task layer** (`gp7_task_executor`) for joint and Cartesian motion through MoveIt (not direct unsafe joint streaming on hardware).

## Goals

- Pick-and-place style workflows with RGB-D / perception (future)
- Safe trajectory execution via **MoveIt 2** and **MotoROS2** on real hardware
- Reinforcement learning only for high-level planning parameters (not direct joint commands on hardware)

## Packages

| Package | Role |
|--------|------|
| [`gp7_description`](src/gp7_description/README.md) | Robot URDF/Xacro, `ros2_control` macros, TF frames (`world`, `base_link`, `tool0`, …) |
| [`gp7_moveit_config`](src/gp7_moveit_config/README.md) | MoveIt 2 config, `move_group`, fake-hardware and real launch entry points |
| [`gp7_bringup`](src/gp7_bringup/README.md) | Controller YAML, display launch (RViz + joint GUI) |
| [`gp7_gazebo_classic`](src/gp7_gazebo_classic/README.md) | Gazebo Classic simulation, `sim_moveit.launch.py`, `gazebo_display.launch.py` |
| [`gp7_task_executor_msgs`](src/gp7_task_executor_msgs/README.md) | Service definitions (`MoveToJointGoal`, `MoveToPose`, `GetCurrentPose`, …) |
| [`gp7_task_executor`](src/gp7_task_executor/README.md) | `task_executor_node`: MoveIt-based services; demo nodes and verification |
| [`gp7_vision_pipeline`](src/gp7_vision_pipeline/README.md) | D435 perception (M2: depth debug; future YOLO + 3D box in `base_link`; no motion) |
| [`gp7_vision_bringup`](src/gp7_vision_bringup/README.md) | RealSense launch, static TF `base_link`→`camera_link`, vision debug / bringup launches |
| [`gp7_handeye_calibration`](src/gp7_handeye_calibration/README.md) | Hand–eye calibration scaffold (empty launch + config skeleton) |

## Prerequisites

- Ubuntu 22.04, **ROS 2 Humble**
- Colcon workspace at this path (or clone and build elsewhere)
- For simulation: Gazebo Classic 11, MoveIt 2, `ros2_control` stack as used by the packages above
- For D435 bringup: `ros-humble-realsense2-camera` (see [`src/gp7_vision_bringup/README.md`](src/gp7_vision_bringup/README.md))

## Build

```bash
cd /path/to/pap_yaskawa_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Build a subset:

```bash
colcon build --packages-select gp7_task_executor gp7_task_executor_msgs --symlink-install
```

Vision packages only:

```bash
colcon build --packages-select gp7_vision_pipeline gp7_vision_bringup gp7_handeye_calibration --symlink-install
```

**Vision (Milestone 2):** with a D435 connected, `ros2 launch gp7_vision_bringup vision_debug.launch.py` — expect RGB OK + center depth logs. Plan and contracts: [`docs/VISION_ARCHITECTURE.md`](docs/VISION_ARCHITECTURE.md).

## Common launch flows

**Simulation + MoveIt (recommended baseline for Gazebo demos)**

```bash
ros2 launch gp7_gazebo_classic sim_moveit.launch.py
```

**Simulation + MoveIt + simulated RGB-D camera + vision debug (Gazebo topics, not RealSense)**

```bash
ros2 launch gp7_gazebo_classic sim_moveit_vision_rgbd.launch.py
```

**Gazebo display only (reference spawn + controllers)**

```bash
ros2 launch gp7_gazebo_classic gazebo_display.launch.py
```

**Fake hardware + MoveIt (CI / no Gazebo)**

```bash
ros2 launch gp7_moveit_config moveit_fake_hardware.launch.py
```

**Task layer (services: joint goals, pose goals, current pose)**

```bash
ros2 launch gp7_task_executor task_executor.launch.py
```

Parameters default from `gp7_task_executor/config/task_executor.yaml`.

**Vision stack (perception infrastructure; no robot motion from vision nodes)**

```bash
# Headless: camera + static TF + pipeline placeholder
ros2 launch gp7_vision_bringup vision_bringup.launch.py

# Debug: + depth sanity node + optional RViz
ros2 launch gp7_vision_bringup vision_debug.launch.py
```

## Task layer and demos

See **[`src/gp7_task_executor/README.md`](src/gp7_task_executor/README.md)** for:

- `move_to_joint_goal`, `move_to_pose`, `get_current_pose`
- Joint-space demo loop, Cartesian demos, base-frame joint + pose verification
- Fake-hardware verification scripts
P
## Documentation in this repo

- [`docs/VISION_ARCHITECTURE.md`](docs/VISION_ARCHITECTURE.md) — D435 perception plan, topics/TF/output contracts, milestones
- [`docs/`](docs/) — phase reports, migration notes, cleanup summaries (where present)

## Constraints (project policy)

- **ROS 2 Humble** only for this workspace
- Real robot: motion through **MoveIt 2** and **MotoROS2**; no direct low-level joint streaming for production safety
- Prefer explicit TF frames: `world`, `base_link`, `tool0`, camera frames as documented in `gp7_description`
- Gazebo Classic is isolated under **`gp7_gazebo_classic`** for future migration (e.g. `ros_gz`)

## License

Per-package `package.xml` / upstream notices (commonly Apache-2.0 where stated).
