from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
import numpy as np
from numpy.typing import NDArray

from sar.constants.refined_lee import EPS


def compute_normalized_variance_grid(
    mean_grid: NDArray[np.float64],
    variance_grid: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute the normalized variance of each Refined Lee
    3×3 subwindow.

    Parameters
    ----------
    mean_grid
        Shape (..., 3, 3)

    variance_grid
        Shape (..., 3, 3)

    Returns
    -------
    ndarray
        Shape (..., 3, 3)
    """

    if mean_grid.shape != variance_grid.shape:
        raise ValueError(
            "mean_grid and variance_grid must have the same shape."
        )

    logger.debug(
    "Mean == 0: %d",
    np.sum(mean_grid == 0)
)

    logger.debug(
        "Mean < 1e-12: %s",
        np.sum(mean_grid < 1e-12)
    )
    
    logger.debug(
        "Variance NaN: %d",
        np.isnan(variance_grid).sum()
    )

    return (
        variance_grid /
        np.maximum(
            mean_grid ** 2,
            EPS,
        )
    )


def compute_noise_variance(
    normalized_variance_grid: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Estimate local speckle variance from the
    normalized variance grid.

    Parameters
    ----------
    normalized_variance_grid
        Shape (...,3,3)

    Returns
    -------
    ndarray
        Shape (...)
    """

    flat = normalized_variance_grid.reshape(
        *normalized_variance_grid.shape[:-2],
        9,
    )

    flat = np.sort(
        flat,
        axis=-1,
    )

    return np.mean(
        flat[..., :5],
        axis=-1,
    )