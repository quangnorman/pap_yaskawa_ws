"""Draw YOLO box and labels on a BGR image for debug publishing."""

from __future__ import annotations

from typing import List, Optional, Tuple

import cv2
import numpy as np


def _measure_text_block(
    lines: List[str],
    font: int,
    font_scale: float,
    thickness: int,
    line_gap: int,
    padding: int,
) -> Tuple[int, int, List[Tuple[str, int, int, int]]]:
    """Return (block_w, block_h, rows) where each row is (text, tw, th, baseline)."""
    rows: List[Tuple[str, int, int, int]] = []
    max_tw = 0
    cursor = padding
    for line in lines:
        (tw, th), bl = cv2.getTextSize(line, font, font_scale, thickness)
        rows.append((line, tw, th, bl))
        max_tw = max(max_tw, tw)
        cursor += th + bl + line_gap
    block_h = cursor - line_gap + padding
    block_w = max_tw + 2 * padding
    return block_w, block_h, rows


def _draw_multiline_text_block(
    img: np.ndarray,
    lines: List[str],
    top_left_x: int,
    top_left_y: int,
    font: int = cv2.FONT_HERSHEY_SIMPLEX,
    font_scale: float = 0.55,
    thickness: int = 1,
    text_color: Tuple[int, int, int] = (255, 255, 255),
    bg_color: Tuple[int, int, int] = (0, 0, 0),
    line_gap: int = 2,
    padding: int = 6,
) -> None:
    """Draw several left-aligned lines with one solid background rectangle."""
    h, w = img.shape[:2]
    block_w, block_h, rows = _measure_text_block(
        lines, font, font_scale, thickness, line_gap, padding
    )

    x0 = max(0, min(top_left_x, w - block_w))
    y0 = max(0, min(top_left_y, h - block_h))
    x1 = min(w - 1, x0 + block_w)
    y1 = min(h - 1, y0 + block_h)

    cv2.rectangle(img, (x0, y0), (x1, y1), bg_color, -1)
    cv2.rectangle(img, (x0, y0), (x1, y1), (80, 80, 80), 1, cv2.LINE_AA)

    cursor = y0 + padding
    for line, _tw, th, bl in rows:
        baseline_y = min(cursor + th, h - 1)
        cv2.putText(
            img,
            line,
            (x0 + padding, baseline_y),
            font,
            font_scale,
            text_color,
            thickness,
            cv2.LINE_AA,
        )
        cursor = baseline_y + bl + line_gap


def _clamp_text_block_origin(
    x_min: int,
    y_min: int,
    x_max: int,
    y_max: int,
    block_w: int,
    block_h: int,
    img_w: int,
    img_h: int,
    margin: int,
) -> Tuple[int, int]:
    """Place block above bbox if possible, else below; keep inside image."""
    tx = x_min
    ty_above = y_min - margin - block_h
    if ty_above >= 0:
        ty = ty_above
    else:
        ty = min(y_max + margin, img_h - block_h)
    tx = max(0, min(tx, img_w - block_w))
    ty = max(0, min(ty, img_h - block_h))
    return tx, ty


def draw_box_detection(
    bgr: np.ndarray,
    x_min: int,
    y_min: int,
    x_max: int,
    y_max: int,
    class_name: str,
    confidence: float,
    distance_m: float,
    *,
    center_x: Optional[int] = None,
    center_y: Optional[int] = None,
    width_px: Optional[int] = None,
    height_px: Optional[int] = None,
) -> np.ndarray:
    """Return a copy of ``bgr`` with bbox, center marker, crosshairs, and text overlay.

    If ``center_x`` / ``center_y`` / ``width_px`` / ``height_px`` are omitted, they are
    derived from the bounding box corners.
    """
    out = bgr.copy()
    ih, iw = out.shape[:2]

    cx = int(center_x) if center_x is not None else int(round((x_min + x_max) * 0.5))
    cy = int(center_y) if center_y is not None else int(round((y_min + y_max) * 0.5))
    wp = int(width_px) if width_px is not None else int(x_max - x_min)
    hp = int(height_px) if height_px is not None else int(y_max - y_min)

    box_color = (0, 255, 0)
    cv2.rectangle(out, (x_min, y_min), (x_max, y_max), box_color, 2, cv2.LINE_AA)

    cross_color = (0, 255, 255)
    cv2.line(out, (0, cy), (iw - 1, cy), cross_color, 1, cv2.LINE_AA)
    cv2.line(out, (cx, 0), (cx, ih - 1), cross_color, 1, cv2.LINE_AA)

    r = max(4, min(iw, ih) // 120)
    r = min(r, 14)
    cv2.circle(out, (cx, cy), r, (0, 0, 255), -1, cv2.LINE_AA)
    cv2.circle(out, (cx, cy), r, (255, 255, 255), 1, cv2.LINE_AA)

    if distance_m >= 0.0:
        dist_txt = f"{distance_m:.3f} m"
    else:
        dist_txt = "n/a"

    lines = [
        f"class: {class_name}",
        f"confidence: {confidence:.3f}",
        f"center (px): ({cx}, {cy})",
        f"size (px): {wp} x {hp}",
        f"distance: {dist_txt}",
        f"bbox TL: ({x_min}, {y_min})",
        f"bbox BR: ({x_max}, {y_max})",
    ]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.55
    thick = 1
    gap = 2
    pad = 6
    block_w, block_h, _ = _measure_text_block(lines, font, scale, thick, gap, pad)
    tx, ty = _clamp_text_block_origin(
        x_min, y_min, x_max, y_max, block_w, block_h, iw, ih, margin=8
    )
    _draw_multiline_text_block(
        out,
        lines,
        tx,
        ty,
        font=font,
        font_scale=scale,
        thickness=thick,
        text_color=(255, 255, 255),
        bg_color=(0, 0, 0),
        line_gap=gap,
        padding=pad,
    )
    return out


def draw_no_detection(bgr: np.ndarray, message: str = "No detection") -> np.ndarray:
    """Draw status text with solid background when no target detection is present."""
    out = bgr.copy()
    h, w = out.shape[:2]
    lines = [message]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.7
    thick = 2
    gap = 2
    pad = 8
    block_w, block_h, _ = _measure_text_block(lines, font, scale, thick, gap, pad)
    tx, ty = 8, 8
    tx = max(0, min(tx, w - block_w))
    ty = max(0, min(ty, h - block_h))
    _draw_multiline_text_block(
        out,
        lines,
        tx,
        ty,
        font=font,
        font_scale=scale,
        thickness=thick,
        text_color=(0, 200, 255),
        bg_color=(0, 0, 0),
        line_gap=gap,
        padding=pad,
    )
    return out
