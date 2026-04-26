"""
gp7_gui — GP7 Robot GUI
Phase 1.5: Mode-aware monitoring + unit selector + Tool0 pose display

Architecture:
  - ROS 2 node runs in a background thread to avoid blocking the Qt event loop.
  - Qt Signals are used to safely pass data from the ROS thread to the UI.
  - A Qt timer in the main thread polls the TF buffer at 10 Hz.
  - Topic subscriptions are reconfigured when the user switches sim/real mode.

Mode differences:
  sim:  joint_states <- /joint_states
        controller_state <- /arm_controller/state
        no robot_status

  real: joint_states <- /robot1/joint_states
        robot_status   <- /robot1/robot_status
        no controller_state
"""

import math
import os
import sys
import threading
from typing import Dict, Optional, Tuple

import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

from sensor_msgs.msg import JointState
from nav_msgs.msg import Path
try:
    from control_msgs.msg import JointTrajectoryControllerState
    HAS_CONTROLLER_STATE = True
except ImportError:
    HAS_CONTROLLER_STATE = False
try:
    from yaskawa_robot_controller_msgs.msg import RobotStatus
    HAS_ROBOT_STATUS = True
except ImportError:
    HAS_ROBOT_STATUS = False

from geometry_msgs.msg import TransformStamped
try:
    from tf2_ros import Buffer, TransformListener
    HAS_TF2 = True
except ImportError:
    HAS_TF2 = False

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QObject, Signal, Slot


# ──────────────────────────────────────────────────────────────────────────────
#  Quaternion → RPY (ROS x,y,z,w order)
# ──────────────────────────────────────────────────────────────────────────────

def quaternion_to_rpy(x: float, y: float, z: float, w: float) -> Tuple[float, float, float]:
    """Convert quaternion (ROS x,y,z,w) to roll, pitch, yaw in radians."""
    # Roll (x-axis rotation)
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = 2.0 * (w * y - z * x)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    # Yaw (z-axis rotation)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


# ──────────────────────────────────────────────────────────────────────────────
#  ROS 2 Node — runs in a dedicated thread
# ──────────────────────────────────────────────────────────────────────────────

class GP7RosNode(Node):
    """Background ROS 2 node that subscribes to topics based on the selected mode."""

    def __init__(self, config: Dict):
        super().__init__("gp7_gui_node")
        self._config = config
        self._js_sub: Optional[object] = None
        self._cs_sub: Optional[object] = None
        self._rs_sub: Optional[object] = None
        self._pp_sub: Optional[object] = None

        self._signals = RosSignals()

        self._js_stale = False
        self._cs_stale = False
        self._rs_stale = False

        # TF2 — lookup base_link → tool0
        if HAS_TF2:
            self._tf_buffer = Buffer()
            self._tf_listener = TransformListener(self._tf_buffer, self)
        else:
            self._tf_buffer = None

        # Stale-detection timers
        self._js_timer = self.create_timer(0.5, self._check_js_stale)
        self._cs_timer = self.create_timer(0.5, self._check_cs_stale)
        self._rs_timer = self.create_timer(0.5, self._check_rs_stale)

        # TF polling at 10 Hz
        if HAS_TF2:
            self._tf_timer = self.create_timer(0.1, self._poll_tf)

    # ── called from main thread ─────────────────────────────────────────────

    @Slot(str)
    def switch_mode(self, mode: str) -> None:
        """Unsubscribe / resubscribe based on the new mode."""
        self._teardown_subscriptions()
        cfg = self._config[mode]
        self._setup_subscriptions(cfg)

    def _setup_subscriptions(self, cfg: Dict) -> None:
        self.get_logger().info(f"[gp7_gui] Setting up subscriptions for mode: {cfg}")

        self._js_sub = self.create_subscription(
            JointState, cfg["joint_states_topic"], self._on_joint_states, 10
        )

        if cfg["controller_state_topic"] and HAS_CONTROLLER_STATE:
            self._cs_sub = self.create_subscription(
                JointTrajectoryControllerState,
                cfg["controller_state_topic"],
                self._on_controller_state, 10,
            )
        else:
            self._cs_sub = None

        if cfg["robot_status_topic"] and HAS_ROBOT_STATUS:
            self._rs_sub = self.create_subscription(
                RobotStatus,
                cfg["robot_status_topic"],
                self._on_robot_status, 10,
            )
        else:
            self._rs_sub = None

        self._pp_sub = self.create_subscription(
            Path, cfg["planned_path_topic"], self._on_planned_path, 10
        )

        self._js_stale = False
        self._cs_stale = False
        self._rs_stale = False

    def _teardown_subscriptions(self) -> None:
        if self._js_sub:
            self.destroy_subscription(self._js_sub)
            self._js_sub = None
        if self._cs_sub:
            self.destroy_subscription(self._cs_sub)
            self._cs_sub = None
        if self._rs_sub:
            self.destroy_subscription(self._rs_sub)
            self._rs_sub = None
        if self._pp_sub:
            self.destroy_subscription(self._pp_sub)
            self._pp_sub = None

    # ── subscription callbacks ──────────────────────────────────────────────

    def _on_joint_states(self, msg: JointState) -> None:
        self._js_stale = False
        self._signals.joints_updated.emit(
            dict(zip(msg.name, msg.position)) if msg.position else {}
        )

    def _on_controller_state(self, msg: JointTrajectoryControllerState) -> None:
        self._cs_stale = False
        actual = list(msg.actual.positions) if msg.actual.positions else []
        error = list(msg.error.positions) if msg.error.positions else []
        self._signals.controller_state_updated.emit(actual, error)

    def _on_robot_status(self, msg: object) -> None:
        self._cs_stale = False
        self._rs_stale = False
        self._signals.robot_status_updated.emit({
            "drives_powered": getattr(msg, "drives_powered", False),
            "motion_possible": getattr(msg, "motion_possible", False),
            "in_motion": getattr(msg, "in_motion", False),
            "in_error": getattr(msg, "in_error", False),
        })

    def _on_planned_path(self, msg: Path) -> None:
        self._signals.planned_path_updated.emit(len(msg.poses))

    # ── stale monitoring ───────────────────────────────────────────────────

    def _check_js_stale(self) -> None:
        if self._js_stale and self._js_sub:
            self._signals.topic_status_updated.emit("joint_states", False)
        else:
            self._signals.topic_status_updated.emit("joint_states", True)
        self._js_stale = True

    def _check_cs_stale(self) -> None:
        topic = "controller_state" if self._cs_sub else None
        if topic:
            self._signals.topic_status_updated.emit(topic, not self._cs_stale)
            self._cs_stale = True

    def _check_rs_stale(self) -> None:
        topic = "robot_status" if self._rs_sub else None
        if topic:
            self._signals.topic_status_updated.emit(topic, not self._rs_stale)
            self._rs_stale = True

    # ── TF polling ────────────────────────────────────────────────────────

    def _poll_tf(self) -> None:
        """Lookup base_link → tool0 transform and emit via signal."""
        if not HAS_TF2 or self._tf_buffer is None:
            return
        try:
            transform = self._tf_buffer.lookup_transform(
                "base_link", "tool0", rclpy.time.Time()
            )
            t = transform.transform.translation
            q = transform.transform.rotation
            roll, pitch, yaw = quaternion_to_rpy(q.x, q.y, q.z, q.w)
            self._signals.tf_pose_updated.emit({
                "tx": t.x, "ty": t.y, "tz": t.z,
                "roll": roll, "pitch": pitch, "yaw": yaw,
                "available": True,
            })
        except Exception:
            self._signals.tf_pose_updated.emit({"available": False})


# ──────────────────────────────────────────────────────────────────────────────
#  Qt Signals — bridge between ROS thread and Qt main thread
# ──────────────────────────────────────────────────────────────────────────────

class RosSignals(QObject):
    joints_updated = Signal(dict)
    controller_state_updated = Signal(list, list)   # actual positions, tracking error
    robot_status_updated = Signal(dict)
    planned_path_updated = Signal(int)              # number of poses
    topic_status_updated = Signal(str, bool)       # topic name, alive
    tf_pose_updated = Signal(dict)                 # tx,ty,tz,roll,pitch,yaw (all rad)


# ──────────────────────────────────────────────────────────────────────────────
#  Main Window
# ──────────────────────────────────────────────────────────────────────────────

class GP7MainWindow(QtWidgets.QMainWindow):
    """Phase 1.5 GUI — mode-aware monitoring + unit selector + Tool0 pose."""

    JOINT_NAMES = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]
    MODES = ["sim", "real"]
    UNIT_OPTIONS = ["rad", "deg"]

    def __init__(self, config: Dict, initial_mode: str = "sim"):
        super().__init__()
        self._config = config
        self._mode = initial_mode
        self._unit = "rad"
        self._raw_joints: Dict[str, float] = {}
        self._ros_node: Optional[GP7RosNode] = None
        self._ros_thread: Optional[threading.Thread] = None

        self.setWindowTitle("GP7 Robot GUI — Phase 1.5: Monitoring")
        self.setMinimumSize(780, 580)
        self._setup_ui()
        self._connect_signals()
        self._start_ros(initial_mode)

    # ── UI setup ────────────────────────────────────────────────────────────

    def _setup_ui(self) -> None:
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        top_layout = QtWidgets.QVBoxLayout(central)

        top_layout.addWidget(self._build_header())
        top_layout.addWidget(self._build_topic_strip())
        top_layout.addWidget(self._build_joints_panel())
        top_layout.addWidget(self._build_tool_pose_panel())
        top_layout.addWidget(self._build_status_panel())
        top_layout.addStretch()

    def _build_header(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Mode Selection")
        layout = QtWidgets.QHBoxLayout(group)

        lbl = QtWidgets.QLabel("Operation mode:")
        lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl)

        self._mode_combo = QtWidgets.QComboBox()
        self._mode_combo.addItems(self.MODES)
        self._mode_combo.setCurrentText(self._mode)
        layout.addWidget(self._mode_combo)

        layout.addSpacing(24)

        unit_lbl = QtWidgets.QLabel("Angular unit:")
        unit_lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(unit_lbl)

        self._unit_combo = QtWidgets.QComboBox()
        self._unit_combo.addItems(self.UNIT_OPTIONS)
        self._unit_combo.setCurrentText(self._unit)
        layout.addWidget(self._unit_combo)

        layout.addStretch()

        self._mode_label = QtWidgets.QLabel(f"[{self._mode.upper()}]")
        self._mode_label.setStyleSheet(
            "font-size: 14pt; font-weight: bold; color: #2e86de;"
        )
        layout.addWidget(self._mode_label)

        return group

    def _build_topic_strip(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Active Topics")
        layout = QtWidgets.QGridLayout(group)

        self._topic_labels: Dict[str, QtWidgets.QLabel] = {}
        self._topic_alive: Dict[str, QtWidgets.QLabel] = {}

        topics = [
            ("js_topic", "Joint States:"),
            ("rs_topic", "Robot Status:"),
            ("cs_topic", "Controller State:"),
            ("pp_topic", "Planned Path:"),
        ]
        for col, (key, label) in enumerate(topics):
            lbl = QtWidgets.QLabel(label)
            lbl.setStyleSheet("font-weight: bold;")
            layout.addWidget(lbl, 0, col * 2)

            val = QtWidgets.QLabel("—")
            val.setStyleSheet("color: #888; font-family: monospace; font-size: 9pt;")
            layout.addWidget(val, 0, col * 2 + 1)
            self._topic_labels[key] = val

            indicator = QtWidgets.QLabel("●")
            indicator.setStyleSheet("color: #555; font-size: 10pt;")
            layout.addWidget(indicator, 1, col * 2 + 1)
            self._topic_alive[key] = indicator

        return group

    def _build_joints_panel(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Joint Positions")
        group_layout = QtWidgets.QVBoxLayout(group)

        # Header row with joint names
        header_row = QtWidgets.QHBoxLayout()
        header_row.addStretch()
        for name in self.JOINT_NAMES:
            lbl = QtWidgets.QLabel(name)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setStyleSheet("font-weight: bold; font-size: 9pt; color: #aaa;")
            lbl.setMinimumWidth(60)
            header_row.addWidget(lbl)
        header_row.addStretch()

        # Unit label row
        self._joint_unit_lbl = QtWidgets.QLabel("unit: rad")
        self._joint_unit_lbl.setStyleSheet("font-size: 9pt; color: #888;")
        header_row.addWidget(self._joint_unit_lbl)

        group_layout.addLayout(header_row)

        # Value row
        value_row = QtWidgets.QHBoxLayout()
        value_row.addStretch()
        self._joint_cells: Dict[str, QtWidgets.QLabel] = {}
        for name in self.JOINT_NAMES:
            cell = QtWidgets.QLabel("—")
            cell.setAlignment(QtCore.Qt.AlignCenter)
            cell.setStyleSheet(
                "background: #1e1e1e; color: #00e676; "
                "border: 1px solid #333; border-radius: 4px; "
                "padding: 4px; font-family: monospace; font-size: 9pt;"
            )
            cell.setMinimumHeight(28)
            cell.setMinimumWidth(60)
            value_row.addWidget(cell)
            self._joint_cells[name] = cell
        value_row.addStretch()

        group_layout.addLayout(value_row)
        return group

    def _build_tool_pose_panel(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Tool0 Pose  (base_link → tool0)")
        layout = QtWidgets.QGridLayout(group)

        self._pose_cells: Dict[str, QtWidgets.QLabel] = {}
        fields = [
            ("tx", "X (m)"), ("ty", "Y (m)"), ("tz", "Z (m)"),
            ("roll", "Roll"), ("pitch", "Pitch"), ("yaw", "Yaw"),
        ]
        for i, (key, label) in enumerate(fields):
            row, col = i // 3, (i % 3) * 2
            lbl = QtWidgets.QLabel(label)
            lbl.setStyleSheet("font-weight: bold; font-size: 9pt; color: #aaa;")
            layout.addWidget(lbl, row, col)

            cell = QtWidgets.QLabel("—")
            cell.setAlignment(QtCore.Qt.AlignCenter)
            cell.setStyleSheet(
                "background: #1e1e2e; color: #ce93d8; "
                "border: 1px solid #333; border-radius: 4px; "
                "padding: 3px; font-family: monospace; font-size: 9pt;"
            )
            cell.setMinimumHeight(26)
            layout.addWidget(cell, row, col + 1)
            self._pose_cells[key] = cell

        self._pose_unit_lbl = QtWidgets.QLabel("unit: rad")
        self._pose_unit_lbl.setStyleSheet("font-size: 9pt; color: #888;")
        layout.addWidget(self._pose_unit_lbl, 2, 1)

        self._tf_status_lbl = QtWidgets.QLabel("")
        self._tf_status_lbl.setStyleSheet("font-size: 9pt; color: #ff5252;")
        layout.addWidget(self._tf_status_lbl, 2, 3, 1, 2)

        return group

    def _build_status_panel(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Robot Status")
        layout = QtWidgets.QGridLayout(group)

        # ── Sim: Controller State ───────────────────────────────────────────
        self._cs_group = QtWidgets.QGroupBox("Controller State (sim)")
        cs_layout = QtWidgets.QGridLayout(self._cs_group)

        self._cs_actual_cells: Dict[str, QtWidgets.QLabel] = {}
        self._cs_error_cells: Dict[str, QtWidgets.QLabel] = {}

        for i, name in enumerate(self.JOINT_NAMES):
            lbl = QtWidgets.QLabel(name)
            lbl.setStyleSheet("font-weight: bold; font-size: 8pt; color: #aaa;")
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            cs_layout.addWidget(lbl, 0, i)

            actual = QtWidgets.QLabel("—")
            actual.setAlignment(QtCore.Qt.AlignCenter)
            actual.setStyleSheet(
                "background: #1a1a2e; color: #00bcd4; "
                "border: 1px solid #333; border-radius: 4px; "
                "padding: 2px; font-family: monospace; font-size: 8pt;"
            )
            cs_layout.addWidget(actual, 1, i)
            self._cs_actual_cells[name] = actual

            error = QtWidgets.QLabel("—")
            error.setAlignment(QtCore.Qt.AlignCenter)
            error.setStyleSheet(
                "background: #2e1a1a; color: #ff5252; "
                "border: 1px solid #333; border-radius: 4px; "
                "padding: 2px; font-family: monospace; font-size: 8pt;"
            )
            cs_layout.addWidget(error, 2, i)
            self._cs_error_cells[name] = error

        row_lbl = QtWidgets.QLabel("actual")
        row_lbl.setStyleSheet("font-size: 8pt; color: #00bcd4;")
        cs_layout.addWidget(row_lbl, 1, len(self.JOINT_NAMES))
        row_lbl = QtWidgets.QLabel("error")
        row_lbl.setStyleSheet("font-size: 8pt; color: #ff5252;")
        cs_layout.addWidget(row_lbl, 2, len(self.JOINT_NAMES))

        # ── Real: Robot Status ──────────────────────────────────────────────
        self._rs_group = QtWidgets.QGroupBox("Yaskawa Robot Status (real)")
        rs_layout = QtWidgets.QGridLayout(self._rs_group)

        self._rs_cells: Dict[str, QtWidgets.QLabel] = {}
        fields = ["drives_powered", "motion_possible", "in_motion", "in_error"]
        for col, field in enumerate(fields):
            lbl = QtWidgets.QLabel(field.replace("_", " ").capitalize())
            lbl.setStyleSheet("font-weight: bold; font-size: 9pt; color: #aaa;")
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            rs_layout.addWidget(lbl, 0, col)

            cell = QtWidgets.QLabel("—")
            cell.setAlignment(QtCore.Qt.AlignCenter)
            cell.setMinimumWidth(60)
            rs_layout.addWidget(cell, 1, col)
            self._rs_cells[field] = cell

        # ── Stacked widget ──────────────────────────────────────────────────
        self._status_stack = QtWidgets.QStackedWidget()
        self._status_stack.addWidget(self._cs_group)   # index 0 = sim
        self._status_stack.addWidget(self._rs_group)   # index 1 = real
        layout.addWidget(self._status_stack, 0, 0, 1, 2)

        # Planned path
        self._path_label = QtWidgets.QLabel("Planned path: — pose(s)")
        self._path_label.setStyleSheet("color: #aaa; font-size: 9pt;")
        layout.addWidget(self._path_label, 1, 0, 1, 2)

        self._update_status_visibility()
        return group

    # ── signal connections ─────────────────────────────────────────────────

    def _connect_signals(self) -> None:
        self._mode_combo.currentTextChanged.connect(self._on_mode_changed)
        self._unit_combo.currentTextChanged.connect(self._on_unit_changed)

    def _start_ros(self, mode: str) -> None:
        self._mode = mode
        self._update_status_visibility()
        self._update_topic_labels()

        def ros_spin():
            rclpy.init()
            node = GP7RosNode(self._config)
            self._ros_node = node
            node.switch_mode(mode)
            node._signals.joints_updated.connect(self._on_joints_updated)
            node._signals.controller_state_updated.connect(self._on_controller_state_updated)
            node._signals.robot_status_updated.connect(self._on_robot_status_updated)
            node._signals.planned_path_updated.connect(self._on_planned_path_updated)
            node._signals.topic_status_updated.connect(self._on_topic_status_updated)
            node._signals.tf_pose_updated.connect(self._on_tf_pose_updated)
            try:
                while rclpy.ok():
                    rclpy.spin_once(node, timeout_sec=0.05)
            finally:
                node.destroy_node()
                rclpy.shutdown()

        self._ros_thread = threading.Thread(target=ros_spin, daemon=True)
        self._ros_thread.start()

    # ── Qt Slots ───────────────────────────────────────────────────────────

    @Slot(str)
    def _on_mode_changed(self, mode: str) -> None:
        self._mode = mode
        self._mode_label.setText(f"[{mode.upper()}]")
        self._mode_label.setStyleSheet(
            "font-size: 14pt; font-weight: bold; "
            + ("color: #2e86de;" if mode == "sim" else "color: #f6c90e;")
        )
        self._update_status_visibility()
        self._update_topic_labels()
        if self._ros_node:
            self._ros_node.switch_mode(mode)

    @Slot(str)
    def _on_unit_changed(self, unit: str) -> None:
        self._unit = unit
        self._joint_unit_lbl.setText(f"unit: {unit}")
        self._pose_unit_lbl.setText(f"unit: {unit}")
        self._refresh_joint_display()
        self._refresh_pose_display()

    @Slot(dict)
    def _on_joints_updated(self, joints: Dict[str, float]) -> None:
        self._raw_joints = joints
        self._refresh_joint_display()

    def _refresh_joint_display(self) -> None:
        factor = 180.0 / math.pi if self._unit == "deg" else 1.0
        for name in self.JOINT_NAMES:
            val = self._raw_joints.get(name)
            if val is not None:
                self._joint_cells[name].setText(f"{val * factor:.3f}")
            else:
                self._joint_cells[name].setText("—")

    @Slot(list, list)
    def _on_controller_state_updated(self, actual: list, error: list) -> None:
        factor = 180.0 / math.pi if self._unit == "deg" else 1.0
        for i, name in enumerate(self.JOINT_NAMES):
            if i < len(actual):
                self._cs_actual_cells[name].setText(f"{actual[i] * factor:.3f}")
            if i < len(error):
                self._cs_error_cells[name].setText(f"{error[i] * factor:.3f}")

    @Slot(dict)
    def _on_robot_status_updated(self, status: Dict) -> None:
        for field, cell in self._rs_cells.items():
            val = status.get(field, False)
            cell.setText("ON" if val else "OFF")
            cell.setStyleSheet(
                "background: "
                + ("#1b4332; color: #52b788; " if val else "#5c1a1a; color: #ff5252; ")
                + "border: 1px solid #333; border-radius: 4px; "
                + "padding: 2px; font-weight: bold; font-size: 9pt;"
            )

    @Slot(int)
    def _on_planned_path_updated(self, num_poses: int) -> None:
        self._path_label.setText(f"Planned path: {num_poses} pose(s)")

    @Slot(str, bool)
    def _on_topic_status_updated(self, topic: str, alive: bool) -> None:
        key_map = {
            "joint_states": "js_topic",
            "controller_state": "cs_topic",
            "robot_status": "rs_topic",
        }
        key = key_map.get(topic)
        if key and key in self._topic_alive:
            indicator = self._topic_alive[key]
            indicator.setStyleSheet(
                "color: #00e676; font-size: 10pt;" if alive
                else "color: #ff5252; font-size: 10pt;"
            )

    # ── TF pose slot (driven by ROS thread signal) ───────────────────────

    @Slot(dict)
    def _on_tf_pose_updated(self, pose: Dict[str, float]) -> None:
        if not pose.get("available", False):
            self._tf_status_lbl.setText("TF not available: base_link → tool0")
            return
        self._pose_cells["tx"].setText(f"{pose['tx']:.4f}")
        self._pose_cells["ty"].setText(f"{pose['ty']:.4f}")
        self._pose_cells["tz"].setText(f"{pose['tz']:.4f}")

        factor = 180.0 / math.pi if self._unit == "deg" else 1.0
        self._pose_cells["roll"].setText(f"{pose['roll'] * factor:.3f}")
        self._pose_cells["pitch"].setText(f"{pose['pitch'] * factor:.3f}")
        self._pose_cells["yaw"].setText(f"{pose['yaw'] * factor:.3f}")

        self._tf_status_lbl.setText("")

    # ── helpers ────────────────────────────────────────────────────────────

    def _update_status_visibility(self) -> None:
        self._status_stack.setCurrentIndex(0 if self._mode == "sim" else 1)

    def _update_topic_labels(self) -> None:
        cfg = self._config[self._mode]
        self._topic_labels["js_topic"].setText(cfg["joint_states_topic"])
        self._topic_labels["rs_topic"].setText(cfg["robot_status_topic"] or "—")
        self._topic_labels["cs_topic"].setText(cfg["controller_state_topic"] or "—")
        self._topic_labels["pp_topic"].setText(cfg["planned_path_topic"])

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self._ros_node:
            self._ros_node.get_logger().info("[gp7_gui] Shutting down ROS node...")
        event.accept()


# ──────────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description="GP7 Robot GUI — Phase 1.5")
    parser.add_argument(
        "--mode", default="sim", choices=["sim", "real"],
        help="Initial operation mode (sim or real)"
    )
    parsed, _ = parser.parse_known_args(args or [])

    config_path = os.path.join(
        get_package_share_directory("gp7_gui"), "config", "gui_modes.yaml"
    )
    if not os.path.exists(config_path):
        print(
            f"[gp7_gui] ERROR: config file not found at {config_path}\n"
            "Did you forget to source the workspace?",
            file=sys.stderr,
        )
        sys.exit(1)

    import yaml
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    app = QtWidgets.QApplication(["GP7 Robot GUI"])
    app.setStyle("Fusion")
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(30, 30, 30))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(35, 35, 35))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 45))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(46, 134, 222))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(dark_palette)

    window = GP7MainWindow(config, initial_mode=parsed.mode)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
