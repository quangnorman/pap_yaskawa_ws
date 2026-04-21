# gp7_handeye_calibration

**Scaffold only** for future extrinsic tooling. The current project decision is **eye-to-hand** (camera on `base_link` side): the primary mount transform is the **static TF** in `gp7_vision_bringup`. This package may later hold refinement workflows (e.g. Charuco) if you move to eye-in-hand or want sub-centimeter extrinsics. No calibration logic in Milestone 1.

## Intended use (later)

- Collect poses via MoveIt-safe motions (no direct joint streaming on hardware).
- Solve for static transform `tool0` → `camera_link` (eye-in-hand) or `base_link` → `camera_link` (eye-to-hand), then commit to URDF or `robot_state_publisher` supplementary TF.

## Files

| Path | Role |
|------|------|
| `launch/handeye_stub.launch.py` | Empty launch (placeholder). |
| `config/handeye_params.yaml` | Reserved parameter names. |

## Launch

```bash
ros2 launch gp7_handeye_calibration handeye_stub.launch.py
```

(No nodes start in Milestone 1.)

## Dependencies

Milestone 1: `launch`, `launch_ros` only. Future milestones may add calibration libraries explicitly in `package.xml`.
