# Phase 4 — canonical task layer (minimal)

## Goals delivered

- **`task_executor_node`** is a working node (not a stub): exposes **`move_to_joint_goal`** service.
- Execution path matches validated smoke tests: **`moveit_msgs/action/MoveGroup`** on **`/move_action`**.
- **`move_to_pose`** is **not** implemented (higher complexity / constraint setup); reserved for a later phase.
- **`gp7_task_executor_msgs`** holds **`MoveToJointGoal.srv`** (avoids CMake conflict between `rosidl` and `ament_python_install_package` in one package).

## Packages

| Package | Role |
|---------|------|
| `gp7_task_executor_msgs` | `MoveToJointGoal.srv` |
| `gp7_task_executor` | Python node, MoveIt helper `moveit_joint_goal.py`, `verify_fake_stack` |

## Interfaces

### Service (canonical task)

- **Name:** `/gp7_task_executor/move_to_joint_goal`
- **Type:** `gp7_task_executor_msgs/srv/MoveToJointGoal`

### Parameters (`task_executor_node`)

See `gp7_task_executor/config/task_executor.yaml` and package README.

### Topics / actions (unchanged from Phase 3 verify path)

- **Subscribes:** `/joint_states` (optional gate via `require_joint_states`)
- **Action clients:** `/move_action`, `/arm_controller/follow_joint_trajectory` (readiness check)

## Legacy verifier retirement (proposal only — **not** executed)

| Milestone | Criterion |
|-----------|-----------|
| **Keep** | Until CI and manual hardware runs routinely use `move_to_joint_goal` + `verify_fake_stack` with zero regressions across releases. |
| **Deprecate** | Announce `verify_plan_execute.py` as “regression-only” in release notes; keep installed 1–2 release cycles. |
| **Remove** | Only after: (1) no external docs/scripts reference it, (2) `run_fake_sim_test.sh` relies solely on `verify_fake_stack` + service call, (3) MotoROS2/real stack sign-off. |

Do **not** delete `gp7_moveit_config/scripts/verify_plan_execute.py` until the above are satisfied.

## Validation

Run from workspace (after `colcon build` + `source install/setup.bash`):

```bash
./scripts/run_fake_sim_test.sh
```

Expect: `VERIFY_LEGACY_EXIT=0`, `VERIFY_NEW_EXIT=0`, `TASK_SERVICE_EXIT=0`.

**Script order:** `moveit_fake_hardware` → sleep → **legacy verify** → **`verify_fake_stack --repeat 2`** (two goals in one process) → **then** launch `task_executor` → service call.

**Notes:**
- Starting `task_executor` *before* the MoveIt smoke tests can add a second `MoveGroup` client and contribute to flaky `MOTION_PLAN_INVALIDATED_BY_ENVIRONMENT_CHANGE` (-4) on some setups.
- Back-to-back **separate** `ros2 run` processes both using `MoveGroup` can hang on goal acceptance on some Fast DDS shared-memory setups; `--repeat 2` covers a second goal **inside one process** without that pattern.
- `RTPS_TRANSPORT_SHM` / `open_and_lock_file` messages: consider Cyclone DDS (`RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`) or tuning Fast DDS if tests are flaky.
