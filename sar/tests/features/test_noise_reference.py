import numpy as np

from sar.features.noise import (
    compute_normalized_variance_grid,
    compute_noise_variance,
)

from sar.features.subwindow_grid import (
    build_subwindow_mean_grid,
)

from sar.features.subwindow_variance_grid import (
    build_subwindow_variance_grid,
)

from sar.features.window_views import (
    build_window_view,
)

from sar.filters.refined_lee import (
    _estimate_noise_variance,
)

from sar.sar_statistics import local_mean
from sar.sar_image import SARImage

def test_noise_variance_matches_reference(
    sample_linear_image,
):

    windows = build_window_view(
        sample_linear_image.data,
    )

    mean_image = local_mean(
        sample_linear_image,
        window_size=3,
    ).data

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

    actual = compute_noise_variance(
        normalized,
    )

    expected = np.empty_like(actual)

    for row in range(actual.shape[0]):
        for col in range(actual.shape[1]):

            expected[row, col] = _estimate_noise_variance(
                mean_grid[row, col].reshape(-1),
                variance_grid[row, col].reshape(-1),
            )

    np.testing.assert_allclose(
        actual,
        expected,
        atol=1e-12,
    )

from sar.features.mmse import (
    compute_signal_variance,
)

def test_signal_variance_matches_reference():

    rng = np.random.default_rng(42)

    directional_mean = rng.random((30,30))

    directional_variance = rng.random((30,30))

    noise = rng.random((30,30))

    actual = compute_signal_variance(
        directional_mean,
        directional_variance,
        noise,
    )

    expected = np.empty_like(actual)

    for row in range(actual.shape[0]):

        for col in range(actual.shape[1]):

            signal = (
                directional_variance[row,col]
                -
                directional_mean[row,col]**2
                * noise[row,col]
            )

            signal /= (
                noise[row,col]
                + 1.0
            )

            expected[row,col] = max(
                signal,
                0.0,
            )

    np.testing.assert_allclose(
        actual,
        expected,
        atol=1e-12,
    )

from sar.features.mmse import (
    compute_mmse_weight,
)

from sar.constants.refined_lee import EPS

def test_mmse_weight_matches_reference():

    rng = np.random.default_rng(42)

    signal = rng.random((30,30))

    variance = rng.random((30,30))

    actual = compute_mmse_weight(
        signal,
        variance,
    )

    expected = np.empty_like(actual)

    for row in range(actual.shape[0]):

        for col in range(actual.shape[1]):

            weight = (
                signal[row,col]
                /
                max(
                    variance[row,col],
                    EPS,
                )
            )

            expected[row,col] = np.clip(
                weight,
                0.0,
                1.0,
            )

    np.testing.assert_allclose(
        actual,
        expected,
        atol=1e-12,
    )