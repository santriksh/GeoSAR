import numpy as np

from sar.features.mmse import (
    compute_signal_variance,compute_mmse_weight
)

def test_signal_variance_shape():

    mean = np.ones((20,20))

    variance = np.ones((20,20))

    noise = np.ones((20,20))

    signal = compute_signal_variance(
        mean,
        variance,
        noise,
    )

    assert signal.shape == (20,20)


def test_signal_variance_zero():

    mean = np.ones((10,10))

    variance = np.zeros((10,10))

    noise = np.zeros((10,10))

    signal = compute_signal_variance(
        mean,
        variance,
        noise,
    )

    np.testing.assert_allclose(
        signal,
        0.0,
    )


def test_signal_variance_non_negative():

    rng = np.random.default_rng(42)

    mean = rng.random((20,20))

    variance = rng.random((20,20))

    noise = rng.random((20,20))

    signal = compute_signal_variance(
        mean,
        variance,
        noise,
    )

    assert np.all(signal >= 0.0)

def test_mmse_weight_shape():

    signal = np.ones((20,20))

    variance = np.ones((20,20))

    weight = compute_mmse_weight(
        signal,
        variance,
    )

    assert weight.shape == (20,20)

def test_mmse_weight_zero_signal():

    signal = np.zeros((20,20))

    variance = np.ones((20,20))

    weight = compute_mmse_weight(
        signal,
        variance,
    )

    np.testing.assert_allclose(
        weight,
        0.0,
    )


def test_mmse_weight_one():

    signal = np.ones((20,20))

    variance = np.ones((20,20))

    weight = compute_mmse_weight(
        signal,
        variance,
    )

    np.testing.assert_allclose(
        weight,
        1.0,
    )