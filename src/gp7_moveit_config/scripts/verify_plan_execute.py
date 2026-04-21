#!/usr/bin/env python3
"""Wait for move_group, send a simple joint-space goal, plan+execute; exit 0 on SUCCESS."""
import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

from control_msgs.action import FollowJointTrajectory
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, JointConstraint, MoveItErrorCodes, PlanningOptions
from sensor_msgs.msg import JointState


class VerifyPlanExecute(Node):
    def __init__(self):
        super().__init__("gp7_verify_plan_execute")
        # MoveIt 2 uses /move_action (server node is still named move_group)
        self._action = ActionClient(self, MoveGroup, "/move_action")
        self._traj_action = ActionClient(
            self, FollowJointTrajectory, "/arm_controller/follow_joint_trajectory"
        )
        self._got_js = False
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self._js_sub = self.create_subscription(
            JointState, "/joint_states", self._on_js, qos
        )

    def _on_js(self, msg: JointState):
        if msg.name and len(msg.position) == len(msg.name):
            self._got_js = True

    def run(self, executor: MultiThreadedExecutor) -> int:
        self.get_logger().info("Waiting for /move_action (MoveGroup) server...")
        if not self._action.wait_for_server(timeout_sec=120.0):
            self.get_logger().error("Timeout waiting for /move_action")
            return 2

        self.get_logger().info("Waiting for /arm_controller/follow_joint_trajectory ...")
        if not self._traj_action.wait_for_server(timeout_sec=120.0):
            self.get_logger().error("Timeout waiting for trajectory action server")
            return 7

        self.get_logger().info("Waiting for /joint_states...")
        for _ in range(400):
            executor.spin_once(timeout_sec=0.05)
            if self._got_js:
                break
        if not self._got_js:
            self.get_logger().error("No /joint_states received")
            return 3

        goal = MoveGroup.Goal()
        goal.request.group_name = "arm"
        goal.request.num_planning_attempts = 10
        goal.request.allowed_planning_time = 15.0
        goal.request.max_velocity_scaling_factor = 0.5
        goal.request.max_acceleration_scaling_factor = 0.5
        goal.request.pipeline_id = "ompl"
        goal.request.planner_id = "RRTConnectkConfigDefault"

        jc = JointConstraint()
        jc.joint_name = "joint_s"
        jc.position = 0.12
        jc.tolerance_above = 0.05
        jc.tolerance_below = 0.05
        jc.weight = 1.0

        c = Constraints()
        c.joint_constraints.append(jc)
        goal.request.goal_constraints.append(c)

        goal.planning_options = PlanningOptions()
        goal.planning_options.plan_only = False

        self.get_logger().info("Sending MoveGroup goal (plan + execute)...")
        send_future = self._action.send_goal_async(goal)
        executor.spin_until_future_complete(send_future, timeout_sec=120.0)
        if not send_future.done():
            self.get_logger().error("Timeout waiting for goal acceptance")
            return 8

        goal_handle = send_future.result()
        if goal_handle is None:
            self.get_logger().error("send_goal_async returned None")
            return 4
        if not goal_handle.accepted:
            self.get_logger().error("Goal rejected")
            return 5

        result_future = goal_handle.get_result_async()
        executor.spin_until_future_complete(result_future, timeout_sec=120.0)
        if not result_future.done():
            self.get_logger().error("Timeout waiting for MoveGroup result")
            return 9

        wrapped = result_future.result()
        if wrapped is None:
            self.get_logger().error("No result wrapper")
            return 6

        move_result = getattr(wrapped, "result", wrapped)
        err = move_result.error_code.val
        self.get_logger().info(
            f"MoveIt error_code={err} planning_time={move_result.planning_time:.3f}"
        )
        if err == MoveItErrorCodes.SUCCESS:
            self.get_logger().info("PASS: plan + execute reported SUCCESS")
            return 0
        self.get_logger().error(f"FAIL: MoveIt error_code={err}")
        return 1


def main():
    rclpy.init(args=sys.argv)
    node = VerifyPlanExecute()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        code = node.run(executor)
    finally:
        executor.remove_node(node)
        node.destroy_node()
        rclpy.shutdown()
    sys.exit(code)


if __name__ == "__main__":
    main()
