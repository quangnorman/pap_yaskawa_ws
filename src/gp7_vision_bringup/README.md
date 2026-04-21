# gp7_vision_bringup

Launch files and YAML for **vision-only** bringup: Intel RealSense D435 (`realsense2_camera`), **eye-to-hand** static TF (`base_link` → `camera_link`), and composition with `gp7_vision_pipeline`. Does **not** start MoveIt, controllers, or `gp7_task_executor`.

## Prerequisites (hardware / system)

- D435 connected, `udev` rules installed per Intel documentation.
- ROS 2 package: `sudo apt install ros-humble-realsense2-camera` (or build `realsense-ros` from source into the workspace).

If launch arguments differ for your driver version, compare with:

```bash
ros2 launch realsense2_camera rs_launch.py --show-args
```

and edit `config/d435_realsense_launch_args.yaml`.

## Real camera topics (verify locally)

**Do not assume** topic strings without checking. With the driver running:

```bash
source install/setup.bash
ros2 topic list | grep -E '^/camera|^/cam'
bash $(ros2 pkg prefix gp7_vision_bringup)/share/gp7_vision_bringup/scripts/check_realsense_topics.bash
```

Expected names for many `rs_launch.py` defaults are listed in `config/d435_topic_contract.yaml`. If yours differ, edit `gp7_vision_pipeline/config/realsense_depth_debug.yaml` or launch with:

```bash
ros2 launch gp7_vision_bringup vision_debug.launch.py depth_debug_params:=/path/to/your_params.yaml
```

`d435_realsense_launch_args.yaml` enables **`pointcloud.enable`** so `/camera/camera/depth/color/points` is likely (confirm with `ros2 topic list`). If the driver errors, set it to `false` in that YAML.

## Hardware mount defaults (static TF)

`static_tf_camera.launch.py`, `vision_debug.launch.py`, and `vision_bringup.launch.py` share defaults:

This publishes the eye-to-hand static mount **`world → camera_link`** only (the RealSense driver is expected to publish the optical frame TF).

| Quantity | Default | Meaning |
|----------|---------|--------|
| Parent → child | `world → camera_link` | Measured mount pose (see your ground truth) |
| Translation | `(0.0, -0.7, 1.0)` m | REP-103 right = −Y, 1.0 m height |
| Roll | `pi` | Lens/scene Z aligned so the camera looks straight downward |
| Pitch | `0.0` | No tilt off vertical |
| Yaw | `0.0` | Tail/USB side points toward the robot per your mounting |

Override any with launch args, e.g. `cam_ty:=-0.7`.

## Launches

| File | Purpose |
|------|---------|
| `realsense_d435.launch.py` | D435 only (loads args from `config/d435_realsense_launch_args.yaml`). |
| `static_tf_camera.launch.py` | Static mount TF (defaults above). |
| `vision_bringup.launch.py` | Headless: RealSense + static TF + `vision_pipeline_placeholder`. |
| `vision_debug.launch.py` | RealSense + static TF + `realsense_depth_debug` + optional RViz. |
| `vision_sim_rgbd.launch.py` | **Gazebo sim only** (see `gp7_gazebo_classic`). |

### RViz (hardware debug)

Fixed Frame **`world`**. Image topics (verify names first):

- Color: `/camera/camera/color/image_raw`
- Depth: `/camera/camera/aligned_depth_to_color/image_raw`

**Gazebo sim** (different names): `/gp7_sim/camera/color/image_raw`, `/gp7_sim/camera/depth/image_raw`.

## Config

| File | Role |
|------|------|
| `config/d435_realsense_launch_args.yaml` | Passed to `rs_launch.py`. |
| `config/d435_realsense.yaml` | Notes + pointers. |
| `config/d435_topic_contract.yaml` | Expected topic template (**verify**). |

## Dependencies

- `launch`, `launch_ros`, `ament_index_python`, `python3-yaml`
- `gp7_vision_pipeline`
- `realsense2_camera`, `tf2_ros`, `rviz2`

## Validation checklist (hardware)

1. `colcon build --symlink-install` and `source install/setup.bash`.
2. `ros2 launch gp7_vision_bringup vision_debug.launch.py`
3. Script + `ros2 topic hz` on color, aligned depth, `camera_info`, point cloud (if listed).
4. Logs: **RGB OK** and center depth lines from `realsense_depth_debug`.
5. `ros2 run tf2_ros tf2_echo world camera_link` matches mount; adjust `cam_roll`/`cam_pitch`/`cam_yaw` if orientation is wrong in RViz.

Architecture: [`docs/VISION_ARCHITECTURE.md`](../../docs/VISION_ARCHITECTURE.md).
