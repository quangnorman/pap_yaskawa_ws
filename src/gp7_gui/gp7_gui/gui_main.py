"""
gp7_gui — GP7 Robot GUI
Phase 1.6: Launch Manager — GUI starts independently, user controls bringup

Architecture:
  - GUI starts with mode=none (no ROS subscriptions).
  - LaunchManager handles ros2 launch subprocesses via subprocess.Popen.
  - ROS 2 node runs in a background thread to avoid blocking the Qt event loop.
  - Qt Signals bridge the ROS thread and the UI.
  - TF2 polls at 10 Hz for base_link → tool0.

Workflow:
  1. GUI starts independently — no bringup required.
  2. User selects sim or real from the dropdown.
  3. User clicks "Start selected mode" to launch the bringup.
  4. GUI subscribes to topics for the chosen mode.
  5. User clicks "Stop system" to shut down and return to idle.
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

from gp7_gui.launch_manager import LaunchManager, LaunchState


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

        js_topic = cfg.get("joint_states_topic", "")
        if js_topic:
            self._js_sub = self.create_subscription(
                JointState, js_topic, self._on_joint_states, 10
            )

        if cfg.get("controller_state_topic") and HAS_CONTROLLER_STATE:
            self._cs_sub = self.create_subscription(
                JointTrajectoryControllerState,
                cfg["controller_state_topic"],
                self._on_controller_state, 10,
            )

        if cfg.get("robot_status_topic") and HAS_ROBOT_STATUS:
            self._rs_sub = self.create_subscription(
                RobotStatus,
                cfg["robot_status_topic"],
                self._on_robot_status, 10,
            )

        pp_topic = cfg.get("planned_path_topic", "")
        if pp_topic:
            self._pp_sub = self.create_subscription(
                Path, pp_topic, self._on_planned_path, 10
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
            pass  # Silently ignore — "TF not available" only shown when mode is none


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
    """Phase 1.6 GUI — Launch Manager with mode selector and Start/Stop buttons."""

    JOINT_NAMES = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]
    MODES = ["none", "sim", "real"]
    UNIT_OPTIONS = ["rad", "deg"]

    def __init__(self, config: Dict, initial_mode: str = "none"):
        super().__init__()
        self._config = config
        self._mode = initial_mode          # what the combo box says
        self._running_mode = "none"        # what is actually launched
        self._stop_reason: Optional[str] = None  # "manual" or "before_launch"
        self._pending_launch: Optional[str] = None  # mode to launch after stop
        self._pending_mode: Optional[str] = None
        self._unit = "rad"
        self._raw_joints: Dict[str, float] = {}
        self._ros_node: Optional[GP7RosNode] = None
        self._ros_thread: Optional[threading.Thread] = None

        # LaunchManager — runs ros2 launch as a subprocess
        self._launch_manager = LaunchManager(self)

        self.setWindowTitle("GP7 Robot GUI — Phase 1.6: Launch Manager")
        self.setMinimumSize(780, 620)
        self._setup_ui()
        self._connect_signals()
        self._start_ros()  # No subscriptions until user starts a mode

    # ── UI setup ────────────────────────────────────────────────────────────

    def _setup_ui(self) -> None:
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        top_layout = QtWidgets.QVBoxLayout(central)

        top_layout.addWidget(self._build_header())
        top_layout.addWidget(self._build_control_panel())
        top_layout.addWidget(self._build_topic_strip())
        top_layout.addWidget(self._build_joints_panel())
        top_layout.addWidget(self._build_tool_pose_panel())
        top_layout.addWidget(self._build_status_panel())
        top_layout.addStretch()

    def _build_header(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox()
        group.setStyleSheet("border: none;")
        layout = QtWidgets.QHBoxLayout(group)

        self._title_lbl = QtWidgets.QLabel("GP7 Robot GUI")
        self._title_lbl.setStyleSheet("font-size: 16pt; font-weight: bold; color: #e0e0e0;")
        layout.addWidget(self._title_lbl)

        layout.addStretch()

        unit_lbl = QtWidgets.QLabel("Angular unit:")
        unit_lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(unit_lbl)

        self._unit_combo = QtWidgets.QComboBox()
        self._unit_combo.addItems(self.UNIT_OPTIONS)
        self._unit_combo.setCurrentText(self._unit)
        self._unit_combo.setMinimumWidth(90)
        self._unit_combo.setFixedWidth(90)
        self._unit_combo.setSizeAdjustPolicy(
            QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        layout.addWidget(self._unit_combo)

        return group

    def _build_control_panel(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Launch Control")
        layout = QtWidgets.QHBoxLayout(group)

        mode_lbl = QtWidgets.QLabel("Selected mode:")
        mode_lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(mode_lbl)

        self._mode_combo = QtWidgets.QComboBox()
        self._mode_combo.addItems(self.MODES)
        self._mode_combo.setCurrentText("none")
        layout.addWidget(self._mode_combo)

        layout.addSpacing(16)

        self._start_btn = QtWidgets.QPushButton("Start selected mode")
        self._start_btn.setStyleSheet(
            "background: #2e7d32; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 16px;"
        )
        self._start_btn.clicked.connect(self._on_start_clicked)
        layout.addWidget(self._start_btn)

        self._stop_btn = QtWidgets.QPushButton("Stop system")
        self._stop_btn.setEnabled(False)
        self._stop_btn.setStyleSheet(
            "background: #c62828; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 16px;"
        )
        self._stop_btn.clicked.connect(self._on_stop_clicked)
        layout.addWidget(self._stop_btn)

        layout.addSpacing(16)

        self._launch_state_lbl = QtWidgets.QLabel("System: Idle")
        self._launch_state_lbl.setStyleSheet(
            "font-size: 10pt; font-weight: bold; color: #888;"
        )
        layout.addWidget(self._launch_state_lbl)

        layout.addStretch()

        self._real_warning_lbl = QtWidgets.QLabel(
            "REAL ROBOT MODE — execution disabled until safety confirmation"
        )
        self._real_warning_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self._real_warning_lbl.setStyleSheet(
            "background: #7b1fa2; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px; font-size: 10pt;"
        )
        self._real_warning_lbl.setVisible(False)
        layout.addWidget(self._real_warning_lbl)

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
        self._unit_combo.currentTextChanged.connect(self._on_unit_changed)
        self._mode_combo.currentTextChanged.connect(self._on_mode_combo_changed)

        # LaunchManager signals
        self._launch_manager.state_changed.connect(self._on_launch_state_changed)
        self._launch_manager.log_line.connect(self._append_launch_log)
        self._launch_manager.stop_complete.connect(self._on_stop_complete)

    def _start_ros(self) -> None:
        """Start the ROS node thread. No subscriptions until a mode is started."""
        self._update_topic_labels()

        def ros_spin():
            rclpy.init()
            node = GP7RosNode(self._config)
            self._ros_node = node
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
    def _on_mode_combo_changed(self, mode: str) -> None:
        """Selecting a mode only stores it as pending — no subscription yet."""
        self._pending_mode = mode
        self._mode = mode

    @Slot()
    def _on_start_clicked(self) -> None:
        """Start the selected mode: confirmation for real, then launch."""
        selected = self._mode_combo.currentText()
        if selected == "none":
            return

        # Guard: prevent double-click while a launch is running
        if self._launch_manager.is_running:
            print(f"[GUI] Cannot start: a launch is already running.")
            return

        # Disable buttons immediately to prevent double-click
        self._start_btn.setEnabled(False)
        self._stop_btn.setEnabled(False)

        if selected == "real":
            reply = QtWidgets.QMessageBox.question(
                self,
                "Confirm Real Robot Mode",
                "You are about to start REAL ROBOT mode.\n\n"
                "The robot will be commanded. Continue?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if reply != QtWidgets.QMessageBox.Yes:
                self._update_button_states(self._launch_manager.state.name.lower())
                return

        # Queue the launch — will fire in _on_stop_complete
        self._pending_launch = selected
        self._stop_reason = "before_launch"
        print(f"[GUI] _on_start_clicked: pending_launch={self._pending_launch} stop_reason={self._stop_reason} mode={selected}")

        self._reset_all_displays()
        self._set_all_indicators_gray()

        print(f"[GUI] Calling stop() before starting {selected}...")
        self._launch_manager.stop(timeout=9.0)
        # Launch fires in _on_stop_complete after stop finishes

    @Slot()
    def _on_stop_clicked(self) -> None:
        """Stop the current system — stop runs asynchronously."""
        self._stop_reason = "manual"
        self._pending_launch = None
        print(f"[GUI] _on_stop_clicked: stop_reason={self._stop_reason} pending_launch={self._pending_launch}")
        self._start_btn.setEnabled(False)
        self._stop_btn.setEnabled(False)
        print(f"[GUI] Calling stop() (manual)...")
        self._launch_manager.stop(timeout=9.0)

    @Slot()
    def _on_stop_complete(self) -> None:
        """
        Called when LaunchManager finishes stopping.
        Decides whether to launch a pending mode or go idle.
        """
        stop_reason = self._stop_reason
        pending = self._pending_launch
        print(f"[GUI] _on_stop_complete: stop_reason={stop_reason} pending_launch={pending}")

        # If we're switching modes, clear subscriptions from the old mode
        if self._ros_node:
            self._ros_node._teardown_subscriptions()

        if stop_reason == "before_launch" and pending in ("sim", "real"):
            # This stop was part of a start-switch flow — proceed with launch
            print(f"[GUI] Stop complete, proceeding to launch {pending}...")
            self._pending_launch = None
            self._stop_reason = None
            self._do_launch(pending)
        else:
            # Pure stop — go idle
            self._pending_launch = None
            self._stop_reason = None
            self._running_mode = "none"
            self._mode = "none"
            self._mode_combo.setCurrentText("none")
            self._real_warning_lbl.setVisible(False)
            self._reset_all_displays()
            self._set_all_indicators_gray()
            self._update_status_visibility()
            self._update_topic_labels()
            self._launch_state_lbl.setText("System: Idle")
            self._launch_state_lbl.setStyleSheet(
                "font-size: 10pt; font-weight: bold; color: #888;"
            )
            self._start_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)
            print("[GUI] Stop complete, GUI is now idle.")

    def _do_launch(self, mode: str) -> None:
        """
        Actually perform the launch for the given mode.
        Called from _on_stop_complete after the previous system has fully stopped.
        """
        print(f"[GUI] _do_launch({mode}): running_mode={self._running_mode} pending={self._pending_launch}")

        self._running_mode = mode
        self._mode = mode
        self._real_warning_lbl.setVisible(mode == "real")

        self._launch_state_lbl.setText(f"System: {mode.upper()} launching...")
        self._launch_state_lbl.setStyleSheet(
            "font-size: 10pt; font-weight: bold; color: #ff9800;"
        )
        self._start_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)

        # Configure ROS subscriptions for this mode
        if self._ros_node:
            self._ros_node.switch_mode(mode)
        self._update_status_visibility()
        self._update_topic_labels()
        print(f"[GUI] ROS subscriptions configured for {mode}.")

        # Launch the external bringup
        cfg = self._config[mode]
        if cfg.get("launch_package"):
            cmd_str = " ".join(
                ["ros2", "launch", cfg["launch_package"], cfg["launch_file"]]
                + [f"{k}:={v}" for k, v in cfg.get("launch_args", {}).items()]
            )
            print(f"[GUI] Launch command: {cmd_str}")
            self._launch_manager.launch(
                cfg["launch_package"],
                cfg["launch_file"],
                cfg.get("launch_args"),
            )

    @Slot(str)
    def _on_launch_state_changed(self, state: str) -> None:
        """Update UI based on LaunchManager state."""
        print(f"[GUI] _on_launch_state_changed({state}): running_mode={self._running_mode} stop_reason={self._stop_reason} pending={self._pending_launch}")
        self._update_button_states(state)
        self._update_state_label(state)

    def _update_button_states(self, state: str) -> None:
        """Update button enabled state based on LaunchManager state."""
        if state == "running":
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)
        elif state in ("idle", "stopped", "failed", "launching"):
            # These states are handled by _on_stop_complete for actual enabling
            # For now, keep both disabled — _on_stop_complete will re-enable Start
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(False)

    def _update_state_label(self, state: str) -> None:
        """Update the launch state label text and color."""
        rm = self._running_mode or "?"
        state_styles = {
            "idle":     ("System: Idle",                   "#888888"),
            "launching":(f"System: {rm.upper()} launching...",  "#ff9800"),
            "running":  (f"System: {rm.upper()} running",        "#4caf50"),
            "failed":   ("System: Launch failed",                "#f44336"),
            "stopped":  ("System: Idle",                         "#888888"),
        }
        text, color = state_styles.get(
            state, (f"System: {state}", "#888888")
        )
        self._launch_state_lbl.setText(text)
        self._launch_state_lbl.setStyleSheet(
            f"font-size: 10pt; font-weight: bold; color: {color};"
        )

    def _append_launch_log(self, line: str) -> None:
        """Append a line from the launch process to the log (stored for debug)."""
        pass  # Future: QTextEdit log widget


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
            return  # Silently ignore — will show "TF not available" on next poll if still needed
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
        if self._mode == "none":
            self._status_stack.setCurrentIndex(-1)  # hide
        elif self._mode == "sim":
            self._status_stack.setCurrentIndex(0)
        else:
            self._status_stack.setCurrentIndex(1)

    def _update_topic_labels(self) -> None:
        cfg = self._config.get(self._mode, self._config.get("none", {}))
        self._topic_labels["js_topic"].setText(cfg.get("joint_states_topic") or "—")
        self._topic_labels["rs_topic"].setText(cfg.get("robot_status_topic") or "—")
        self._topic_labels["cs_topic"].setText(cfg.get("controller_state_topic") or "—")
        self._topic_labels["pp_topic"].setText(cfg.get("planned_path_topic") or "—")

    def _set_all_indicators_gray(self) -> None:
        for indicator in self._topic_alive.values():
            indicator.setStyleSheet("color: #555; font-size: 10pt;")

    def _reset_all_displays(self) -> None:
        """Clear all live display values back to '—' after stop."""
        for cell in self._joint_cells.values():
            cell.setText("—")
        for cell in self._cs_actual_cells.values():
            cell.setText("—")
        for cell in self._cs_error_cells.values():
            cell.setText("—")
        for cell in self._rs_cells.values():
            cell.setText("—")
            cell.setStyleSheet(
                "background: #1e1e1e; color: #888; "
                "border: 1px solid #333; border-radius: 4px; "
                "padding: 2px; font-size: 9pt;"
            )
        for cell in self._pose_cells.values():
            cell.setText("—")
        self._path_label.setText("Planned path: — pose(s)")
        self._tf_status_lbl.setText("TF inactive: mode none")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self._launch_manager.stop(timeout=3.0)
        if self._ros_node:
            self._ros_node.get_logger().info("[gp7_gui] Shutting down...")
        event.accept()


# ──────────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description="GP7 Robot GUI — Phase 1.6")
    parser.add_argument(
        "--mode", default="none", choices=["none", "sim", "real"],
        help="Initial selected mode (default: none)"
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
