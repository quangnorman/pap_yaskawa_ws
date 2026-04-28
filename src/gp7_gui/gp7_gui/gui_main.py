"""
gp7_gui — GP7 Robot GUI
Phase 3: Joint Execute + Cartesian Move

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
from typing import Dict, List, Optional, Tuple

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from ament_index_python.packages import get_package_share_directory

from sensor_msgs.msg import JointState
from nav_msgs.msg import Path
try:
    from control_msgs.msg import JointTrajectoryControllerState
    HAS_CONTROLLER_STATE = True
except ImportError:
    HAS_CONTROLLER_STATE = False
try:
    from industrial_msgs.msg import RobotStatus
    HAS_ROBOT_STATUS = True
    print("[GUI] RobotStatus: industrial_msgs (BEST_EFFORT capable) — REAL MODE WILL WORK")
except ImportError:
    HAS_ROBOT_STATUS = False
    print("[GUI] RobotStatus: NOT AVAILABLE — industrial_msgs not installed, real robot_status subscription SKIPPED")

# QoS profiles
REAL_ROBOT_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    depth=10,
)

from geometry_msgs.msg import TransformStamped
try:
    from tf2_ros import Buffer, TransformListener
    HAS_TF2 = True
except ImportError:
    HAS_TF2 = False

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QObject, Signal, Slot

from gp7_gui.launch_manager import LaunchManager, LaunchState

try:
    from gp7_task_executor_msgs.srv import MoveToJointTarget
    HAS_MOVE_JOINT_TARGET = True
except ImportError:
    HAS_MOVE_JOINT_TARGET = False

try:
    from gp7_task_executor_msgs.srv import MoveToCartesianTarget
    HAS_MOVE_CARTESIAN_TARGET = True
except ImportError:
    HAS_MOVE_CARTESIAN_TARGET = False


# Topic type reference (verify with: ros2 topic type /topic_name)
# /robot1/joint_states       -> sensor_msgs/msg/JointState          (sensor_msgs)
# /robot1/robot_status       -> yaskawa_robot_controller_msgs/msg/RobotStatus (moto_ros2_interface)
# /arm_controller/state     -> control_msgs/msg/JointTrajectoryControllerState  (control_msgs)
# /task_executor/planned_tool_path -> nav_msgs/msg/Path               (nav_msgs)
#
# To check actual types on your system:
#   ros2 topic type /robot1/joint_states
#   ros2 topic type /robot1/robot_status
#   ros2 topic type /arm_controller/state
#   ros2 topic type /task_executor/planned_tool_path

# Joint name mapping: maps actual names from /robot1/joint_states to canonical names.
# If the real robot publishes "joint_s", "joint_t", etc. instead of "joint_1", "joint_6",
# add them here. Keys = names from the message, Values = canonical names expected by GUI.
# Leave empty {} if the robot already uses "joint_1".."joint_6".
JOINT_NAME_MAP: Dict[str, str] = {}


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


def rpy_to_quaternion(roll: float, pitch: float, yaw: float) -> Tuple[float, float, float, float]:
    """Convert roll, pitch, yaw (radians) to quaternion (ROS x,y,z,w order)."""
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    qw = cr * cp * cy + sr * sp * sy
    return qx, qy, qz, qw


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


class JointPlanSignals(QObject):
    planning_started = Signal()
    planning_finished = Signal(bool, str)
    button_enabled_changed = Signal(bool)


class CartesianPlanSignals(QObject):
    planning_started = Signal()
    planning_finished = Signal(bool, str)
    button_enabled_changed = Signal(bool)


# ──────────────────────────────────────────────────────────────────────────────
#  Joint Plan Bridge — service client for /move_to_joint_target
# ──────────────────────────────────────────────────────────────────────────────

class JointPlanBridge:
    """
    Service client for /move_to_joint_target.
    Lives in the ROS node thread; communicates with Qt via JointPlanSignals.
    """

    SERVICE_NAME = "/move_to_joint_target"
    JOINT_NAMES = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]

    def __init__(self, node: Node):
        self._node = node
        self._signals = JointPlanSignals()
        self._client = None
        self._plan_pending = False
        self._execute_pending = False

    @property
    def signals(self) -> JointPlanSignals:
        return self._signals

    def _ensure_client(self) -> bool:
        if self._client is None:
            if not HAS_MOVE_JOINT_TARGET:
                self._node.get_logger().error("[gp7_gui] MoveToJointTarget msg not available")
                return False
            self._node.get_logger().info(f"[gp7_gui] Creating client for {self.SERVICE_NAME}")
            self._client = self._node.create_client(MoveToJointTarget, self.SERVICE_NAME)
        return self._client.service_is_ready()

    def call_plan(self, positions_rad: List[float]) -> None:
        if self._plan_pending or self._execute_pending:
            return
        if not self._ensure_client():
            self._node.get_logger().warn("[gp7_gui] Service not ready — waiting...")
            if not self._client.wait_for_service(timeout_sec=2.0):
                self._node.get_logger().error("[gp7_gui] Service /move_to_joint_target not available within 2s")
                self._signals.planning_finished.emit(False, "Service unavailable")
                return
            # Re-check after wait
            if not self._ensure_client():
                self._signals.planning_finished.emit(False, "Service unavailable")
                return

        self._plan_pending = True
        self._signals.planning_started.emit()
        self._signals.button_enabled_changed.emit(False)

        req = MoveToJointTarget.Request()
        req.joint_names = self.JOINT_NAMES
        req.positions = positions_rad
        req.execute = False

        self._node.get_logger().info(
            f"[gp7_gui] Calling /move_to_joint_target: joints={req.joint_names}, "
            f"positions={req.positions}, execute={req.execute}"
        )

        future = self._client.call_async(req)
        future.add_done_callback(self._on_response(future, is_execute=False))

    def call_execute(self, positions_rad: List[float]) -> None:
        if self._plan_pending or self._execute_pending:
            return
        if not self._ensure_client():
            self._node.get_logger().warn("[gp7_gui] Service not ready — waiting...")
            if not self._client.wait_for_service(timeout_sec=2.0):
                self._node.get_logger().error("[gp7_gui] Service /move_to_joint_target not available within 2s")
                self._signals.planning_finished.emit(False, "Service unavailable")
                return
            if not self._ensure_client():
                self._signals.planning_finished.emit(False, "Service unavailable")
                return

        self._execute_pending = True
        self._signals.planning_started.emit()
        self._signals.button_enabled_changed.emit(False)

        req = MoveToJointTarget.Request()
        req.joint_names = self.JOINT_NAMES
        req.positions = positions_rad
        req.execute = True

        self._node.get_logger().info(
            f"[gp7_gui] Calling /move_to_joint_target EXECUTE: joints={req.joint_names}, "
            f"positions={req.positions}, execute={req.execute}"
        )

        future = self._client.call_async(req)
        future.add_done_callback(self._on_response(future, is_execute=True))

    def _on_response(self, future, is_execute: bool = False):
        def callback(_future):
            if is_execute:
                self._execute_pending = False
            else:
                self._plan_pending = False
            try:
                response = _future.result()
                if response is None:
                    self._node.get_logger().error("[gp7_gui] Service response is None")
                    self._signals.planning_finished.emit(False, "Service unavailable")
                else:
                    self._node.get_logger().info(
                        f"[gp7_gui] Service response: success={response.success}, message={response.message}"
                    )
                    self._signals.planning_finished.emit(
                        bool(response.success), str(response.message)
                    )
            except Exception as e:
                self._node.get_logger().error(f"[gp7_gui] Service call failed: {e}")
                self._signals.planning_finished.emit(False, f"Service call failed: {e}")
            finally:
                self._signals.button_enabled_changed.emit(True)

        return callback


# ──────────────────────────────────────────────────────────────────────────────
#  Cartesian Bridge — service client for /move_to_cartesian_target
# ──────────────────────────────────────────────────────────────────────────────

class CartesianBridge:
    """
    Service client for /move_to_cartesian_target.
    Lives in the ROS node thread; communicates with Qt via CartesianPlanSignals.
    """

    SERVICE_NAME = "/move_to_cartesian_target"
    FIXED_ROLL = math.pi    # 180 deg
    FIXED_PITCH = 0.0
    FIXED_YAW = 0.0

    def __init__(self, node: Node):
        self._node = node
        self._signals = CartesianPlanSignals()
        self._client = None
        self._plan_pending = False
        self._execute_pending = False

    @property
    def signals(self) -> CartesianPlanSignals:
        return self._signals

    def _ensure_client(self) -> bool:
        if self._client is None:
            if not HAS_MOVE_CARTESIAN_TARGET:
                self._node.get_logger().error("[gp7_gui] MoveToCartesianTarget msg not available")
                return False
            self._node.get_logger().info(f"[gp7_gui] Creating client for {self.SERVICE_NAME}")
            self._client = self._node.create_client(MoveToCartesianTarget, self.SERVICE_NAME)
        return self._client.service_is_ready()

    def call_plan(self, x_m: float, y_m: float, z_m: float, frame_id: str) -> None:
        self._do_call(x_m, y_m, z_m, frame_id, execute=False, is_execute=False)

    def call_execute(self, x_m: float, y_m: float, z_m: float, frame_id: str) -> None:
        self._do_call(x_m, y_m, z_m, frame_id, execute=True, is_execute=True)

    def _do_call(self, x_m: float, y_m: float, z_m: float, frame_id: str, execute: bool, is_execute: bool) -> None:
        if self._plan_pending or self._execute_pending:
            return
        if not self._ensure_client():
            self._node.get_logger().warn("[gp7_gui] Cartesian service not ready — waiting...")
            if not self._client.wait_for_service(timeout_sec=2.0):
                self._node.get_logger().error("[gp7_gui] Service /move_to_cartesian_target not available within 2s")
                self._signals.planning_finished.emit(False, "Service unavailable")
                return
            if not self._ensure_client():
                self._signals.planning_finished.emit(False, "Service unavailable")
                return

        roll = self.FIXED_ROLL
        pitch = self.FIXED_PITCH
        yaw = self.FIXED_YAW
        qx, qy, qz, qw = rpy_to_quaternion(roll, pitch, yaw)
        x_mm = x_m * 1000.0
        y_mm = y_m * 1000.0
        z_mm = z_m * 1000.0

        req = MoveToCartesianTarget.Request()
        req.x = x_m
        req.y = y_m
        req.z = z_m
        req.frame_id = frame_id
        req.execute = execute

        print(f"DEBUG Cartesian service: {self.SERVICE_NAME}")
        print(f"DEBUG Cartesian input mm: {x_mm:.3f} {y_mm:.3f} {z_mm:.3f}")
        print(f"DEBUG Cartesian converted m: {x_m:.6f} {y_m:.6f} {z_m:.6f}")
        print(f"DEBUG Cartesian fixed rpy: {roll:.6f} {pitch:.6f} {yaw:.6f}")
        print(f"DEBUG Cartesian quaternion: {qx:.6f} {qy:.6f} {qz:.6f} {qw:.6f}")
        print(f"DEBUG Cartesian execute: {execute}")
        print(f"DEBUG Cartesian request: x={req.x}, y={req.y}, z={req.z}, frame_id={req.frame_id}, execute={req.execute}")

        self._node.get_logger().info(
            f"[gp7_gui] Calling /move_to_cartesian_target: "
            f"x={x_m:.4f} y={y_m:.4f} z={z_m:.4f} frame={frame_id} "
            f"rpy=({roll:.4f},{pitch:.4f},{yaw:.4f}) q=({qx:.4f},{qy:.4f},{qz:.4f},{qw:.4f}) "
            f"execute={execute}"
        )

        if is_execute:
            self._execute_pending = True
        else:
            self._plan_pending = True
        self._signals.planning_started.emit()
        self._signals.button_enabled_changed.emit(False)

        future = self._client.call_async(req)
        future.add_done_callback(self._on_response(future, is_execute))

    def _on_response(self, future, is_execute: bool):
        def callback(_future):
            if is_execute:
                self._execute_pending = False
            else:
                self._plan_pending = False
            try:
                response = _future.result()
                if response is None:
                    self._node.get_logger().error("[gp7_gui] Cartesian service response is None")
                    print("DEBUG Cartesian response success: False")
                    print("DEBUG Cartesian response message: Service response is None")
                    self._signals.planning_finished.emit(False, "Service unavailable")
                else:
                    print(f"DEBUG Cartesian response success: {response.success}")
                    print(f"DEBUG Cartesian response message: {response.message}")
                    self._node.get_logger().info(
                        f"[gp7_gui] Cartesian response: success={response.success}, "
                        f"fraction={response.fraction}, message={response.message}"
                    )
                    self._signals.planning_finished.emit(
                        bool(response.success), str(response.message)
                    )
            except Exception as e:
                self._node.get_logger().error(f"[gp7_gui] Cartesian service call failed: {e}")
                print(f"DEBUG Cartesian response success: False")
                print(f"DEBUG Cartesian response message: Service call failed: {e}")
                self._signals.planning_finished.emit(False, f"Service call failed: {e}")
            finally:
                self._signals.button_enabled_changed.emit(True)

        return callback


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

        # All stale at start — indicators will go green only when first message arrives
        self._js_stale = True
        self._cs_stale = True
        self._rs_stale = True

        # TF2 — lookup base_link → tool0
        if HAS_TF2:
            self._tf_buffer = Buffer()
            self._tf_listener = TransformListener(self._tf_buffer, self)
        else:
            self._tf_buffer = None

        self._tf_pose_cache: Dict[str, float] = {}

        # Joint plan service bridge
        self._joint_plan_bridge: Optional[JointPlanBridge] = None
        if HAS_MOVE_JOINT_TARGET:
            self._joint_plan_bridge = JointPlanBridge(self)

        # Cartesian plan service bridge
        self._cartesian_bridge: Optional[CartesianBridge] = None
        if HAS_MOVE_CARTESIAN_TARGET:
            self._cartesian_bridge = CartesianBridge(self)

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
        self._setup_subscriptions(cfg, mode)

    def _setup_subscriptions(self, cfg: Dict, mode: str) -> None:
        self.get_logger().info(f"[gp7_gui] Setting up subscriptions for mode={mode} cfg={cfg}")
        is_real = (mode == "real")

        js_topic = cfg.get("joint_states_topic", "")
        if js_topic:
            qos = REAL_ROBOT_QOS if is_real else 10
            print(f"[GUI] _setup_subscriptions: creating joint_states subscription to topic='{js_topic}' is_real={is_real} qos={qos}")
            self._js_sub = self.create_subscription(
                JointState, js_topic, self._on_joint_states, qos
            )
            print(f"[GUI] _setup_subscriptions: joint_states sub={self._js_sub} topic='{js_topic}'")
            if is_real:
                print(f"[GUI] real joint_states QoS = BEST_EFFORT")

        if cfg.get("controller_state_topic") and HAS_CONTROLLER_STATE:
            cs_topic = cfg["controller_state_topic"]
            print(f"[GUI] _setup_subscriptions: creating controller_state subscription to topic='{cs_topic}'")
            self._cs_sub = self.create_subscription(
                JointTrajectoryControllerState,
                cs_topic,
                self._on_controller_state, 10,
            )
            print(f"[GUI] _setup_subscriptions: controller_state sub={self._cs_sub} topic='{cs_topic}'")

        if cfg.get("robot_status_topic") and HAS_ROBOT_STATUS:
            rs_topic = cfg["robot_status_topic"]
            qos = REAL_ROBOT_QOS if is_real else 10
            print(f"[GUI] _setup_subscriptions: creating robot_status subscription to topic='{rs_topic}' is_real={is_real} qos={qos}")
            self._rs_sub = self.create_subscription(
                RobotStatus,
                rs_topic,
                self._on_robot_status, qos,
            )
            print(f"[GUI] _setup_subscriptions: robot_status sub={self._rs_sub} topic='{rs_topic}'")
            if is_real:
                print(f"[GUI] real robot_status QoS = BEST_EFFORT")

        pp_topic = cfg.get("planned_path_topic", "")
        if pp_topic:
            qos = REAL_ROBOT_QOS if is_real else 10
            print(f"[GUI] _setup_subscriptions: creating planned_path subscription to topic='{pp_topic}' is_real={is_real} qos={qos}")
            self._pp_sub = self.create_subscription(
                Path, pp_topic, self._on_planned_path, qos
            )
            print(f"[GUI] _setup_subscriptions: planned_path sub={self._pp_sub} topic='{pp_topic}'")

        # Reset to True so indicators go gray until first message arrives
        self._js_stale = True
        self._cs_stale = True
        self._rs_stale = True

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
        print(f"[CALLBACK] joint_states received name={msg.name} position={msg.position}")
        self._js_stale = False
        self._signals.topic_status_updated.emit("joint_states", True)
        if not msg.name or not msg.position:
            return
        # Map actual names to canonical names using JOINT_NAME_MAP
        joints = {}
        for name, pos in zip(msg.name, msg.position):
            canonical = JOINT_NAME_MAP.get(name, name)
            joints[canonical] = pos
        print(f"[CALLBACK] joint_states mapped joints={joints}")
        self._signals.joints_updated.emit(joints)

    def _on_controller_state(self, msg: JointTrajectoryControllerState) -> None:
        self._cs_stale = False
        self._signals.topic_status_updated.emit("controller_state", True)
        actual = list(msg.actual.positions) if msg.actual.positions else []
        error = list(msg.error.positions) if msg.error.positions else []
        self._signals.controller_state_updated.emit(actual, error)

    def _on_robot_status(self, msg: RobotStatus) -> None:
        print(f"[CALLBACK] robot_status received msg={msg}")
        self._rs_stale = False
        self._signals.topic_status_updated.emit("robot_status", True)
        # industrial_msgs.TriState.val: 1=TRUE, 0=FALSE, -1=UNKNOWN
        self._signals.robot_status_updated.emit({
            "drives_powered": msg.drives_powered.val == 1,
            "motion_possible": msg.motion_possible.val == 1,
            "in_motion": msg.in_motion.val == 1,
            "in_error": msg.in_error.val == 1,
        })

    def _on_planned_path(self, msg: Path) -> None:
        print(f"[CALLBACK] planned_path received poses={len(msg.poses)}")
        self._signals.planned_path_updated.emit(len(msg.poses))

    # ── stale monitoring ───────────────────────────────────────────────────

    def _check_js_stale(self) -> None:
        # Only emit when the state CHANGES to stale (message stopped arriving)
        if self._js_stale and self._js_sub:
            self._signals.topic_status_updated.emit("joint_states", False)

    def _check_cs_stale(self) -> None:
        if self._cs_stale and self._cs_sub:
            self._signals.topic_status_updated.emit("controller_state", False)

    def _check_rs_stale(self) -> None:
        if self._rs_stale and self._rs_sub:
            self._signals.topic_status_updated.emit("robot_status", False)

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
            self._tf_pose_cache = {
                "tx": t.x, "ty": t.y, "tz": t.z,
                "roll": roll, "pitch": pitch, "yaw": yaw,
                "available": True,
            }
            self._signals.tf_pose_updated.emit(self._tf_pose_cache)
        except Exception:
            pass  # Silently ignore — "TF not available" only shown when mode is none

    def call_joint_plan(self, positions_rad: List[float]) -> None:
        """Call the /move_to_joint_target service with execute=False."""
        if self._joint_plan_bridge:
            self._joint_plan_bridge.call_plan(positions_rad)

    def get_joint_plan_signals(self) -> Optional[JointPlanSignals]:
        """Return the bridge signals object for connecting to Qt slots."""
        if self._joint_plan_bridge:
            return self._joint_plan_bridge.signals
        return None

    def call_joint_execute(self, positions_rad: List[float]) -> None:
        """Call the /move_to_joint_target service with execute=True."""
        if self._joint_plan_bridge:
            self._joint_plan_bridge.call_execute(positions_rad)

    def call_cartesian_plan(self, x_m: float, y_m: float, z_m: float, frame_id: str) -> None:
        """Call the /move_to_cartesian_target service with execute=False."""
        if self._cartesian_bridge:
            self._cartesian_bridge.call_plan(x_m, y_m, z_m, frame_id)

    def call_cartesian_execute(self, x_m: float, y_m: float, z_m: float, frame_id: str) -> None:
        """Call the /move_to_cartesian_target service with execute=True."""
        if self._cartesian_bridge:
            self._cartesian_bridge.call_execute(x_m, y_m, z_m, frame_id)

    def get_cartesian_signals(self) -> Optional[CartesianPlanSignals]:
        """Return the cartesian bridge signals object for connecting to Qt slots."""
        if self._cartesian_bridge:
            return self._cartesian_bridge.signals
        return None


# ──────────────────────────────────────────────────────────────────────────────
#  Main Window
# ──────────────────────────────────────────────────────────────────────────────

class GP7MainWindow(QtWidgets.QMainWindow):
    """Phase 3 GUI — Joint Execute + Cartesian Move."""

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

        self.setWindowTitle("GP7 Robot GUI — Phase 3: Joint Execute + Cartesian")
        self.setMinimumSize(960, 900)
        self._setup_ui()
        self._update_joint_target_labels()
        self._update_cartesian_rpy_display()
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
        top_layout.addWidget(self._build_joint_plan_panel())
        top_layout.addWidget(self._build_cartesian_panel())
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

        self._refresh_topics_btn = QtWidgets.QPushButton("Refresh topics")
        self._refresh_topics_btn.setStyleSheet(
            "background: #1565c0; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 16px;"
        )
        self._refresh_topics_btn.clicked.connect(self._on_refresh_topics_clicked)
        layout.addWidget(self._refresh_topics_btn)

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

    def _build_joint_plan_panel(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Joint Target")
        self._joint_plan_group = group
        layout = QtWidgets.QGridLayout(group)

        self._target_inputs: List[QtWidgets.QLineEdit] = []
        self._joint_target_labels: List[QtWidgets.QLabel] = []

        for col, name in enumerate(self.JOINT_NAMES):
            lbl = QtWidgets.QLabel(f"{name} (rad):")
            lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
            lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            layout.addWidget(lbl, 0, col)
            self._joint_target_labels.append(lbl)

            le = QtWidgets.QLineEdit()
            le.setPlaceholderText("0.000")
            le.setAlignment(QtCore.Qt.AlignCenter)
            le.setStyleSheet(
                "background: #1a1a2e; color: #fff; "
                "border: 1px solid #444; border-radius: 4px; "
                "padding: 3px; font-family: monospace; font-size: 9pt;"
            )
            le.setMinimumWidth(80)
            le.returnPressed.connect(self._on_plan_clicked)
            layout.addWidget(le, 1, col)
            self._target_inputs.append(le)

        # Buttons row
        btn_layout = QtWidgets.QHBoxLayout()

        self._fill_joints_btn = QtWidgets.QPushButton("Fill current joints")
        self._fill_joints_btn.setStyleSheet(
            "background: #1565c0; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 16px;"
        )
        self._fill_joints_btn.clicked.connect(self._on_fill_joints_clicked)
        btn_layout.addWidget(self._fill_joints_btn)

        self._plan_btn = QtWidgets.QPushButton("Plan only")
        self._plan_btn.setStyleSheet(
            "background: #00695c; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 20px;"
        )
        self._plan_btn.clicked.connect(self._on_plan_clicked)
        self._plan_btn.setEnabled(False)
        btn_layout.addWidget(self._plan_btn)

        self._execute_btn = QtWidgets.QPushButton("Execute")
        self._execute_btn.setStyleSheet(
            "background: #e65100; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 20px;"
        )
        self._execute_btn.clicked.connect(self._on_execute_clicked)
        self._execute_btn.setEnabled(False)
        btn_layout.addWidget(self._execute_btn)

        btn_layout.addStretch()

        # Status label
        self._plan_status_lbl = QtWidgets.QLabel("—")
        self._plan_status_lbl.setStyleSheet(
            "font-size: 9pt; color: #888; font-style: italic;"
        )
        btn_layout.addWidget(self._plan_status_lbl)

        layout.addLayout(btn_layout, 2, 0, 1, 6)

        # Safety checkbox row
        safety_layout = QtWidgets.QHBoxLayout()
        safety_layout.addStretch()
        self._joint_safety_chk = QtWidgets.QCheckBox(
            "I understand this will move the real robot"
        )
        self._joint_safety_chk.setStyleSheet("color: #ff8a65; font-size: 9pt;")
        self._joint_safety_chk.setVisible(False)
        self._joint_safety_chk.stateChanged.connect(self._on_joint_safety_changed)
        safety_layout.addWidget(self._joint_safety_chk)
        safety_layout.addStretch()
        layout.addLayout(safety_layout, 3, 0, 1, 6)

        return group

    def _build_cartesian_panel(self) -> QtWidgets.QGroupBox:
        group = QtWidgets.QGroupBox("Cartesian Target")
        self._cartesian_group = group
        layout = QtWidgets.QGridLayout(group)

        # X, Y, Z (mm) — row 0
        x_lbl = QtWidgets.QLabel("X (mm):")
        x_lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
        x_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(x_lbl, 0, 0)

        self._cart_x_input = QtWidgets.QLineEdit()
        self._cart_x_input.setPlaceholderText("0.000")
        self._cart_x_input.setStyleSheet(
            "background: #1a1a2e; color: #fff; "
            "border: 1px solid #444; border-radius: 4px; "
            "padding: 3px; font-family: monospace; font-size: 9pt;"
        )
        self._cart_x_input.setMinimumWidth(100)
        self._cart_x_input.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self._cart_x_input, 0, 1)

        y_lbl = QtWidgets.QLabel("Y (mm):")
        y_lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
        y_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(y_lbl, 0, 2)

        self._cart_y_input = QtWidgets.QLineEdit()
        self._cart_y_input.setPlaceholderText("0.000")
        self._cart_y_input.setStyleSheet(
            "background: #1a1a2e; color: #fff; "
            "border: 1px solid #444; border-radius: 4px; "
            "padding: 3px; font-family: monospace; font-size: 9pt;"
        )
        self._cart_y_input.setMinimumWidth(100)
        self._cart_y_input.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self._cart_y_input, 0, 3)

        z_lbl = QtWidgets.QLabel("Z (mm):")
        z_lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
        z_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(z_lbl, 0, 4)

        self._cart_z_input = QtWidgets.QLineEdit()
        self._cart_z_input.setPlaceholderText("0.000")
        self._cart_z_input.setStyleSheet(
            "background: #1a1a2e; color: #fff; "
            "border: 1px solid #444; border-radius: 4px; "
            "padding: 3px; font-family: monospace; font-size: 9pt;"
        )
        self._cart_z_input.setMinimumWidth(100)
        self._cart_z_input.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self._cart_z_input, 0, 5)

        # R, P, Y (fixed, read-only) — row 1
        roll_lbl = QtWidgets.QLabel("Roll (fixed):")
        roll_lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
        roll_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(roll_lbl, 1, 0)

        self._cart_roll_lbl = QtWidgets.QLabel("3.1416 (rad)")
        self._cart_roll_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self._cart_roll_lbl.setStyleSheet(
            "background: #1e1e2e; color: #ce93d8; "
            "border: 1px solid #333; border-radius: 4px; "
            "padding: 3px; font-family: monospace; font-size: 9pt;"
        )
        layout.addWidget(self._cart_roll_lbl, 1, 1)

        pitch_lbl = QtWidgets.QLabel("Pitch (fixed):")
        pitch_lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
        pitch_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(pitch_lbl, 1, 2)

        self._cart_pitch_lbl = QtWidgets.QLabel("0.0000 (rad)")
        self._cart_pitch_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self._cart_pitch_lbl.setStyleSheet(
            "background: #1e1e2e; color: #ce93d8; "
            "border: 1px solid #333; border-radius: 4px; "
            "padding: 3px; font-family: monospace; font-size: 9pt;"
        )
        layout.addWidget(self._cart_pitch_lbl, 1, 3)

        yaw_lbl = QtWidgets.QLabel("Yaw (fixed):")
        yaw_lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
        yaw_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(yaw_lbl, 1, 4)

        self._cart_yaw_lbl = QtWidgets.QLabel("0.0000 (rad)")
        self._cart_yaw_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self._cart_yaw_lbl.setStyleSheet(
            "background: #1e1e2e; color: #ce93d8; "
            "border: 1px solid #333; border-radius: 4px; "
            "padding: 3px; font-family: monospace; font-size: 9pt;"
        )
        layout.addWidget(self._cart_yaw_lbl, 1, 5)

        # Frame ID row — row 2
        frame_lbl = QtWidgets.QLabel("Frame ID:")
        frame_lbl.setStyleSheet("font-size: 9pt; color: #aaa;")
        frame_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(frame_lbl, 2, 0)

        self._cart_frame_input = QtWidgets.QLineEdit("base_link")
        self._cart_frame_input.setStyleSheet(
            "background: #1a1a2e; color: #fff; "
            "border: 1px solid #444; border-radius: 4px; "
            "padding: 3px; font-family: monospace; font-size: 9pt;"
        )
        self._cart_frame_input.setMaximumWidth(120)
        self._cart_frame_input.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self._cart_frame_input, 2, 1, 1, 2)

        # Buttons row — row 3
        cart_btn_layout = QtWidgets.QHBoxLayout()

        self._fill_cart_btn = QtWidgets.QPushButton("Fill current tool0")
        self._fill_cart_btn.setStyleSheet(
            "background: #1565c0; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 16px;"
        )
        self._fill_cart_btn.clicked.connect(self._on_fill_cart_clicked)
        cart_btn_layout.addWidget(self._fill_cart_btn)

        self._cart_plan_btn = QtWidgets.QPushButton("Plan Cartesian")
        self._cart_plan_btn.setStyleSheet(
            "background: #00695c; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 20px;"
        )
        self._cart_plan_btn.clicked.connect(self._on_cart_plan_clicked)
        self._cart_plan_btn.setEnabled(False)
        cart_btn_layout.addWidget(self._cart_plan_btn)

        self._cart_execute_btn = QtWidgets.QPushButton("Execute Cartesian")
        self._cart_execute_btn.setStyleSheet(
            "background: #e65100; color: white; font-weight: bold; "
            "border-radius: 4px; padding: 6px 20px;"
        )
        self._cart_execute_btn.clicked.connect(self._on_cart_execute_clicked)
        self._cart_execute_btn.setEnabled(False)
        cart_btn_layout.addWidget(self._cart_execute_btn)

        cart_btn_layout.addStretch()

        # Cartesian status label
        self._cart_status_lbl = QtWidgets.QLabel("—")
        self._cart_status_lbl.setStyleSheet(
            "font-size: 9pt; color: #888; font-style: italic;"
        )
        cart_btn_layout.addWidget(self._cart_status_lbl)

        layout.addLayout(cart_btn_layout, 3, 0, 1, 6)

        # Safety checkbox row
        cart_safety_layout = QtWidgets.QHBoxLayout()
        cart_safety_layout.addStretch()
        self._cart_safety_chk = QtWidgets.QCheckBox(
            "I understand this will move the real robot"
        )
        self._cart_safety_chk.setStyleSheet("color: #ff8a65; font-size: 9pt;")
        self._cart_safety_chk.setVisible(False)
        self._cart_safety_chk.stateChanged.connect(self._on_cart_safety_changed)
        cart_safety_layout.addWidget(self._cart_safety_chk)
        cart_safety_layout.addStretch()
        layout.addLayout(cart_safety_layout, 4, 0, 1, 6)

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
            try:
                print("[SPIN] ROS spin thread started")
                rclpy.init()
                node = GP7RosNode(self._config)
                self._ros_node = node
                node._signals.joints_updated.connect(self._on_joints_updated)
                node._signals.controller_state_updated.connect(self._on_controller_state_updated)
                node._signals.robot_status_updated.connect(self._on_robot_status_updated)
                node._signals.planned_path_updated.connect(self._on_planned_path_updated)
                node._signals.topic_status_updated.connect(self._on_topic_status_updated)
                node._signals.tf_pose_updated.connect(self._on_tf_pose_updated)
                print("[SIGNAL] signal connections configured")
                # Connect joint plan signals
                plan_signals = node.get_joint_plan_signals()
                if plan_signals:
                    plan_signals.planning_started.connect(self._on_planning_started)
                    plan_signals.planning_finished.connect(self._on_planning_finished)
                    plan_signals.button_enabled_changed.connect(self._on_plan_btn_enabled)
                # Connect cartesian plan signals
                cart_signals = node.get_cartesian_signals()
                if cart_signals:
                    cart_signals.planning_started.connect(self._on_cart_planning_started)
                    cart_signals.planning_finished.connect(self._on_cart_planning_finished)
                    cart_signals.button_enabled_changed.connect(self._on_cart_buttons_enabled)
                print("[SPIN] ROS node spinning...")
                spin_count = 0
                while rclpy.ok():
                    rclpy.spin_once(node, timeout_sec=0.05)
                    spin_count += 1
                    if spin_count % 20 == 0:
                        print(f"[SPIN] ROS node spinning... spin_count={spin_count}")
                print(f"[SPIN] ROS spin loop ended (spin_count={spin_count})")
            except Exception as exc:
                print(f"[SPIN][ERROR] ROS spin thread crashed: {exc}")
                import traceback
                traceback.print_exc()
                self._ros_node = None

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
        self._joint_safety_chk.setChecked(False)
        self._cart_safety_chk.setChecked(False)
        # Show safety checkbox in real mode so execute is available
        self._joint_safety_chk.setVisible(selected == "real")
        self._cart_safety_chk.setVisible(selected == "real")

        print(f"[GUI] Calling stop() before starting {selected}...")
        self._launch_manager.stop(timeout=9.0)
        # Launch fires in _on_stop_complete after stop finishes

    @Slot()
    def _on_refresh_topics_clicked(self) -> None:
        """Reconfigure subscriptions for the current running mode."""
        if self._ros_node and self._running_mode != "none":
            print(f"[GUI] Refresh topics: re-subscribing for mode={self._running_mode}")
            self._ros_node.switch_mode(self._running_mode)
        else:
            print("[GUI] Refresh topics: no active mode, nothing to refresh")

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
            self._joint_safety_chk.setVisible(False)
            self._cart_safety_chk.setVisible(False)
            self._joint_safety_chk.setChecked(False)
            self._cart_safety_chk.setChecked(False)
            self._reset_all_displays()
            self._set_all_indicators_gray()
            self._update_status_visibility()
            self._update_topic_labels()
            self._launch_state_lbl.setText("System: Idle")
            self._launch_state_lbl.setStyleSheet(
                "font-size: 10pt; font-weight: bold; color: #888;"
            )
            self._tf_status_lbl.setText("TF inactive: mode none")
            self._start_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)
            self._plan_btn.setEnabled(False)
            self._execute_btn.setEnabled(False)
            self._cart_plan_btn.setEnabled(False)
            self._cart_execute_btn.setEnabled(False)
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
        self._joint_safety_chk.setVisible(mode == "real")
        self._cart_safety_chk.setVisible(mode == "real")
        self._joint_safety_chk.setChecked(False)
        self._cart_safety_chk.setChecked(False)
        self._tf_status_lbl.setText(
            "TF unavailable: base_link -> tool0"
            if mode in ("sim", "real")
            else "TF inactive: mode none"
        )

        self._launch_state_lbl.setText(f"System: {mode.upper()} launching...")
        self._launch_state_lbl.setStyleSheet(
            "font-size: 10pt; font-weight: bold; color: #ff9800;"
        )
        self._start_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)

        # Configure ROS subscriptions for this mode
        if self._ros_node is None:
            print("[GUI] ERROR: ROS node is not running — cannot switch mode")
            self._launch_state_lbl.setText("System: ERROR — ROS node not running")
            self._launch_state_lbl.setStyleSheet(
                "font-size: 10pt; font-weight: bold; color: #ff5252;"
            )
            self._start_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)
            return
        self._ros_node.switch_mode(mode)
        self._update_status_visibility()
        self._update_topic_labels()
        self._update_plan_button_enabled()
        self._update_cart_button_enabled()
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
        if state == "running":
            self._update_plan_button_enabled()
            self._update_cart_button_enabled()

    def _update_button_states(self, state: str) -> None:
        """Update button enabled state based on LaunchManager state."""
        if state == "running":
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)
            self._update_plan_button_enabled()
        elif state in ("idle", "stopped", "failed", "launching"):
            # These states are handled by _on_stop_complete for actual enabling
            # For now, keep both disabled — _on_stop_complete will re-enable Start
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(False)
            self._plan_btn.setEnabled(False)
            self._execute_btn.setEnabled(False)
            self._cart_plan_btn.setEnabled(False)
            self._cart_execute_btn.setEnabled(False)

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
        self._update_joint_target_labels()
        self._update_cartesian_rpy_display()
        self._refresh_joint_display()
        self._refresh_pose_display()

    def _update_joint_target_labels(self) -> None:
        """Update joint target labels to reflect the current angular unit."""
        unit = self._unit
        for i, label in enumerate(self._joint_target_labels):
            label.setText(f"{self.JOINT_NAMES[i]} ({unit}):")

    def _update_cartesian_rpy_display(self) -> None:
        """Update the fixed RPY display to show values in the selected unit."""
        unit = self._unit
        roll_fixed = CartesianBridge.FIXED_ROLL
        pitch_fixed = CartesianBridge.FIXED_PITCH
        yaw_fixed = CartesianBridge.FIXED_YAW
        if unit == "deg":
            self._cart_roll_lbl.setText(f"{math.degrees(roll_fixed):.1f} (deg)")
            self._cart_pitch_lbl.setText(f"{math.degrees(pitch_fixed):.1f} (deg)")
            self._cart_yaw_lbl.setText(f"{math.degrees(yaw_fixed):.1f} (deg)")
        else:
            self._cart_roll_lbl.setText(f"{roll_fixed:.4f} (rad)")
            self._cart_pitch_lbl.setText(f"{pitch_fixed:.4f} (rad)")
            self._cart_yaw_lbl.setText(f"{yaw_fixed:.4f} (rad)")

    @Slot(dict)
    def _on_joints_updated(self, joints: Dict[str, float]) -> None:
        print(f"[UI] updating joints {joints}")
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
        print(f"[UI] updating controller_state actual={actual[:3] if actual else []} error={error[:3] if error else []}")
        factor = 180.0 / math.pi if self._unit == "deg" else 1.0
        for i, name in enumerate(self.JOINT_NAMES):
            if i < len(actual):
                self._cs_actual_cells[name].setText(f"{actual[i] * factor:.3f}")
            if i < len(error):
                self._cs_error_cells[name].setText(f"{error[i] * factor:.3f}")

    @Slot(dict)
    def _on_robot_status_updated(self, status: Dict) -> None:
        print(f"[UI] updating robot_status {status}")
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
        print(f"[UI] updating planned_path num_poses={num_poses}")
        self._path_label.setText(f"Planned path: {num_poses} pose(s)")

    @Slot(str, bool)
    def _on_topic_status_updated(self, topic: str, alive: bool) -> None:
        print(f"[UI] updating topic_status topic={topic} alive={alive}")
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
        print(f"[UI] updating tf_pose {pose}")
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

    # ── Joint Plan slots ──────────────────────────────────────────────────

    def _update_plan_button_enabled(self) -> None:
        """Enable joint plan buttons only when backend is running and running_mode is not none."""
        plan_enabled = self._running_mode in ("sim", "real") and self._launch_manager.is_running
        self._plan_btn.setEnabled(plan_enabled)
        if self._running_mode == "sim":
            exec_enabled = plan_enabled
        elif self._running_mode == "real":
            exec_enabled = plan_enabled and self._joint_safety_chk.isChecked()
        else:
            exec_enabled = False
        self._execute_btn.setEnabled(exec_enabled)
        print(
            f"[BTN] _update_plan_button_enabled: "
            f"running_mode={self._running_mode} is_running={self._launch_manager.is_running} "
            f"safety_checked={self._joint_safety_chk.isChecked()} "
            f"plan_enabled={plan_enabled} exec_enabled={exec_enabled}"
        )

    def _update_cart_button_enabled(self) -> None:
        """Enable cartesian buttons only when backend is running and running_mode is not none."""
        plan_enabled = self._running_mode in ("sim", "real") and self._launch_manager.is_running
        self._cart_plan_btn.setEnabled(plan_enabled)
        if self._running_mode == "sim":
            exec_enabled = plan_enabled
        elif self._running_mode == "real":
            exec_enabled = plan_enabled and self._cart_safety_chk.isChecked()
        else:
            exec_enabled = False
        self._cart_execute_btn.setEnabled(exec_enabled)
        print(
            f"[BTN] _update_cart_button_enabled: "
            f"running_mode={self._running_mode} is_running={self._launch_manager.is_running} "
            f"safety_checked={self._cart_safety_chk.isChecked()} "
            f"plan_enabled={plan_enabled} exec_enabled={exec_enabled}"
        )

    @Slot()
    def _on_fill_joints_clicked(self) -> None:
        """Fill target fields with current joint values, in the selected unit."""
        if self._unit == "deg":
            inv_factor = 180.0 / math.pi
        else:
            inv_factor = 1.0
        for i, name in enumerate(self.JOINT_NAMES):
            val = self._raw_joints.get(name)
            if val is not None:
                self._target_inputs[i].setText(f"{val * inv_factor:.4f}")
            else:
                self._target_inputs[i].setText("")
        self._plan_status_lbl.setText("—")
        self._plan_status_lbl.setStyleSheet(
            "font-size: 9pt; color: #888; font-style: italic;"
        )

    @Slot()
    def _on_plan_clicked(self) -> None:
        """Read target fields, convert to radians, call the service via ROS bridge."""
        angular_unit = self._unit
        raw_values: List[float] = []
        for le in self._target_inputs:
            text = le.text().strip()
            if not text:
                self._plan_status_lbl.setText("Invalid input — fill all 6 fields")
                self._plan_status_lbl.setStyleSheet(
                    "font-size: 9pt; color: #ff5252; font-weight: bold;"
                )
                return
            try:
                raw_values.append(float(text))
            except ValueError:
                self._plan_status_lbl.setText(f"Invalid input — non-numeric value")
                self._plan_status_lbl.setStyleSheet(
                    "font-size: 9pt; color: #ff5252; font-weight: bold;"
                )
                return

        if len(raw_values) != 6:
            self._plan_status_lbl.setText("Invalid input — enter 6 values")
            self._plan_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        # Always convert to radians before sending to ROS
        if angular_unit == "deg":
            positions_rad = [math.radians(v) for v in raw_values]
        else:
            positions_rad = raw_values

        print(f"DEBUG unit: {angular_unit}")
        print(f"DEBUG input: {raw_values}")
        print(f"DEBUG positions_rad: {positions_rad}")

        if self._ros_node is None:
            self._plan_status_lbl.setText("ROS node not running")
            self._plan_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        self._ros_node.call_joint_plan(positions_rad)

    @Slot()
    def _on_planning_started(self) -> None:
        self._plan_status_lbl.setText("Planning...")
        self._plan_status_lbl.setStyleSheet(
            "font-size: 9pt; color: #ff9800; font-weight: bold;"
        )

    @Slot(bool, str)
    def _on_planning_finished(self, success: bool, message: str) -> None:
        if success:
            self._plan_status_lbl.setText(f"Plan success — {message}")
            self._plan_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #00e676; font-weight: bold;"
            )
        else:
            self._plan_status_lbl.setText(f"Plan failed — {message}")
            self._plan_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
        self._update_plan_button_enabled()

    @Slot(bool)
    def _on_plan_btn_enabled(self, enabled: bool) -> None:
        """Called from bridge during service call — only disable plan button."""
        self._plan_btn.setEnabled(enabled)

    @Slot()
    def _on_execute_clicked(self) -> None:
        """Execute joint target (execute=True on service)."""
        print(
            f"[EXEC] _on_execute_clicked: "
            f"running_mode={self._running_mode} "
            f"safety_checked={self._joint_safety_chk.isChecked()} "
            f"execute=True"
        )
        if self._running_mode == "real" and not self._joint_safety_chk.isChecked():
            self._plan_status_lbl.setText("Safety checkbox required for real mode")
            self._plan_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        if self._ros_node is None:
            self._plan_status_lbl.setText("ROS node not running")
            self._plan_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        angular_unit = self._unit
        raw_values: List[float] = []
        for le in self._target_inputs:
            text = le.text().strip()
            if not text:
                self._plan_status_lbl.setText("Invalid input — fill all 6 fields")
                self._plan_status_lbl.setStyleSheet(
                    "font-size: 9pt; color: #ff5252; font-weight: bold;"
                )
                return
            try:
                raw_values.append(float(text))
            except ValueError:
                self._plan_status_lbl.setText(f"Invalid input — non-numeric value")
                self._plan_status_lbl.setStyleSheet(
                    "font-size: 9pt; color: #ff5252; font-weight: bold;"
                )
                return

        if len(raw_values) != 6:
            self._plan_status_lbl.setText("Invalid input — enter 6 values")
            self._plan_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        if angular_unit == "deg":
            positions_rad = [math.radians(v) for v in raw_values]
        else:
            positions_rad = raw_values

        print(f"[EXEC] unit={angular_unit} input={raw_values} positions_rad={positions_rad}")
        bridge = self._ros_node._joint_plan_bridge
        if bridge and bridge._client:
            svc = bridge.SERVICE_NAME
            if not bridge._client.wait_for_service(timeout_sec=2.0):
                self._plan_status_lbl.setText(f"Service {svc} not available")
                self._plan_status_lbl.setStyleSheet(
                    "font-size: 9pt; color: #ff5252; font-weight: bold;"
                )
                return
            print(f"[EXEC] service={svc} ready, calling execute=True")

        self._ros_node.call_joint_execute(positions_rad)
        self._update_plan_button_enabled()

    @Slot()
    def _on_fill_cart_clicked(self) -> None:
        """Fill X,Y,Z from current tool0 TF transform."""
        pose = getattr(self._ros_node, "_tf_pose_cache", None) if self._ros_node else None
        if pose and pose.get("available"):
            x_m = pose["tx"]
            y_m = pose["ty"]
            z_m = pose["tz"]
            self._cart_x_input.setText(f"{x_m * 1000.0:.3f}")
            self._cart_y_input.setText(f"{y_m * 1000.0:.3f}")
            self._cart_z_input.setText(f"{z_m * 1000.0:.3f}")
        else:
            self._cart_status_lbl.setText("TF tool0 not available")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )

    def _read_cartesian_inputs(self) -> Tuple[bool, float, float, float, str]:
        """Read and validate cartesian XYZ inputs. Returns (ok, x_m, y_m, z_m, frame_id)."""
        try:
            x_mm = float(self._cart_x_input.text().strip())
            y_mm = float(self._cart_y_input.text().strip())
            z_mm = float(self._cart_z_input.text().strip())
        except ValueError:
            return False, 0.0, 0.0, 0.0, ""
        x_m = x_mm / 1000.0
        y_m = y_mm / 1000.0
        z_m = z_mm / 1000.0
        frame_id = self._cart_frame_input.text().strip() or "base_link"
        return True, x_m, y_m, z_m, frame_id

    @Slot()
    def _on_cart_plan_clicked(self) -> None:
        """Plan cartesian target (execute=False on service)."""
        print("[GUI] Cartesian plan clicked")
        print(f"[GUI] running_mode: {self._running_mode}")
        print(f"[GUI] launch_state: {'running' if self._launch_manager.is_running else 'stopped'}")
        print(f"[GUI] execute: False")

        ok, x_m, y_m, z_m, frame_id = self._read_cartesian_inputs()
        if not ok:
            self._cart_status_lbl.setText("Invalid input — enter X, Y, Z in mm")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        roll = CartesianBridge.FIXED_ROLL
        pitch = CartesianBridge.FIXED_PITCH
        yaw = CartesianBridge.FIXED_YAW
        qx, qy, qz, qw = rpy_to_quaternion(roll, pitch, yaw)

        x_mm = x_m * 1000.0
        y_mm = y_m * 1000.0
        z_mm = z_m * 1000.0
        print(f"DEBUG Cartesian input mm: {x_mm:.3f} {y_mm:.3f} {z_mm:.3f}")
        print(f"DEBUG Cartesian m: {x_m:.6f} {y_m:.6f} {z_m:.6f}")
        print(f"DEBUG fixed rpy: {roll:.6f} {pitch:.6f} {yaw:.6f}")
        print(f"DEBUG quaternion: {qx:.6f} {qy:.6f} {qz:.6f} {qw:.6f}")

        if self._ros_node is None:
            self._cart_status_lbl.setText("ROS node not running")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        self._ros_node.call_cartesian_plan(x_m, y_m, z_m, frame_id)

    @Slot()
    def _on_cart_execute_clicked(self) -> None:
        """Execute cartesian target (execute=True on service)."""
        print(
            f"[EXEC] _on_cart_execute_clicked: "
            f"running_mode={self._running_mode} "
            f"safety_checked={self._cart_safety_chk.isChecked()} "
            f"execute=True"
        )
        if self._running_mode == "real" and not self._cart_safety_chk.isChecked():
            self._cart_status_lbl.setText("Safety checkbox required for real mode")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        if self._ros_node is None:
            self._cart_status_lbl.setText("ROS node not running")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        ok, x_m, y_m, z_m, frame_id = self._read_cartesian_inputs()
        if not ok:
            self._cart_status_lbl.setText("Invalid input — enter X, Y, Z in mm")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
            return

        roll = CartesianBridge.FIXED_ROLL
        pitch = CartesianBridge.FIXED_PITCH
        yaw = CartesianBridge.FIXED_YAW
        qx, qy, qz, qw = rpy_to_quaternion(roll, pitch, yaw)

        print(f"[EXEC] Cartesian: x_m={x_m:.6f} y_m={y_m:.6f} z_m={z_m:.6f} frame={frame_id}")
        print(f"[EXEC] Cartesian: rpy=({roll:.6f},{pitch:.6f},{yaw:.6f}) q=({qx:.6f},{qy:.6f},{qz:.6f},{qw:.6f})")

        bridge = self._ros_node._cartesian_bridge
        if bridge and bridge._client:
            svc = bridge.SERVICE_NAME
            if not bridge._client.wait_for_service(timeout_sec=2.0):
                self._cart_status_lbl.setText(f"Service {svc} not available")
                self._cart_status_lbl.setStyleSheet(
                    "font-size: 9pt; color: #ff5252; font-weight: bold;"
                )
                return
            print(f"[EXEC] service={svc} ready, calling execute=True")

        self._ros_node.call_cartesian_execute(x_m, y_m, z_m, frame_id)
        self._update_cart_button_enabled()

    @Slot()
    def _on_cart_planning_started(self) -> None:
        """Called when cartesian planning service call starts."""
        self._cart_status_lbl.setText("Cartesian planning...")
        self._cart_status_lbl.setStyleSheet("font-size: 9pt; color: #ff9800;")
        self._cart_plan_btn.setEnabled(False)
        self._cart_execute_btn.setEnabled(False)

    @Slot(bool, str)
    def _on_cart_planning_finished(self, success: bool, message: str) -> None:
        if success:
            self._cart_status_lbl.setText(f"Plan success — {message}")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #00e676; font-weight: bold;"
            )
        else:
            self._cart_status_lbl.setText(f"Plan failed — {message}")
            self._cart_status_lbl.setStyleSheet(
                "font-size: 9pt; color: #ff5252; font-weight: bold;"
            )
        self._update_cart_button_enabled()

    @Slot(bool)
    def _on_cart_buttons_enabled(self, enabled: bool) -> None:
        """Re-evaluate cartesian button states after a service call completes."""
        self._update_cart_button_enabled()

    @Slot(int)
    def _on_joint_safety_changed(self, state: int) -> None:
        """Re-evaluate execute button when safety checkbox toggles."""
        self._update_plan_button_enabled()

    @Slot(int)
    def _on_cart_safety_changed(self, state: int) -> None:
        """Re-evaluate execute button when safety checkbox toggles."""
        self._update_cart_button_enabled()

    # ── helpers ────────────────────────────────────────────────────────────

    def _update_status_visibility(self) -> None:
        if self._running_mode == "none":
            self._status_stack.setCurrentIndex(-1)  # hide
        elif self._running_mode == "sim":
            self._status_stack.setCurrentIndex(0)
        else:
            self._status_stack.setCurrentIndex(1)

    def _update_topic_labels(self) -> None:
        cfg = self._config.get(self._running_mode, self._config.get("none", {}))
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
        self._tf_status_lbl.setText(
            "TF unavailable: base_link -> tool0"
            if self._running_mode in ("sim", "real")
            else "TF inactive: mode none"
        )

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self._launch_manager.stop(timeout=3.0)
        # Capture and null out _ros_node so no new calls can start
        node = self._ros_node
        self._ros_node = None
        # Signal rclpy context shutdown so spin thread exits its loop naturally
        try:
            rclpy.shutdown()
            print("[GUI] rclpy.shutdown() called")
        except Exception:
            pass
        # Wait for the spin thread to finish (it exits after rclpy.ok() returns False)
        if self._ros_thread is not None and self._ros_thread.is_alive():
            print("[GUI] waiting for ROS spin thread to finish...")
            self._ros_thread.join(timeout=5.0)
            if self._ros_thread.is_alive():
                print("[GUI] WARNING: ROS spin thread did not exit cleanly")
        # Now safe to destroy the node (spin thread is done)
        if node is not None:
            try:
                node.destroy_node()
                print("[GUI] ROS node destroyed on close")
            except Exception as exc:
                print(f"[GUI] Error destroying ROS node: {exc}")
        event.accept()


# ──────────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description="GP7 Robot GUI — Phase 2.1: Joint Plan Only")
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
