# Phase 3 cleanup report

## Policy

- No blind deletes: duplicates/unused files were **moved** to per-package `legacy/` with README notes.
- `verify_plan_execute.py` **retained** under `gp7_moveit_config/scripts/` for regression.

## Actions taken

| Location | Action |
|----------|--------|
| `gp7_description/urdf/gp7_yaskawa.urdf11.xacro` | Moved → `gp7_description/legacy/` |
| `gp7_description/urdf/gp7_yaskawa.csv` | Moved → `gp7_description/legacy/` |
| `gp7_moveit_config/config/planning_python_api.yaml` | Moved → `gp7_moveit_config/legacy/` |
| CMake `install()` | Updated to install `legacy/` trees for both packages |

## Candidates (not moved in this phase)

| Item | Suggested follow-up |
|------|---------------------|
| Extra Gazebo worlds under `gp7_gazebo_classic` | Audit usage; archive only if confirmed unused. |
| `gp7_bringup/launch/display_xml.xml` | Mark as legacy RViz/display helper if superseded; archive when safe. |

## Deletes

- **None** in Phase 3.

## Validation snapshot (2026-03-22)

- **`./scripts/run_fake_sim_test.sh`:** **PASS** — both `verify_plan_execute.py` (legacy) and `verify_fake_stack` (new) exited 0 after `moveit_fake_hardware.launch.py` (post-launch wait 45 s).
- **`colcon build`** for touched packages: **PASS**.
