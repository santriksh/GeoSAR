from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from sar.enums import ValueScale

from sar.features.directional_statistics import (
    compute_directional_means,
    compute_directional_variances,
)
from sar.features.gather import (
    gather_directional_values,
)
from sar.features.gradients import (
    compute_gradient_directions,
)
from sar.features.mmse import (
    compute_mmse_weight,
    compute_signal_variance,
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

#from sar.sar_radiometry import db_to_linear
from sar.features.window_views import build_window_view
from sar.sar_image import SARImage
from sar.sar_statistics import (
    local_mean,
    local_variance,
)


def _create_sar_image(
    image: NDArray[np.float64],
) -> SARImage:
    """
    Convert a NumPy array into a temporary SARImage.

    Parameters
    ----------
    image
        Input image.

    Returns
    -------
    SARImage
    """

    return SARImage(
        data=image,
        value_scale=ValueScale.LINEAR,
    )

################################################

def _compute_noise_image(
    image: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute the Refined Lee local noise variance image.
    """

    sar = _create_sar_image(image)

    mean_image = local_mean(
        sar,
        window_size=3,
    ).data

    variance_image = local_variance(
        sar,
        window_size=3,
    ).data

    mean_grid = build_subwindow_mean_grid(
        mean_image,
    )

    variance_grid = build_subwindow_variance_grid(
        variance_image,
    )

    normalized = compute_normalized_variance_grid(
        mean_grid,
        variance_grid,
    )

    return compute_noise_variance(
        normalized,
    )


def _compute_direction_image(
    image: NDArray[np.float64],
) -> NDArray[np.int_]:
    """
    Compute dominant Refined Lee directions.
    """

    sar = _create_sar_image(image)

    mean_image = local_mean(
        sar,
        window_size=3,
    ).data

    mean_grid = build_subwindow_mean_grid(
        mean_image,
    )

    return compute_gradient_directions(
        mean_grid,
    )


def _compute_selected_directional_statistics(
    windows: NDArray[np.float64],
    directions: NDArray[np.int_],
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
]:
    """
    Compute selected directional mean and variance.
    """

    directional_means = compute_directional_means(
        windows,
    )

    directional_variances = (
        compute_directional_variances(
            windows,
        )
    )

    selected_mean = gather_directional_values(
        directional_means,
        directions,
    )

    selected_variance = gather_directional_values(
        directional_variances,
        directions,
    )

    return (
        selected_mean,
        selected_variance,
    )


def refined_lee_filter_image(
    image: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Apply the Refined Lee filter to an image.

    Parameters
    ----------
    image
        Linear-scale SAR image.

    Returns
    -------
    ndarray
        Filtered image.
    """

    windows = build_window_view(
        image,
    )

    directions = _compute_direction_image(
        image,
    )

    noise = _compute_noise_image(
        image,
    )

    directional_mean, directional_variance = (
        _compute_selected_directional_statistics(
            windows,
            directions,
        )
    )

    signal_variance = compute_signal_variance(
        directional_mean,
        directional_variance,
        noise,
    )

    weight = compute_mmse_weight(
        signal_variance,
        directional_variance,
    )

    centre = windows[..., 3, 3]

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
