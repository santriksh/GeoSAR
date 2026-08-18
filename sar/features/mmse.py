from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from sar.constants.refined_lee import EPS


def compute_signal_variance(
    directional_mean: NDArray[np.float64],
    directional_variance: NDArray[np.float64],
    noise_variance: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute the local signal variance.

    Parameters
    ----------
    directional_mean
        Shape (rows, cols)

    directional_variance
        Shape (rows, cols)

    noise_variance
        Shape (rows, cols)

    Returns
    -------
    ndarray
        Shape (rows, cols)
    """

    signal = (
        directional_variance
        -
        directional_mean**2
        * noise_variance
    )

    signal /= (
        noise_variance + 1.0
    )

    return np.maximum(
        signal,
        0.0,
    )


def compute_mmse_weight(
    signal_variance: NDArray[np.float64],
    directional_variance: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute the MMSE weight.
    """
    weight = (
    signal_variance /
    np.maximum(
        directional_variance,
        EPS,
    )
)

    return np.clip(
    weight,
    0.0,
    1.0,
)