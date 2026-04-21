# gp7_description

**Purpose:** Single source of truth for the Yaskawa GP7 robot model: URDF/Xacro, meshes, optional config (e.g. default joint positions), and Gazebo model assets.

**Depends on:** `gp7_bringup` only for the default path to `config/gp7_controller.yaml` in `urdf/gp7_yaskawa.urdf.xacro` (`controller_yaml` xacro arg).

**Variants:**
- `urdf/gp7_yaskawa.urdf.xacro` — Gazebo `ros2_control` plugin + same controller YAML path.
- `urdf/gp7_yaskawa_fake.urdf.xacro` — `mock_components/GenericSystem` only (offline / CI; no Gazebo, no drivers).

**TF frames:** Defined by the URDF (e.g. `base_link`, link chain, `tool0` if present).

See `gp7_bringup` for shared controller YAML; `gp7_gazebo_classic` for Gazebo Classic launches; `gp7_moveit_config` for MoveIt and fake-hardware simulation.

**Legacy:** `legacy/` holds duplicate/unused URDF-side files (see `legacy/README.md`); active models remain under `urdf/`.
