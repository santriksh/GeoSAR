from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

SUBWINDOW_OFFSETS = (
    (-2, -2),
    (-2,  0),
    (-2,  2),
    ( 0, -2),
    ( 0,  0),
    ( 0,  2),
    ( 2, -2),
    ( 2,  0),
    ( 2,  2),
)


def build_subwindow_mean_grid(
    mean_image: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Construct the 3×3 grid of shifted mean images.

    Parameters
    ----------
    mean_image
        Local 3×3 mean image.

    Returns
    -------
    ndarray
        Shape (rows, cols, 3, 3)
    """

    rows, cols = mean_image.shape

    padded = np.pad(
        mean_image,
        pad_width=2,
        mode="reflect",
    )

    grid = np.empty(
        (rows, cols, 3, 3),
        dtype=np.float64,
    )

    for index, (dr, dc) in enumerate(SUBWINDOW_OFFSETS):

        r = dr + 2
        c = dc + 2

        grid[..., index // 3, index % 3] = (
            padded[
                r : r + rows,
                c : c + cols,
            ]
        )

    return grid
