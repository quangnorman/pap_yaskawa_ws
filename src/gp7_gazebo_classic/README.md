# gp7_gazebo_classic

**Purpose:** Gazebo Classic–only simulation for the Yaskawa GP7. Keeps simulation isolated from `gp7_bringup` (real-robot launch and shared controller YAML).

**Depends on:**
- `gp7_description` — URDF, models, Gazebo tags in xacro
- `gp7_bringup` — shared `config/gp7_controller.yaml` and `rviz/rviz.rviz`
- `gp7_moveit_config` — MoveIt config when using `sim_moveit.launch.py` (renamed from former `moveit.launch.py`)

**Launch files (examples):**
- `launch/gazebo_display.launch.py` — Gazebo display variant (primary lightweight display launch).
- `launch/sim_moveit.launch.py` — full Gazebo + MoveIt + RViz simulation stack (primary planning simulation launch).
- `launch/sim_moveit_vision_rgbd.launch.py` — same as above plus **simulated RGB-D camera** (`models/gp7_sim_rgbd_camera`), TF `world`→`camera_link`→`camera_color_optical_frame`, and optional `vision_sim_rgbd` debug node (`/gp7_sim/camera/...` topics). Hardware RealSense remains `gp7_vision_bringup/vision_debug.launch.py`.

**Legacy launch files:**
- `launch/legacy/gazebo.launch.py` — archived older Gazebo bringup variant.
- `launch/legacy/gazebo1.launch.py` — archived alternate Gazebo/controller layout.

**Offline / no Gazebo:** use `gp7_moveit_config/launch/moveit_fake_hardware.launch.py` (mock hardware), not this package.
