from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def compute_signed_composite_gradients(
    mean_grid: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute the four composite gradient images from the
    3×3 subwindow mean grid.

    Parameters
    ----------
    mean_grid
        Shape (rows, cols, 3, 3)

    Returns
    -------
    gradients
        Shape (rows, cols, 4)
    """
    m00 = mean_grid[..., 0, 0]
    m01 = mean_grid[..., 0, 1]
    m02 = mean_grid[..., 0, 2]
    
    m10 = mean_grid[..., 1, 0]
    #m11 = mean_grid[..., 1, 1]
    m12 = mean_grid[..., 1, 2]
    
    m20 = mean_grid[..., 2, 0]
    m21 = mean_grid[..., 2, 1]
    m22 = mean_grid[..., 2, 2]

    g0 = (m01 - m21) + (m02 - m20)

    g1 = (m12 - m10) + (m22 - m00)
    
    g2 = (m02 - m20) + (m12 - m10)
    
    g3 = (m00 - m22) + (m01 - m21)
    
    gradients = np.stack(
    (
        g0,g1,g2,g3
    ),
    axis=-1,
)

    return gradients
    
def compute_composite_gradients(
    mean_grid,
):

    return np.abs(
        compute_signed_composite_gradients(
            mean_grid
        )
    )


def compute_gradient_directions(
    signed_gradients: NDArray[np.float64],
) -> NDArray[np.int8]:
    """
    Compute the dominant Refined Lee direction.

    Parameters
    ----------
    signed_gradients
        Shape (..., 4)

    Returns
    -------
    ndarray
        Shape (...)
        Values in [0,7]
    """

    dominant = np.argmax(
        np.abs(signed_gradients),
        axis=-1,
    )

    dominant_signed = np.take_along_axis(
        signed_gradients,
        dominant[..., None],
        axis=-1,
    ).squeeze(-1)

    return np.where(
        dominant_signed >= 0,
        dominant,
        dominant + 4,
    ).astype(np.int8)
