"""
Utilities for constructing sliding window views over images.
"""

from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from numpy.typing import NDArray


def build_window_view(
    image: NDArray[np.float64],
    window_size: int = 7,
) -> NDArray[np.float64]:
    """
    Construct a reflected sliding-window view.

    Parameters
    ----------
    image
        Input image.

    window_size
        Odd-sized sliding window.

    Returns
    -------
    ndarray
        Shape (rows, cols, window_size, window_size)
    """
    if window_size % 2 == 0:
        raise ValueError(
            "window_size must be odd."
        )

    radius = window_size // 2

    padded = np.pad(
        image,
        radius,
        mode="reflect",
    )

    return sliding_window_view(
        padded,
        (window_size, window_size),
    )