# gp7_moveit_config

**Purpose:** MoveIt 2 configuration (SRDF, kinematics, planning, controller mapping) and MoveIt launch files for the GP7.

**Key files:**
- `config/gp7_yaskawa.srdf` — semantic description.
- `config/moveit_controllers.yaml` — trajectory execution mapping (fake sim + Gazebo; default controller name `arm_controller`).
- `config/moveit_real_controllers.yaml` — real robot / MotoROS2-style mapping (adjust namespaces to match your controller).
- `launch/moveit_real.launch.py` — `move_group` + `robot_state_publisher` for hardware (RViz optional).
- `launch/moveit_fake_hardware.launch.py` — **offline validation:** `mock_components/GenericSystem` + `ros2_control` + MoveIt (no Gazebo, no MotoROS2). Uses `gp7_description/urdf/gp7_yaskawa_fake.urdf.xacro`.
- `scripts/verify_plan_execute.py` — plans and executes a small joint motion via `/move_action` (`moveit_msgs/action/MoveGroup`). **Regression script;** a cleaner equivalent lives in **`gp7_task_executor`** as `verify_fake_stack` (same stack checks).
- `legacy/` — archived configs not used by current launches (see `legacy/README.md`).

**Robot model:** Loaded from `gp7_description` (`urdf/gp7_yaskawa.urdf.xacro` for Gazebo; `gp7_yaskawa_fake.urdf.xacro` for mock hardware).

### Offline simulation (no real hardware)

Uses `gp7_description/urdf/gp7_yaskawa_fake.urdf.xacro` (`mock_components/GenericSystem`) + the same `arm_controller` name as Gazebo/real configs for consistency.

**Automated check** (from workspace root, after `colcon build` + `source install/setup.bash`):

```bash
./scripts/run_fake_sim_test.sh
```

The script runs **legacy** `verify_plan_execute.py`, then **`verify_fake_stack --repeat 2`**, then launches **`gp7_task_executor`** and calls **`move_to_joint_goal`**. If you see Fast DDS shared-memory errors, try another RMW or increase startup delays in the script.

**Manual:**

```bash
ros2 daemon stop   # recommended: clears stale action graph between runs
ros2 launch gp7_moveit_config moveit_fake_hardware.launch.py
# wait ~45 s for controllers + move_group, then:
ros2 run gp7_moveit_config verify_plan_execute.py
# or (equivalent smoke test):
ros2 run gp7_task_executor verify_fake_stack
```

MoveIt 2 exposes the motion planning action as **`/move_action`** (type `moveit_msgs/action/MoveGroup`; the node is still named `move_group`). The trajectory controller action is **`/arm_controller/follow_joint_trajectory`**.

The verify script uses a **MultiThreadedExecutor** so the MoveIt action client can complete (single-threaded `spin_until_future_complete` may deadlock).

### Gazebo Classic + MoveIt (simulation)

Use package **`gp7_gazebo_classic`** (e.g. `sim_moveit.launch.py`). That stack is separate from `moveit_fake_hardware.launch.py` and requires Gazebo Classic installed.
