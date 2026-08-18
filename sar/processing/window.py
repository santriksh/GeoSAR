from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


def apply_window_filter(
    image: NDArray[np.float64],
    filter_function: Callable[
        [NDArray[np.float64]],
        float,
    ],
    *,
    window_size: int,
    padding_mode: str = "reflect",
) -> NDArray[np.float64]:
    """
    Apply a window-based filter to an image.

    Parameters
    ----------
    image
        Input image.

    filter_function
        Function operating on a square window.

    window_size
        Size of the window (must be odd).

    padding_mode
        NumPy padding mode.

    Returns
    -------
    Filtered image.
    """

    if window_size % 2 == 0:
        raise ValueError(
            "window_size must be odd."
        )

    pad = window_size // 2

    padded = np.pad(
        image,
        pad_width=pad,
        mode=padding_mode,
    )

    filtered = np.empty_like(
        image,
        dtype=np.float64,
    )

    rows, cols = image.shape

    for row in range(rows):

        for col in range(cols):

            window = padded[
                row : row + window_size,
                col : col + window_size,
            ]

            filtered[row, col] = filter_function(
                window,
            )

    return filtered