"""Scaffold launch for hand-eye calibration (no calibration nodes in Milestone 1).

TODO(Milestone-N): Launch calibration client/server, charuco/aruco capture, or
third-party hand-eye packages. Keep motion sampling through MoveIt / teach poses only.

Usage::

    ros2 launch gp7_handeye_calibration handeye_stub.launch.py
"""

from launch import LaunchDescription


def generate_launch_description() -> LaunchDescription:
    # Intentionally empty: M1 documents workflow only.
    return LaunchDescription([])
