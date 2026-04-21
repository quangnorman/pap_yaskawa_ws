#!/usr/bin/env bash
# End-to-end: mock ros2_control + MoveIt, then verifiers, then task_executor + service:
#   1) gp7_moveit_config verify_plan_execute.py (regression)
#   2) gp7_task_executor verify_fake_stack --repeat 2 (two goals, one process)
#   3) Launch task_executor (avoids extra MoveGroup clients during MoveIt smoke tests)
#   4) gp7_task_executor move_to_joint_goal service (canonical task path)
# Prereq: colcon build ... && source install/setup.bash (include gp7_task_executor)
set -eo pipefail
cd "$(dirname "$0")/.."
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash
# shellcheck source=/dev/null
source install/setup.bash

pkill -f ros2_control_node 2>/dev/null || true
pkill -f move_group 2>/dev/null || true
sleep 1
# Clears stale graph; avoids flaky /move_action discovery
ros2 daemon stop 2>/dev/null || true
sleep 1

ros2 launch gp7_moveit_config moveit_fake_hardware.launch.py > /tmp/gp7_fake_test.log 2>&1 &
LP=$!
# Bring up ros2_control + move_group first (second launch follows to avoid startup contention).
sleep 52
set +e
ros2 run gp7_moveit_config verify_plan_execute.py 2>&1
RC_LEGACY=$?
sleep 3
ros2 run gp7_task_executor verify_fake_stack -- --repeat 2 2>&1
RC_NEW=$?
ros2 launch gp7_task_executor task_executor.launch.py > /tmp/gp7_task_executor_test.log 2>&1 &
TE=$!
sleep 8
OUT_TASK=$(ros2 service call /gp7_task_executor/move_to_joint_goal gp7_task_executor_msgs/srv/MoveToJointGoal "{joint_names: ['joint_s'], positions: [0.12], tolerance: 0.05, plan_only: false}" 2>&1)
echo "${OUT_TASK}"
if echo "${OUT_TASK}" | grep -qiE 'success:\s*true'; then
  RC_TASK=0
else
  RC_TASK=1
fi
set -e
kill "${TE}" "${LP}" 2>/dev/null || true
echo "VERIFY_LEGACY_EXIT=${RC_LEGACY}"
echo "VERIFY_NEW_EXIT=${RC_NEW}"
echo "TASK_SERVICE_EXIT=${RC_TASK}"
grep -E "FATAL|Failed loading|Failed to configure" /tmp/gp7_fake_test.log || true
grep -E "FATAL|Failed loading|Failed to configure" /tmp/gp7_task_executor_test.log || true
if [ "${RC_LEGACY}" -ne 0 ] || [ "${RC_NEW}" -ne 0 ] || [ "${RC_TASK}" -ne 0 ]; then
  exit 1
fi
exit 0
