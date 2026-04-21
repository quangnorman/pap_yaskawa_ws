# Vision architecture and milestone plan (source of truth)

This document reflects fixed project decisions for Intel RealSense D435 perception, GP7 integration, and downstream Gazebo box simulation. **Motion control remains only through MoveIt 2 / `gp7_task_executor`.** Vision nodes do not publish joint commands.

---

## 1. Confirmed assumptions

| Topic | Decision |
|--------|----------|
| Camera | Intel RealSense D435 |
| Mounting | **Eye-to-hand** (camera rigidly attached to the scene/robot **base** side, not on `tool0`) |
| Vision output frame | **`base_link`** (all poses and dimension reports intended for downstream consumers use this frame) |
| Target class | **Box** |
| Working distance | ~**0.5 m** (design center; not a hard range limit in software) |
| 2D detection | **YOLO** → 2D bounding boxes (training and weights are **out of scope** until a later milestone) |
| 3D from detection | **Aligned depth** to color + **camera intrinsics** → 3D center of box; **approximate** length, width, height from **3D extent** inside the ROI (not from camera API “object size”) |
| Downstream sim | Estimated pose + dimensions feed a **separate bridge** to spawn/update a box model in **Gazebo Classic** (`gp7_gazebo_classic` ecosystem) |
| Metrology | Depth-based dimensions are **approximate** unless a dedicated calibration and validation procedure is performed; D435 is not presented as a certified measuring device |

---

## 2. Revised package architecture

| Package | Role |
|---------|------|
| **`gp7_vision_bringup`** | Composes D435 driver launch, **static TF** `base_link` → `camera_link`, optional RViz, and references debug/perception launches. **No perception algorithms.** |
| **`gp7_vision_pipeline`** | **Perception only**: future YOLO, depth back-projection, extent estimation, publishers into **`base_link`**. **No Gazebo, no spawning.** |
| **`gp7_handeye_calibration`** | Optional future use; for eye-to-hand, the primary extrinsic is often a **measured/calibrated static transform** (may still use a calibration routine). Scaffold remains. |
| **`gp7_vision_gazebo_bridge`** (recommended **new** package, later milestone) | Subscribes to vision outputs (or a stable topic API), calls Gazebo spawn/set model state **only in simulation**. Keeps `gp7_vision_pipeline` free of simulator coupling. |
| **`gp7_vision_msgs`** | **Deferred** until standard messages (`geometry_msgs`, `sensor_msgs`, `vision_msgs`) are insufficient. |

Existing motion packages (`gp7_moveit_config`, `gp7_task_executor`, …) stay unchanged; they may **consume** vision outputs later via explicit interfaces only.

---

## 3. Topic contract

**Driver layer (RealSense, typical defaults with `rs_launch.py`):**

| Topic | Message | Notes |
|-------|---------|--------|
| `/camera/camera/color/image_raw` | `sensor_msgs/Image` | RGB |
| `/camera/camera/aligned_depth_to_color/image_raw` | `sensor_msgs/Image` | **16UC1**, depth aligned to color (required for ROI depth sampling) |
| `/camera/camera/color/camera_info` | `sensor_msgs/CameraInfo` | Intrinsics for back-projection |

Remap via launch if namespace or camera name changes; **keep pipeline params in YAML** aligned with reality.

**Future perception outputs (post-YOLO milestones, illustrative):**

| Topic | Message | Frame id |
|-------|---------|----------|
| TBD stable name, e.g. `/vision/box/pose` | `geometry_msgs/PoseStamped` | **`base_link`** |
| TBD, e.g. `/vision/box/dimensions` | `geometry_msgs/Vector3` or custom **only if needed** | N/A (length/width/height in meters, **approximate**) |

Exact names finalized when implementing the box pipeline; document in `gp7_vision_pipeline` README.

---

## 4. TF contract

| Frame | Role |
|-------|------|
| `world` | World root (existing policy) |
| `base_link` | Robot base; **fixed output frame** for vision results |
| `tool0` | End-effector (unchanged; vision does not command it) |
| `camera_link` | RealSense root frame; **child of `base_link`** for eye-to-hand via **static transform** (until/unless superseded by URDF + calibrated offsets) |
| `camera_color_optical_frame` | Optical frame (from driver / URDF); used for **projection math**, then results transformed to **`base_link`** |

Eye-to-hand: **`base_link` → `camera_link`** published by bringup (static TF scaffold). Driver continues to publish internal camera optical frames under `camera_link`.

---

## 5. Output interface contract

- **Frame:** All pose outputs that are meant for motion planning or simulation bridging are expressed in **`base_link`** (`header.frame_id == base_link`).
- **Box pose:** 6-DoF pose of the **estimated box center** (or a documented reference point on the box), **approximate**.
- **Box dimensions:** Length, width, height in meters from **3D point extent** within the YOLO ROI on **aligned depth** + intrinsics — **not** from device “semantic size” APIs.
- **Uncertainty:** Logs/docs state **approximate** geometry unless calibration + validation are done.
- **Safety:** No joint commands, no `FollowJointTrajectory` from vision packages.

---

## 6. Milestone-by-milestone implementation plan

| Milestone | Scope |
|-----------|--------|
| **M1** | Package skeletons, placeholder node, YAML/launch/README (done). |
| **M2** | RealSense bringup, **static TF** `base_link`→`camera_link`, **RGB + aligned depth + CameraInfo** verification, **lightweight depth debug node** (center-pixel depth sanity), **RViz-capable debug launch**. **No YOLO.** |
| **M3** | Integrate YOLO inference (off-the-shelf weights), ROI extraction, **no training** in-workspace yet; debug viz of boxes in image space. |
| **M4** | For each detection: sample aligned depth in ROI, back-project to 3D camera frame, transform to **`base_link`**, estimate **center** and **approximate L×W×H** from 3D extent (with clear limitations documented). |
| **M5** | **`gp7_vision_gazebo_bridge`**: spawn/update box in Gazebo from vision messages; simulation only. |
| **M6** | Optional: `gp7_vision_msgs`, hand-eye or extrinsic refinement, dataset-based YOLO training workflow **outside** default bringup path. |

---

## 7. Recommended package for Gazebo spawning bridge

**`gp7_vision_gazebo_bridge`** (new package under `src/`, sibling to `gp7_gazebo_classic`):

- **Subscribes** to stable vision topics (poses + dimensions in `base_link`).
- **Publishes** Gazebo model spawn / state updates (Classic APIs already used in the workspace patterns).
- **Depends on** `gp7_gazebo_classic` only at launch/integration level; keeps **`gp7_vision_pipeline`** simulator-agnostic.

---

## 8. Risks and technical limitations

- **Depth noise, missing returns, infrared interference** → wrong extent and pose; must handle invalid pixels and partial ROI visibility.
- **YOLO 2D error** → wrong ROI → wrong 3D crop; no sub-mm metrology claim.
- **Single-view occlusion** → one side of the box may be invisible; L/W/H are **heuristic** (e.g. axis-aligned bbox in camera frame mapped to `base_link`, or percentile bounds on valid depth points).
- **Intrinsic / extrinsic error** without calibration → systematic pose/dimension bias.
- **Working distance ~0.5 m** is a design center; performance outside the D435 sweet spot degrades.
- **RealSense ROS wrapper** version differences may change topic names or parameters — launch args must stay documented and version-pinned in README.

---

## 9. Exact Milestone 2 implementation scope

**In scope:**

- Declare runtime dependency on **`realsense2_camera`** (bringup).
- Launch file(s) that include **`rs_launch.py`** with **aligned depth enabled** (via YAML-driven launch arguments where practical).
- **Static transform** publisher: **`base_link` → `camera_link`** (numeric defaults are a **scaffold**; user replaces with measured/calibrated values).
- **`gp7_vision_pipeline`**: **`realsense_depth_debug_node`** — subscribes to **aligned depth**, **color** (verification), **CameraInfo**; periodic **center-pixel depth** in meters with sanity checks (invalid/zero saturation).
- **`vision_debug.launch.py`** (bringup): camera + static TF + debug node + optional **RViz**.
- **`vision_bringup.launch.py`** updated to compose **camera + static TF +** existing pipeline placeholder (headless stack).
- Documentation updates (README + this file).

**Explicitly out of scope for M2:**

- YOLO (any inference or training).
- Box pose/dimension estimation beyond center-pixel depth sanity.
- Gazebo bridge.
- New custom `.msg` types.
