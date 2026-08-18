import numpy as np

from sar.features.noise import (
    compute_normalized_variance_grid,compute_noise_variance
)
from sar.filters.refined_lee import _estimate_noise_variance

def test_normalized_variance_shape():

    mean = np.ones((20,20,3,3))

    variance = np.ones((20,20,3,3))

    result = compute_normalized_variance_grid(
        mean,
        variance,
    )

    assert result.shape == (20,20,3,3)


def test_normalized_variance_simple():

    mean = np.full(
        (1,1,3,3),
        2.0,
    )

    variance = np.full(
        (1,1,3,3),
        8.0,
    )

    result = compute_normalized_variance_grid(
        mean,
        variance,
    )

    np.testing.assert_allclose(
        result,
        2.0,
    )


def test_normalized_variance_zero_mean():

    mean = np.zeros((1,1,3,3))

    variance = np.ones((1,1,3,3))

    result = compute_normalized_variance_grid(
        mean,
        variance,
    )

    assert np.all(
        np.isfinite(result)
    )


def test_noise_variance_shape():

    grid = np.ones((20,20,3,3))

    result = compute_noise_variance(
        grid,
    )

    assert result.shape == (20,20)


def test_noise_variance_constant():

    grid = np.full(
        (10,10,3,3),
        3.5,
    )

    result = compute_noise_variance(
        grid,
    )

    np.testing.assert_allclose(
        result,
        3.5,
    )

def test_noise_variance_matches_reference():

    rng = np.random.default_rng(42)

    means = rng.random(9)

    variances = rng.random(9)

    expected = _estimate_noise_variance(
        means,
        variances,
    )

    grid_mean = means.reshape(
        1,1,3,3,
    )

    grid_var = variances.reshape(
        1,1,3,3,
    )

    normalized = compute_normalized_variance_grid(
        grid_mean,
        grid_var,
    )

    actual = compute_noise_variance(
        normalized,
    )[0,0]

    np.testing.assert_allclose(
        actual,
        expected,
        atol=1e-12,
    )


