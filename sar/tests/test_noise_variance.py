import numpy as np
from sar.filters.refined_lee import _estimate_noise_variance
import pytest

def test_returns_expected_noise_variance():

    means = np.array([10.0] * 9)

    variances = np.array([
        1, 2, 3, 4, 5,
        100, 200, 300, 400,
    ])

    noise = _estimate_noise_variance(
        means,
        variances,
    )

    expected = np.mean(
        np.array([1, 2, 3, 4, 5]) / 100
    )

    assert noise == pytest.approx(expected)


def test_requires_nine_means():

    with pytest.raises(ValueError):

        _estimate_noise_variance(
            np.ones(8),
            np.ones(9),
        )


def test_requires_nine_variances():

    with pytest.raises(ValueError):

        _estimate_noise_variance(
            np.ones(9),
            np.ones(8),
        )

def test_handles_zero_means():

    means = np.zeros(9)

    variances = np.ones(9)

    noise = _estimate_noise_variance(
        means,
        variances,
    )

    assert np.isfinite(noise)