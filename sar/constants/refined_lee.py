from enum import IntEnum

import numpy as np
from numpy.typing import NDArray

REFINED_LEE_WINDOW_SIZE = 7
REFINED_LEE_CENTER = REFINED_LEE_WINDOW_SIZE // 2
REFINED_LEE_WINDOW_SHAPE = (
    REFINED_LEE_WINDOW_SIZE,
    REFINED_LEE_WINDOW_SIZE,
)

EPS = 1e-10

REFINED_LEE_SUBWINDOW_SIZE = 3

SUBWINDOW_OFFSETS = (
    (0, 0),
    (0, 2),
    (0, 4),
    (2, 0),
    (2, 2),
    (2, 4),
    (4, 0),
    (4, 2),
    (4, 4),
)

class Direction(IntEnum):
    NORTH = 0
    NORTH_EAST = 1
    EAST = 2
    NORTH_WEST = 3
    SOUTH = 4
    SOUTH_WEST = 5
    WEST = 6
    SOUTH_EAST = 7

def _build_direction_masks() -> dict[Direction, NDArray[np.bool_]]:

    masks: dict[Direction, NDArray[np.bool_]] = {}

    # ---------- Direction 0 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    mask[:, REFINED_LEE_CENTER:] = True
    masks[Direction.NORTH] = mask

    # ---------- Direction 1 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    for y in range(REFINED_LEE_WINDOW_SIZE):
        mask[y, y:] = True
    masks[Direction.NORTH_EAST] = mask

    # ---------- Direction 2 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    mask[:4, :] = True
    masks[Direction.EAST] = mask

    # ---------- Direction 3 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    for y in range(REFINED_LEE_WINDOW_SIZE):
        mask[y, : 7 - y] = True
    masks[Direction.NORTH_WEST] = mask

    # ---------- Direction 4 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    mask[:, :4] = True
    masks[Direction.SOUTH] = mask

    # ---------- Direction 5 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    for y in range(REFINED_LEE_WINDOW_SIZE):
        mask[y, : y + 1] = True
    masks[Direction.SOUTH_WEST] = mask

    # ---------- Direction 6 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    mask[3:, :] = True
    masks[Direction.WEST] = mask

    # ---------- Direction 7 ----------
    mask = np.zeros(
    REFINED_LEE_WINDOW_SHAPE,
    dtype=bool,
)
    for y in range(REFINED_LEE_WINDOW_SIZE):
        mask[y, 6 - y :] = True
    masks[Direction.SOUTH_EAST] = mask

    return masks


DIRECTION_MASKS = _build_direction_masks()

DIRECTION_PIXEL_COUNTS = np.array(
    [
        np.sum(DIRECTION_MASKS[direction])
        for direction in Direction
    ],
    dtype=np.float64,
)

def _build_direction_line_masks() -> dict[Direction, NDArray[np.bool_]]:
    """
    Build the eight 7-pixel directional masks used by
    the Refined Lee directional statistics.
    """

    masks: dict[Direction, NDArray[np.bool_]] = {}

    # ---------------- NORTH ----------------
    mask = np.zeros((7, 7), dtype=bool)
    mask[:, 3] = True
    masks[Direction.NORTH] = mask

    # ---------------- NORTH EAST ----------------
    mask = np.zeros((7, 7), dtype=bool)
    for i in range(7):
        mask[i, 6 - i] = True
    masks[Direction.NORTH_EAST] = mask

    # ---------------- EAST ----------------
    mask = np.zeros((7, 7), dtype=bool)
    mask[3, :] = True
    masks[Direction.EAST] = mask

    # ---------------- NORTH WEST ----------------
    mask = np.zeros((7, 7), dtype=bool)
    for i in range(7):
        mask[i, i] = True
    masks[Direction.NORTH_WEST] = mask

    # ---------------- SOUTH ----------------
    mask = np.zeros((7, 7), dtype=bool)
    mask[:, 3] = True
    masks[Direction.SOUTH] = mask

    # ---------------- SOUTH WEST ----------------
    mask = np.zeros((7, 7), dtype=bool)
    for i in range(7):
        mask[i, 6 - i] = True
    masks[Direction.SOUTH_WEST] = mask

    # ---------------- WEST ----------------
    mask = np.zeros((7, 7), dtype=bool)
    mask[3, :] = True
    masks[Direction.WEST] = mask

    # ---------------- SOUTH EAST ----------------
    mask = np.zeros((7, 7), dtype=bool)
    for i in range(7):
        masks[Direction.SOUTH_EAST] = mask

    return masks

_DIRECTION_LINE_MASKS = _build_direction_line_masks()
__all__ = [
    "DIRECTION_MASKS",
    "REFINED_LEE_CENTER",
    "REFINED_LEE_WINDOW_SHAPE",
    "REFINED_LEE_WINDOW_SIZE",
    "Direction",
]