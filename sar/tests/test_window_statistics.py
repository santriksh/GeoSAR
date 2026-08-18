import numpy as np
import pytest

from sar.sar_statistics import window_statistics

def test_returns_window_statistics():

    windows = np.ones((9,3,3))

    means, variances = window_statistics(windows)

    assert means.shape == (9,)
    assert variances.shape == (9,)


def test_statistics_match_numpy():

    windows = np.arange(
        81,
        dtype=float,
    ).reshape(9, 3, 3)

    means, variances = window_statistics(windows)

    expected_means = np.array(
        [window.mean() for window in windows]
    )

    expected_variances = np.array(
        [window.var() for window in windows]
    )

    np.testing.assert_allclose(
        means,
        expected_means,
    )

    np.testing.assert_allclose(
        variances,
        expected_variances,
    )


def test_requires_3d_array():

    with pytest.raises(ValueError):
        window_statistics(
            np.ones((3, 3))
        )

def test_requires_at_least_one_window():

    with pytest.raises(ValueError):
        window_statistics(
            np.empty((0, 3, 3))
        )