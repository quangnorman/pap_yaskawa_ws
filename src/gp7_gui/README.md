# GP7 GUI — Phase 1: Mode-Aware Monitoring

A PySide6 + rclpy GUI for monitoring the GP7 robot in simulation and real modes.

**Phase 1 scope:** Read-only monitoring — no motion execution, no service calls.

---

## Topics used per mode

| Topic | Sim | Real |
|---|---|---|
| Joint states | `/joint_states` | `/robot1/joint_states` |
| Robot status | *(none)* | `/robot1/robot_status` |
| Controller state | `/arm_controller/state` | *(none)* |
| Planned tool path | `/task_executor/planned_tool_path` | `/task_executor/planned_tool_path` |

---

## How to run

### Simulation mode

Terminal 1 — robot bringup:
```bash
ros2 launch gp7_bringup main.launch.py mode:=sim
```

Terminal 2 — GUI:
```bash
ros2 launch gp7_gui gui.launch.py mode:=sim
```

### Real robot mode

```bash
export ROS_DOMAIN_ID=1
ros2 launch gp7_bringup main.launch.py mode:=real
```

```bash
ros2 launch gp7_gui gui.launch.py mode:=real
```

---

## GUI features (Phase 1)

- **Mode selector** — switch between `sim` and `real` at runtime; subscriptions update instantly
- **Joint positions** — live readouts for joint_1 … joint_6 (rad)
- **Topic status indicators** — green/red dot shows whether each subscription is alive
- **Sim mode** — controller state actual positions + tracking error per joint
- **Real mode** — Yaskawa `RobotStatus` fields: drives_powered, motion_possible, in_motion, in_error
- **Planned path counter** — shows number of poses in `/task_executor/planned_tool_path`

---

## File layout

```
gp7_gui/
├── config/
│   └── gui_modes.yaml       # topic names per mode
├── gp7_gui/
│   ├── __init__.py
│   └── gui_main.py          # main GUI module
├── launch/
│   └── gui.launch.py        # ros2 launch entry point
├── package.xml
├── setup.py
└── README.md
```

---

## Upcoming phases

- Phase 2: Motion execution buttons (joint target, pose target, named target)
- Phase 3: Cartesian path visualization
- Phase 4: Waypoint editor / sequence builder
