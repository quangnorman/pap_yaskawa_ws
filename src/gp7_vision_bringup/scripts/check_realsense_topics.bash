#!/usr/bin/env bash
# List and sample RealSense-related topics. Run **while** the driver is up, e.g. after:
#   ros2 launch gp7_vision_bringup realsense_d435.launch.py
set -euo pipefail

echo "=== ros2 topic list (filtered) ==="
ros2 topic list 2>/dev/null | grep -E '^/camera|^/cam|^/realsense' || true

echo ""
echo "=== Optional: hz sample (5s each, Ctrl+C skips) ==="
for t in \
  /camera/camera/color/image_raw \
  /camera/camera/color/camera_info \
  /camera/camera/aligned_depth_to_color/image_raw \
  /camera/camera/depth/color/points
do
  if ros2 topic list 2>/dev/null | grep -qx "$t"; then
    echo "-- timeout 5 ros2 topic hz $t --"
    timeout 5 ros2 topic hz "$t" 2>/dev/null || echo "(no messages in 5s or hz failed)"
  else
    echo "MISSING: $t"
  fi
done

echo ""
echo "If names differ, update gp7_vision_pipeline/config/realsense_depth_debug.yaml or pass"
echo "depth_debug_params:=/path/to/your.yaml to vision_debug.launch.py"
