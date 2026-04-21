# gp7_bringup

**Purpose:** Real-robot and lab bringup: shared **`config/gp7_controller.yaml`**, RViz configs, and **non-Gazebo** launch files (e.g. model visualization).

**Launch files:**
- `launch/display.launch.py` — RViz + `joint_state_publisher_gui` + `robot_state_publisher` (no Gazebo, no hardware).
- `launch/legacy/display_xml.xml` — legacy XML launcher reference (archived).

**Gazebo Classic simulation** lives in package **`gp7_gazebo_classic`** (worlds + Gazebo launch files).

**Shared assets used by simulation and hardware:**
- `config/gp7_controller.yaml` — `ros2_control` controller parameters (referenced from URDF xacro and Gazebo launches).
- `rviz/rviz.rviz` — default RViz config (referenced from `gp7_gazebo_classic` and `gp7_moveit_config`).

**Depends on:** `gp7_description` (URDF paths in launch files).
