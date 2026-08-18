from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def gather_directional_values(
    values: NDArray[np.float64],
    directions: NDArray[np.int_],
) -> NDArray[np.float64]:
    """
    Select the directional value corresponding to the
    dominant direction at each pixel.

    Parameters
    ----------
    values
        Shape (rows, cols, 8)

    directions
        Shape (rows, cols)

    Returns
    -------
    ndarray
        Shape (rows, cols)
    """

    if values.ndim != 3:
        raise ValueError(
            "values must have shape (rows, cols, 8)."
        )

    if values.shape[:2] != directions.shape:
        raise ValueError(
            "Shape mismatch."
        )

    rows, cols = directions.shape

    row_idx, col_idx = np.indices(
        (rows, cols)
    )

    return values[
        row_idx,
        col_idx,
        directions,
    ]

    