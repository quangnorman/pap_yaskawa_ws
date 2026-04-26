# GP7 GUI — Phase 1.6: Launch Manager

A PySide6 + rclpy GUI for the GP7 robot. The GUI starts independently — no bringup needs to be launched manually first.

**Phase 1.6 scope:** Launch Manager — user selects a mode and clicks Start. No motion execution, no service calls.

---

## How to run

```bash
ros2 launch gp7_gui gui.launch.py
```

The GUI starts in **Idle** mode with all panels inactive.

1. Select `sim` or `real` from the dropdown.
2. Click **Start selected mode**.
3. Watch the status change to `SIM launching` → `SIM running` (or `REAL launching` → `REAL running`).
4. Click **Stop system** to shut down and return to Idle.

For `real` mode, a confirmation dialog appears before the launch begins:

> "You are about to start REAL ROBOT mode. Continue?"

---

## Workflow

```
GUI starts (mode = none, no subscriptions)
  └─ User selects sim or real
       └─ User clicks "Start selected mode"
            ├─ (real only) Confirmation dialog
            ├─ LaunchManager starts ros2 launch subprocess
            ├─ Subscriptions activated for chosen mode
            └─ Status: SIM/REAL running
       └─ User clicks "Stop system"
            ├─ LaunchManager terminates subprocess
            ├─ Subscriptions cleared
            └─ Status: Idle
```

---

## Topics used per mode

| Topic | Sim | Real |
|---|---|---|
| Joint states | `/joint_states` | `/robot1/joint_states` |
| Robot status | *(none)* | `/robot1/robot_status` |
| Controller state | `/arm_controller/state` | *(none)* |
| Planned tool path | `/task_executor/planned_tool_path` | `/task_executor/planned_tool_path` |

---

## GUI features

**Launch Control panel:**
- Mode dropdown (`none` / `sim` / `real`)
- **Start selected mode** button (green) — launches bringup for the chosen mode
- **Stop system** button (red) — terminates bringup, returns to Idle
- Launch state indicator (orange = launching, green = running, grey = idle, red = failed)
- Real-mode purple warning banner: "REAL ROBOT MODE — execution disabled until safety confirmation"

**Monitoring panels:**
- Active Topics — topic names with green/red alive indicators
- Joint Positions — live values in rad or deg (toggle in header)
- Tool0 Pose — base_link → tool0 via TF2, 10 Hz, in rad or deg
- Robot Status — sim: controller state actual + error; real: Yaskawa RobotStatus flags

---

## File layout

```
gp7_gui/
├── config/
│   └── gui_modes.yaml       # topics + launch args per mode
├── gp7_gui/
│   ├── __init__.py
│   ├── gui_main.py          # main GUI module
│   └── launch_manager.py    # subprocess launch manager
├── launch/
│   └── gui.launch.py        # ros2 launch entry point
├── package.xml
├── setup.py
└── README.md
```

---

## Launch arguments (gui.launch.py)

| Argument | Default | Description |
|---|---|---|
| `mode` | `none` | Initial selected mode (`none`, `sim`, `real`) |

---

## Upcoming phases

- Phase 2: Motion execution buttons (joint target, pose target, named target)
- Phase 3: Cartesian path visualization
- Phase 4: Waypoint editor / sequence builder
