import logging

import numpy as np
from numpy.typing import NDArray  # Add this import at the top!

from sar.features.directional_statistics import (
    compute_directional_means,
    compute_directional_variances,
)
from sar.features.gather import gather_directional_values
from sar.features.gradients import (
    compute_gradient_directions,
    compute_signed_composite_gradients,
)
from sar.features.mmse import compute_mmse_weight, compute_signal_variance
from sar.features.noise import compute_noise_variance, compute_normalized_variance_grid
from sar.features.subwindow_grid import build_subwindow_mean_grid
from sar.features.subwindow_variance_grid import build_subwindow_variance_grid
from sar.features.window_views import build_window_view
from sar.filters.refined_lee import refined_lee_filter
from sar.sar_geometry import _create_result
from sar.sar_image import SARImage
from sar.sar_statistics import local_mean

logger = logging.getLogger(__name__)

def _compute_mean_grid(
    image: SARImage,
) -> NDArray[np.float64]:
    """
    Compute the 3×3 mean grid used by Refined Lee.

    Parameters
    ----------
    image
        Input SAR image.

    Returns
    -------
    ndarray
        Shape (rows, cols, 3, 3)
    """
    mean_image = local_mean(
        image,
        window_size=3,
    ).data

    return build_subwindow_mean_grid(
        mean_image,
    )


def _compute_noise_image(
    mean_grid: NDArray[np.float64],
    windows: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Estimate local speckle noise variance.
    """

    variance_grid = build_subwindow_variance_grid(
        windows,
    )
#     logger.debug(
#     "Variance NaNs:",
#     np.isnan(
#         variance_grid[image.mask]
#     ).sum()
# )

    normalized = compute_normalized_variance_grid(
        mean_grid,
        variance_grid,
    )

    return compute_noise_variance(
        normalized,
    )

def _compute_direction_image(
    mean_grid: NDArray[np.float64],
) -> NDArray[np.int8]:
    """
    Compute dominant edge direction.
    """

    signed = compute_signed_composite_gradients(
        mean_grid,
    )

    return compute_gradient_directions(
        signed,
    )

def _compute_selected_directional_statistics(
    windows: NDArray[np.float64],
    directions: NDArray[np.int8],
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
]:
    """
    Gather directional statistics.
    """

    means = compute_directional_means(
        windows,
    )

    variances = compute_directional_variances(
        windows,
    )

    return (
        gather_directional_values(
            means,
            directions,
        ),
        gather_directional_values(
            variances,
            directions,
        ),
    )

def _refined_lee_numpy(
    image: SARImage,
) -> NDArray[np.float64]:
    """
    Internal NumPy implementation of the
    Refined Lee filter.
    """

    # ------------------------------------
    # Stage 1
    # ------------------------------------

    windows = build_window_view(
        image.data,
    )

    mean_grid = _compute_mean_grid(
        image,
    )

    # ------------------------------------
    # Stage 2
    # ------------------------------------

    noise = _compute_noise_image(
        mean_grid,
        windows,
    )
    ###Tmp debug
    logger.debug(
    "Noise NaNs inside valid: %s",
    np.isnan(
        noise[image.mask]
    ).sum(),
)
    directions = _compute_direction_image(
        mean_grid,
    )

    # ------------------------------------
    # Stage 3
    # ------------------------------------

    (
        directional_mean,
        directional_variance,
    ) = _compute_selected_directional_statistics(
        windows,
        directions,
    )

    ###Tmp debug
    logger.debug(
    "Directional mean NaNs inside valid: %s",
    np.isnan(
        directional_mean[image.mask]
    ).sum(),
)
    logger.debug(
    "Directional variance NaNs inside valid: %s",
    np.isnan(
        directional_variance[image.mask]
    ).sum(),
)
    # ------------------------------------
    # Stage 4
    # ------------------------------------

    signal_variance = (
        compute_signal_variance(
            directional_mean,
            directional_variance,
            noise,
        )
    )
    #Tmp Debug
    logger.debug(
    "Signal variance NaNs inside valid: %s",
    np.isnan(
        signal_variance[image.mask]
    ).sum(),
)
    weight = compute_mmse_weight(
        signal_variance,
        directional_variance,
    )
    #Tmp Debug
    logger.debug(
    "Weight NaNs inside valid: %s",
    np.isnan(
        weight[image.mask]
    ).sum(),
)
    # ------------------------------------
    # Stage 5
    # ------------------------------------

    centre = windows[
        ...,
        3,
        3,
    ]

    #Tmp Debug
    filtered = (
    directional_mean
    + weight * (centre - directional_mean)
)

    logger.debug("Filtered NaNs: %s", np.isnan(filtered).sum())

    return (
        directional_mean
        +
        weight
        * (
            centre
            -
            directional_mean
        )
    )


def refined_lee(
    image: SARImage,
) -> SARImage:
    """
    Apply the Refined Lee filter.
    """

    if image.value_scale.lower() != "linear":
        raise ValueError(
            "Refined Lee filter requires "
            "linear-scale input."
        )

    filtered = _refined_lee_numpy(
        image,
    )
    # Preserve numerical equivalence with the
    # scalar Refined Lee implementation at
    # image boundaries.
    _correct_border_pixels(
    image,
    filtered,
)

    return _create_result(
        reference=image,
        data=filtered,
        mask=image.mask,
        operation="refined_lee",
        value_scale=image.value_scale,
    )
#
# Border handling
#
# The vectorized implementation computes the
# 3×3 mean grid from the global mean image.
#
# This is mathematically equivalent to the
# scalar Refined Lee algorithm only for
# interior pixels.
#
# At image boundaries the reflected-window
# construction used by the scalar algorithm
# differs slightly.
#
# Therefore border pixels are recomputed
# using the scalar implementation.
#

def _correct_border_pixels(
    image: SARImage,
    filtered: NDArray[np.float64],
) -> None:
    """
    Recompute border pixels using the scalar
    Refined Lee implementation.

    The vectorized implementation is mathematically
    equivalent to the scalar implementation only
    for interior pixels.

    Border pixels are recomputed using the scalar
    algorithm to preserve exact equivalence.
    """

    radius = 3

    windows = build_window_view(
        image.data,
    )

    rows, cols = image.shape

    #
    # Top + Bottom
    #
    for row in range(radius):

        for col in range(cols):

            filtered[row, col] = refined_lee_filter(
                windows[row, col],
            )

            filtered[
                rows - 1 - row,
                col,
            ] = refined_lee_filter(
                windows[
                    rows - 1 - row,
                    col,
                ],
            )

    #
    # Left + Right
    #
    for row in range(
        radius,
        rows - radius,
    ):

        for col in range(radius):

            filtered[row, col] = refined_lee_filter(
                windows[row, col],
            )

            filtered[
                row,
                cols - 1 - col,
            ] = refined_lee_filter(
                windows[
                    row,
                    cols - 1 - col,
                ],
            )