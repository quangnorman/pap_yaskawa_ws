# Phase 3 migration summary

## New package: `gp7_task_executor`

- **Type:** `ament_cmake` + `ament_python_install_package` (Python modules under `gp7_task_executor/gp7_task_executor/`).
- **Executables:** `scripts/task_executor_node` and `scripts/verify_fake_stack` are installed to `lib/gp7_task_executor/` via CMake `install(PROGRAMS ...)` (same pattern as `gp7_moveit_config/verify_plan_execute.py`).
- **Nodes / CLIs:**
  - `task_executor_node` — minimal stub; parameters `planning_frame`, `move_group_action`; **does not send motion.**
  - `verify_fake_stack` — minimal MoveIt + mock `ros2_control` smoke test (same behaviour as legacy `verify_plan_execute.py`).
- **Launch:** `ros2 launch gp7_task_executor task_executor.launch.py`
- **Config:** `config/task_executor.yaml` (optional; launch also inlines defaults).

## Legacy verification script

- **`gp7_moveit_config/scripts/verify_plan_execute.py`** — **unchanged**, still installed and used for regression.
- **`gp7_task_executor.verify_fake_stack`** — new implementation written from the same requirements (not a file move).

## Test script

- **`scripts/run_fake_sim_test.sh`** — launches `moveit_fake_hardware.launch.py`, then runs **both** `verify_plan_execute.py` and `verify_fake_stack`. Both must exit 0.

## Archived assets (no deletes)

- **`gp7_description/legacy/`** — `gp7_yaskawa.urdf11.xacro`, `gp7_yaskawa.csv` (see `legacy/README.md`).
- **`gp7_moveit_config/legacy/`** — `planning_python_api.yaml` (see `legacy/README.md`).

## Impacted interfaces

| Item | Change |
|------|--------|
| Topics | No new publishers; `verify_fake_stack` subscribes to `/joint_states` (unchanged from legacy script). |
| Actions | Clients: `/move_action`, `/arm_controller/follow_joint_trajectory` (verify only). |
| Params | New: `gp7_task_executor` node params above. |
| Launch | New: `gp7_task_executor/launch/task_executor.launch.py`. |
| TF | Unchanged (none added by this package). |

## Validation (2026-03-22)

| Check | Result |
|-------|--------|
| `colcon build` (`gp7_task_executor`, `gp7_description`, `gp7_moveit_config`) | **PASS** |
| `./scripts/run_fake_sim_test.sh` (legacy + new verifier, `sleep 45`) | **PASS** (`VERIFY_LEGACY_EXIT=0`, `VERIFY_NEW_EXIT=0`) |

If trajectory discovery is slow, increase the sleep in `run_fake_sim_test.sh` or run `ros2 daemon stop` before the test (script already does).
