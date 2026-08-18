import numpy as np

from sar.processing import apply_window_filter
from sar.sar_statistics import window_statistics
from sar.filters.refined_lee import _extract_subwindows,_compute_subwindow_statistics

def identity_filter(window):

    return window[
        window.shape[0] // 2,
        window.shape[1] // 2,
    ]


def test_identity_filter():

    image = np.arange(
        25,
        dtype=float,
    ).reshape(5, 5)

    filtered = apply_window_filter(
        image,
        identity_filter,
        window_size=3,
    )

    np.testing.assert_array_equal(
        image,
        filtered,
    )



def mean_filter(window):

    return np.mean(window)


def test_mean_filter():

    image = np.ones(
        (5, 5),
    )

    filtered = apply_window_filter(
        image,
        mean_filter,
        window_size=3,
    )

    np.testing.assert_allclose(
        filtered,
        1.0,
    )


def test_output_shape():

    image = np.random.random(
        (17, 23),
    )

    filtered = apply_window_filter(
        image,
        mean_filter,
        window_size=5,
    )

    assert filtered.shape == image.shape


import pytest


def test_even_window():

    image = np.ones(
        (5, 5),
    )

    with pytest.raises(ValueError):

        apply_window_filter(
            image,
            mean_filter,
            window_size=4,
        )

def test_compute_subwindow_statistics_matches_reference():

    rng = np.random.default_rng(42)

    window = rng.random((7, 7))

    expected_means, expected_variances = (
        window_statistics(
            _extract_subwindows(window)
        )
    )

    means, variances = (
        _compute_subwindow_statistics(window)
    )

    np.testing.assert_allclose(
        means,
        expected_means,
    )

    np.testing.assert_allclose(
        variances,
        expected_variances,
    )