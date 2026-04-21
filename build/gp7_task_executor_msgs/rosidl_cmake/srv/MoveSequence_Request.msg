# MoveSequence Service Definition
#
# Executes a predefined sequence of named joint targets:
#   origin -> P1 -> P2 -> origin
#
# Request:
#   - execute: If true, plan and execute each waypoint. If false, plan only.
#
# Response:
#   - success: True only if all waypoints succeed.
#   - message: Human-readable result/diagnostic message.

bool execute
