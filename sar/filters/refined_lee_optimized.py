"""
Refined Lee speckle filter.

This module provides the public GeoSAR implementation of the
Refined Lee adaptive speckle filter.

The implementation follows Lee (1981) and is built from the
vectorized feature pipeline implemented in GeoSAR.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from sar.features.gradients import (
    compute_gradient_directions,
)
from sar.features.noise import (
    compute_noise_variance,
    compute_normalized_variance_grid,
)
from sar.features.subwindow_grid import (
    build_subwindow_mean_grid,
)
from sar.features.subwindow_variance_grid import (
    build_subwindow_variance_grid,
)
from sar.sar_image import SARImage
from sar.sar_statistics import (
    local_mean,
)


def _compute_local_statistics(
    image: SARImage,
) -> NDArray:
    """
    Compute the local 3×3 mean image required by
    the Refined Lee filter.

    Parameters
    ----------
    image
        Input SAR image.

    Returns
    -------
    ndarray
        Local mean image.
    """

    return local_mean(
        image,
        window_size=3,
    ).data



def _compute_noise_image(
    mean_image: NDArray,
    windows: NDArray,
) -> NDArray:
    """
    Compute the local speckle noise variance image.
    """

    mean_grid = build_subwindow_mean_grid(
        mean_image,
    )

    variance_grid = build_subwindow_variance_grid(
        windows,
    )

    normalized = compute_normalized_variance_grid(
        mean_grid,
        variance_grid,
    )

    return compute_noise_variance(
        normalized,
    )


from sar.features.gradients import (
    compute_signed_composite_gradients,
)


def _compute_direction_image(
    mean_image: NDArray[np.float64],
) -> NDArray[np.int8]:
    """
    Compute the dominant Refined Lee direction image.
    """

    mean_grid = build_subwindow_mean_grid(
        mean_image,
    )

    signed_gradients = (
        compute_signed_composite_gradients(
            mean_grid,
        )
    )

    return compute_gradient_directions(
        signed_gradients,
    )


