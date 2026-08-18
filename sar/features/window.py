from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def extract_window_centers(
    windows: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Return the centre pixel of every 7×7 window.
    """

    return windows[...,3,3]