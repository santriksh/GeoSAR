import numpy as np

from sar.features.window_views import (
    build_window_view,
)

from sar.features.directional_statistics import (
    compute_directional_sums,compute_directional_means,compute_directional_variances
)
from sar.filters.refined_lee import Direction
from sar.constants.refined_lee import DIRECTION_PIXEL_COUNTS

def test_directional_sum_shape():

    image = np.ones((20, 20))

    windows = build_window_view(image)

    sums = compute_directional_sums(
        windows,
    )

    assert sums.shape == (20, 20, 8)

from sar.constants.refined_lee import (
    DIRECTION_MASKS,
)




def test_directional_sum_constant():

    image = np.full(
        (20, 20),
        5.0,
    )

    windows = build_window_view(image)

    sums = compute_directional_sums(
        windows,
    )

    for direction in Direction:

        expected = (
            DIRECTION_MASKS[direction].sum()
            * 5.0
        )

        np.testing.assert_allclose(
            sums[..., direction],
            expected,
        )

from sar.filters.refined_lee import (
    _extract_directional_pixels,
)


def test_directional_sum_matches_reference():

    rng = np.random.default_rng(42)

    image = rng.random((30, 30))

    windows = build_window_view(image)

    sums = compute_directional_sums(
        windows,
    )

    for _ in range(100):

        row = rng.integers(3, 27)
        col = rng.integers(3, 27)

        window = windows[row, col]

        for direction in Direction:

            expected = (
                _extract_directional_pixels(
                    window,
                    direction,
                ).sum()
            )

            actual = sums[
                row,
                col,
                direction,
            ]

            np.testing.assert_allclose(
                actual,
                expected,
            )

import pytest


def test_directional_sum_invalid_shape():

    windows = np.ones((20, 20, 5, 5))

    with pytest.raises(ValueError):

        compute_directional_sums(
            windows,
        )

def test_directional_mean_shape():

    image = np.ones((20, 20))

    windows = build_window_view(image)

    means = compute_directional_means(
        windows,
    )

    assert means.shape == (20, 20, 8)


def test_directional_mean_constant():

    image = np.full(
        (20, 20),
        7.5,
    )

    windows = build_window_view(image)

    means = compute_directional_means(
        windows,
    )

    np.testing.assert_allclose(
        means,
        7.5,
    )

def test_directional_mean_matches_reference():

    rng = np.random.default_rng(42)

    image = rng.random((30, 30))

    windows = build_window_view(
        image,
    )

    means = compute_directional_means(
        windows,
    )

    for _ in range(100):

        row = rng.integers(3, 27)
        col = rng.integers(3, 27)

        window = windows[row, col]

        for direction in Direction:

            expected = np.mean(
                _extract_directional_pixels(
                    window,
                    direction,
                )
            )

            actual = means[
                row,
                col,
                direction,
            ]

            np.testing.assert_allclose(
                actual,
                expected,
            )

def test_directional_mean_times_count_equals_sum():

    rng = np.random.default_rng(42)

    image = rng.random((20, 20))

    windows = build_window_view(image)

    sums = compute_directional_sums(
        windows,
    )

    means = compute_directional_means(
        windows,
    )

    np.testing.assert_allclose(
        means * DIRECTION_PIXEL_COUNTS,
        sums,
    )

def test_directional_variance_shape():

    image = np.ones((20,20))

    windows = build_window_view(
        image,
    )

    variances = compute_directional_variances(
        windows,
    )

    assert variances.shape == (20,20,8)

def test_directional_variance_constant():

    image = np.full(
        (20,20),
        12.3,
    )

    windows = build_window_view(
        image,
    )

    variances = compute_directional_variances(
        windows,
    )

    assert np.max(
    np.abs(variances)
) < 1e-12

def test_directional_variance_matches_reference():

    rng = np.random.default_rng(42)

    image = rng.random((30,30))

    windows = build_window_view(
        image,
    )

    variances = compute_directional_variances(
        windows,
    )

    for _ in range(100):

        row = rng.integers(3,27)
        col = rng.integers(3,27)

        window = windows[row,col]

        for direction in Direction:

            expected = np.var(
                _extract_directional_pixels(
                    window,
                    direction,
                )
            )

            actual = variances[
                row,
                col,
                direction,
            ]

            np.testing.assert_allclose(
                actual,
                expected,
                atol=1e-12,
            )


def test_directional_variance_non_negative():

    rng = np.random.default_rng(42)

    image = rng.random((20,20))

    windows = build_window_view(
        image,
    )

    variances = compute_directional_variances(
        windows,
    )

    assert np.all(
        variances >= -1e-12
    )
