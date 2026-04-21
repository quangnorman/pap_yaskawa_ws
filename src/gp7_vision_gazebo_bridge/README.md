# gp7_vision_gazebo_bridge

Gazebo Classic bridge for **vision-estimated box pose + size**. This package does **not** run YOLO or any camera processing; it only consumes `/vision/box_pose` and `/vision/box_size` and drives Gazebo services.

## Behavior

`box_spawn_bridge_node`:

1. Subscribes to:
   - `/vision/box_pose` (`geometry_msgs/PoseStamped`) — geometric **center** of the box in `world` (or your `header.frame_id`; spawn uses `reference_frame`, default `world`).
   - `/vision/box_size` (`geometry_msgs/Vector3`) — box extents in meters: **x = length**, **y = width**, **z = height** (matches SDF `<box><size>`).
2. Maintains **exactly one** Gazebo model named **`detected_box`** (configurable via `box_name`).
3. On each meaningful change (pose/size/orientation beyond thresholds), runs **delete → spawn** so the model is replaced in place (no duplicate names under normal operation).
4. After a **successful** spawn, caches the last applied state so **repeated identical messages do not** trigger endless respawns.

Logs to watch (terminal running the bridge):

- `DELETE: calling /delete_entity for 'detected_box'...`
- `DELETE OK:` or a warning if the model did not exist yet
- `SPAWN: calling /spawn_entity for 'detected_box'...`
- `SPAWN OK:` when Gazebo accepted the spawn

## Test publisher (`box_test_publisher_node`)

Publishes configurable fake pose/size (parameters below). No vision packages required.

### Scenario A (default)

- Center: `(0.0, -0.7, 0.45)` m  
- Size: `0.10 × 0.05 × 0.10` m (L × W × H)  
- Table surface at **z = 0.40** m: bottom of box = `0.45 − 0.10/2 = 0.40` m ✓  

### Scenario B

- Size: `0.12 × 0.06 × 0.08` m  
- Center z = **0.44** m so bottom = `0.44 − 0.08/2 = 0.40` m ✓  

Launch with `scenario:=b` (see below).

### Useful parameters

| Parameter | Meaning |
|-----------|---------|
| `x`, `y`, `z` | Box center (m) |
| `yaw_rad` | Yaw-only orientation |
| `length_m`, `width_m`, `height_m` | Box dimensions (m) |
| `publish_rate_hz` | Publish rate for pose + size |
| `pose_topic`, `size_topic` | Remap if needed |
| `log_each_publish` | `true` to log every timer tick |

## Launches

**Full test (Gazebo + MoveIt sim world + bridge + fake publisher):**

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch gp7_vision_gazebo_bridge bridge_test.launch.py
```

**Scenario B preset:**

```bash
ros2 launch gp7_vision_gazebo_bridge bridge_test.launch.py scenario:=b
```

**Bridge + test publisher only** (you already started Gazebo / `sim_moveit_vision_rgbd` elsewhere):

```bash
ros2 launch gp7_vision_gazebo_bridge bridge_standalone.launch.py
```

## Validation

### 1. Entity exists and name is unique

- In **Gazebo GUI**: *Models* list should contain **one** entry **`detected_box`** (red box by default).

If the Gazebo CLI is available:

```bash
gz model -l
```

Expect a **single** line containing `detected_box`. Count duplicates:

```bash
gz model -l | grep -c detected_box
```

Expected: **1** while the bridge has spawned the model.

### 2. Position / size sanity

- Compare the box in the scene to the test publisher parameters (`x,y,z` and `length_m`, `width_m`, `height_m`).
- Scenario A: box center near **y = −0.7**, **z ≈ 0.45**, sitting on the table (**z = 0.4** surface).

If your setup exposes model state via ROS 2, you can also echo relevant topics (names depend on your `gazebo_ros` / world). The authoritative check for this milestone is **Gazebo GUI + bridge logs**.

### 3. No duplicate entities after updates

1. Run `bridge_test.launch.py` with `scenario:=a`; wait for `SPAWN OK`.
2. Stop **only** the test publisher and restart it with different dimensions via CLI override **or** launch `scenario:=b` in a second terminal after killing the first test node — the bridge should log **DELETE** then **SPAWN** again.
3. Run `gz model -l | grep detected_box` repeatedly: **at most one** `detected_box` line.

Bridge policy: always **delete** the same name before **spawn**, so Gazebo should not accumulate `detected_box`, `detected_box_1`, etc.

### 4. Repeated identical messages

With defaults, the test publisher sends the same pose/size at 1 Hz. After the first successful spawn, the bridge should **not** respawn every second (cached state matches). You should see **one** delete/spawn burst at startup, then quiet until parameters change.

## Topics

**Inputs**

- `/vision/box_pose` (`geometry_msgs/PoseStamped`)
- `/vision/box_size` (`geometry_msgs/Vector3`)

**Gazebo services used**

- `/delete_entity`
- `/spawn_entity`

**Model name**

- Default: `detected_box`

## Limitations

- Requires Gazebo Classic with `gazebo_ros` providing `/spawn_entity` and `/delete_entity`.
- Resize is implemented as **full model replacement** (delete + spawn), not in-place link scaling.
