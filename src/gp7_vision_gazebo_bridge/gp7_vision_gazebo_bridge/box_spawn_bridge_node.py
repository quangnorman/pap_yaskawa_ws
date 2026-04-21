"""Bridge vision-estimated box pose and size into Gazebo Classic.

Per architecture: perception is separate from Gazebo simulation logic.
This node ONLY listens to vision outputs and uses Gazebo services to spawn/update
a stable model name.
"""

from __future__ import annotations

import copy
import math
import sys
import time
from dataclasses import dataclass
from typing import Optional, Tuple

import rclpy
from gazebo_msgs.srv import DeleteEntity
from gazebo_msgs.srv import SpawnEntity
from geometry_msgs.msg import PoseStamped, Vector3
from rclpy.node import Node
from rclpy.qos import QoSProfile


@dataclass
class BoxState:
    pose: PoseStamped
    size: Vector3


def _vec3_to_tuple(v: Vector3) -> Tuple[float, float, float]:
    return float(v.x), float(v.y), float(v.z)


def _quat_norm(q) -> float:
    return float(math.sqrt(q.x * q.x + q.y * q.y + q.z * q.z + q.w * q.w))


class BoxSpawnBridgeNode(Node):
    """Subscribe to /vision/box_pose and /vision/box_size and update detected_box in Gazebo."""

    def __init__(self) -> None:
        super().__init__("box_spawn_bridge_node")

        self.declare_parameter("box_name", "detected_box")
        self.declare_parameter("pose_topic", "/vision/box_pose")
        self.declare_parameter("size_topic", "/vision/box_size")

        self.declare_parameter("update_min_interval_sec", 0.3)

        self.declare_parameter("size_abs_threshold_m", 0.001)
        self.declare_parameter("size_rel_threshold", 0.05)

        self.declare_parameter("color_r", 0.8)
        self.declare_parameter("color_g", 0.1)
        self.declare_parameter("color_b", 0.1)
        self.declare_parameter("color_a", 1.0)

        self.declare_parameter("model_static", True)
        self.declare_parameter("reference_frame", "world")

        self.box_name: str = self.get_parameter("box_name").get_parameter_value().string_value
        self.pose_topic: str = self.get_parameter("pose_topic").get_parameter_value().string_value
        self.size_topic: str = self.get_parameter("size_topic").get_parameter_value().string_value

        qos = QoSProfile(depth=1)

        self._last_pose: Optional[PoseStamped] = None
        self._last_size: Optional[Vector3] = None
        self._last_spawn_state: Optional[BoxState] = None
        self._last_update_time: float = 0.0

        self._spawn_in_progress: bool = False

        self._spawn_client = self.create_client(SpawnEntity, "/spawn_entity")
        self._delete_client = self.create_client(DeleteEntity, "/delete_entity")

        self.create_subscription(PoseStamped, self.pose_topic, self._on_pose, qos)
        self.create_subscription(Vector3, self.size_topic, self._on_size, qos)

        self.create_timer(0.1, self._on_timer)

        self.get_logger().info(
            f"Bridge: subscribing pose='{self.pose_topic}', size='{self.size_topic}'. "
            f"Single Gazebo model name='{self.box_name}' (delete + respawn on change)."
        )

    def _on_pose(self, msg: PoseStamped) -> None:
        self._last_pose = msg

    def _on_size(self, msg: Vector3) -> None:
        self._last_size = msg

    def _on_timer(self) -> None:
        if self._spawn_in_progress:
            return
        if self._last_pose is None or self._last_size is None:
            return

        now = time.monotonic()
        min_interval = float(self.get_parameter("update_min_interval_sec").value)
        if now - self._last_update_time < min_interval:
            return

        new_state = BoxState(pose=self._last_pose, size=self._last_size)

        if not self._should_respawn(new_state):
            return

        self._last_update_time = now
        self._spawn_in_progress = True
        self.get_logger().info(
            f"UPDATE: scheduling delete+respawn for '{self.box_name}' "
            f"(center=({new_state.pose.pose.position.x:.3f}, {new_state.pose.pose.position.y:.3f}, "
            f"{new_state.pose.pose.position.z:.3f}) m, "
            f"size=({new_state.size.x:.3f}, {new_state.size.y:.3f}, {new_state.size.z:.3f}) m)"
        )
        self._respawn_box(new_state)

    def _should_respawn(self, new_state: BoxState) -> bool:
        if self._last_spawn_state is None:
            self.get_logger().info(
                "First spawn: no previous Gazebo state cached (will create or replace model)."
            )
            return True

        old_pose = self._last_spawn_state.pose
        old_size = self._last_spawn_state.size

        abs_th = float(self.get_parameter("size_abs_threshold_m").value)
        rel_th = float(self.get_parameter("size_rel_threshold").value)

        new_len, new_wid, new_h = _vec3_to_tuple(new_state.size)
        old_len, old_wid, old_h = _vec3_to_tuple(old_size)

        def size_changed(a: float, b: float) -> bool:
            if abs(a - b) > abs_th:
                return True
            denom = max(abs(b), 1e-6)
            if abs(a - b) / denom > rel_th:
                return True
            return False

        if size_changed(new_len, old_len) or size_changed(new_wid, old_wid) or size_changed(
            new_h, old_h
        ):
            return True

        dx = float(new_state.pose.pose.position.x - old_pose.pose.position.x)
        dy = float(new_state.pose.pose.position.y - old_pose.pose.position.y)
        dz = float(new_state.pose.pose.position.z - old_pose.pose.position.z)
        if math.sqrt(dx * dx + dy * dy + dz * dz) > 0.002:
            return True

        qn = new_state.pose.pose.orientation
        qo = old_pose.pose.orientation
        if _quat_norm(qn) < 1e-6 or _quat_norm(qo) < 1e-6:
            return False
        dot = float(qn.x * qo.x + qn.y * qo.y + qn.z * qo.z + qn.w * qo.w)
        dot = abs(dot)
        if dot < 0.999:
            return True

        return False

    def _make_box_sdf(self, length_m: float, width_m: float, height_m: float) -> str:
        r = float(self.get_parameter("color_r").value)
        g = float(self.get_parameter("color_g").value)
        b = float(self.get_parameter("color_b").value)
        a = float(self.get_parameter("color_a").value)
        static_flag = "true" if bool(self.get_parameter("model_static").value) else "false"

        return (
            '<?xml version="1.0"?>\n'
            '<sdf version="1.6">\n'
            f'  <model name="{self.box_name}">\n'
            f'    <static>{static_flag}</static>\n'
            '    <link name="link">\n'
            '      <visual name="visual">\n'
            "        <geometry>\n"
            f"          <box><size>{length_m} {width_m} {height_m}</size></box>\n"
            "        </geometry>\n"
            "        <material>\n"
            f'          <ambient>{r} {g} {b} {a}</ambient>\n'
            f'          <diffuse>{r} {g} {b} {a}</diffuse>\n'
            "        </material>\n"
            "      </visual>\n"
            '      <collision name="collision">\n'
            "        <geometry>\n"
            f"          <box><size>{length_m} {width_m} {height_m}</size></box>\n"
            "        </geometry>\n"
            "      </collision>\n"
            "    </link>\n"
            "  </model>\n"
            "</sdf>\n"
        )

    def _respawn_box(self, state: BoxState) -> None:
        length_m, width_m, height_m = _vec3_to_tuple(state.size)
        sdf = self._make_box_sdf(length_m, width_m, height_m)

        delete_req = DeleteEntity.Request()
        delete_req.name = self.box_name

        def _after_spawn(fut) -> None:
            try:
                resp = fut.result()
                ok = bool(resp.success)
                msg = resp.status_message
                if ok:
                    self.get_logger().info(
                        f"SPAWN OK: '{self.box_name}' — {msg} "
                        "(single named entity; duplicates avoided by delete-first policy)"
                    )
                    self._last_spawn_state = BoxState(
                        pose=copy.deepcopy(state.pose),
                        size=copy.deepcopy(state.size),
                    )
                else:
                    self.get_logger().error(f"SPAWN FAILED: '{self.box_name}' — {msg}")
            except Exception as e:  # noqa: BLE001
                self.get_logger().error(f"SPAWN exception for '{self.box_name}': {e}")
            finally:
                self._spawn_in_progress = False

        def _after_delete(fut) -> None:
            if fut is not None:
                try:
                    resp = fut.result()
                    if resp.success:
                        self.get_logger().info(
                            f"DELETE OK: '{self.box_name}' removed ({resp.status_message})"
                        )
                    else:
                        self.get_logger().warning(
                            f"DELETE reported failure for '{self.box_name}' "
                            f"(often 'not found' on first spawn): {resp.status_message}"
                        )
                except Exception as e:  # noqa: BLE001
                    self.get_logger().warning(
                        f"DELETE exception for '{self.box_name}' (continuing to spawn): {e}"
                    )
            else:
                self.get_logger().warning(
                    "DELETE skipped (/delete_entity not ready); spawning (first run or race)."
                )

            spawn_req = SpawnEntity.Request()
            spawn_req.name = self.box_name
            spawn_req.xml = sdf
            spawn_req.robot_namespace = ""
            spawn_req.reference_frame = str(self.get_parameter("reference_frame").value)
            spawn_req.initial_pose = state.pose.pose

            self.get_logger().info(f"SPAWN: calling /spawn_entity for '{self.box_name}'...")
            spawn_future = self._spawn_client.call_async(spawn_req)
            spawn_future.add_done_callback(_after_spawn)

        if not self._delete_client.service_is_ready():
            self.get_logger().warning(
                "/delete_entity not ready; spawning without prior delete (no duplicate if name free)."
            )
            _after_delete(None)
            return

        self.get_logger().info(f"DELETE: calling /delete_entity for '{self.box_name}'...")
        delete_future = self._delete_client.call_async(delete_req)
        delete_future.add_done_callback(_after_delete)


def main(argv: list[str] | None = None) -> None:
    rclpy.init(args=argv)
    node = BoxSpawnBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main(sys.argv)
