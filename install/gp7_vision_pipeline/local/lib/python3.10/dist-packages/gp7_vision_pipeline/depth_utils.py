"""Depth image helpers: ROI median, unit conversion, invalid filtering."""

from __future__ import annotations

import math
from typing import Tuple

import numpy as np


def median_depth_meters(
    depth_image: np.ndarray,
    center_x: int,
    center_y: int,
    half_size: int,
    encoding: str,
) -> float:
    """Return median depth in meters for a square ROI around (center_x, center_y).

    Invalid values (0, NaN, Inf) are ignored. If the depth image is uint16,
    values are treated as millimeters and converted to meters (RealSense
    aligned depth convention).

    Args:
        depth_image: 2D depth array (H, W).
        center_x: Column index of ROI center.
        center_y: Row index of ROI center.
        half_size: Half side length of the square ROI in pixels (inclusive).
        encoding: sensor_msgs/Image encoding, e.g. ``16UC1`` or ``32FC1``.

    Returns:
        Median depth in meters, or ``-1.0`` if no valid samples exist.
    """
    if depth_image is None or depth_image.size == 0:
        return -1.0

    h, w = depth_image.shape[:2]
    if h < 1 or w < 1:
        return -1.0

    x0 = max(0, center_x - half_size)
    y0 = max(0, center_y - half_size)
    x1 = min(w, center_x + half_size + 1)
    y1 = min(h, center_y + half_size + 1)
    if x0 >= x1 or y0 >= y1:
        return -1.0

    roi = depth_image[y0:y1, x0:x1]

    if encoding in ("16UC1", "mono16"):
        roi_f = roi.astype(np.float64)
        valid = roi_f > 0.0
        if not np.any(valid):
            return -1.0
        mm = roi_f[valid]
        meters = mm * 0.001
    elif encoding in ("32FC1",):
        roi_f = roi.astype(np.float64)
        valid = np.isfinite(roi_f) & (roi_f > 0.0)
        if not np.any(valid):
            return -1.0
        meters = roi_f[valid]
    else:
        # Best effort: treat as float meters if float-like, else mm uint
        if np.issubdtype(roi.dtype, np.floating):
            roi_f = roi.astype(np.float64)
            valid = np.isfinite(roi_f) & (roi_f > 0.0)
            if not np.any(valid):
                return -1.0
            meters = roi_f[valid]
        else:
            roi_f = roi.astype(np.float64)
            valid = roi_f > 0.0
            if not np.any(valid):
                return -1.0
            meters = roi_f[valid] * 0.001

    med = float(np.median(meters))
    if not math.isfinite(med) or med <= 0.0:
        return -1.0
    return med


def bbox_clip_to_image(
    x_min: int,
    y_min: int,
    x_max: int,
    y_max: int,
    width: int,
    height: int,
) -> Tuple[int, int, int, int]:
    """Clip bbox integer coordinates to image bounds."""
    x_min = int(max(0, min(x_min, width - 1)))
    y_min = int(max(0, min(y_min, height - 1)))
    x_max = int(max(0, min(x_max, width - 1)))
    y_max = int(max(0, min(y_max, height - 1)))
    if x_max < x_min:
        x_min, x_max = x_max, x_min
    if y_max < y_min:
        y_min, y_max = y_max, y_min
    return x_min, y_min, x_max, y_max
