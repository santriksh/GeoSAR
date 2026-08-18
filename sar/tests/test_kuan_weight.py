import numpy as np
import pytest

from sar.sar_filters import _kuan_weight


def test_negative_noise_variance():

    with pytest.raises(ValueError):
        _kuan_weight(
            local_mean=10.0,
            local_variance=5.0,
            noise_variance=-1.0,
        )


def test_weight_is_bounded():

    weight = _kuan_weight(
        local_mean=10.0,
        local_variance=5.0,
        noise_variance=1.0,
    )

    assert 0.0 <= weight <= 1.0


def test_vectorised_input():

    local_mean = np.array([10.0, 20.0, 30.0])
    local_variance = np.array([5.0, 6.0, 7.0])

    weight = _kuan_weight(
        local_mean,
        local_variance,
        noise_variance=1.0,
    )

    assert weight.shape == local_mean.shape


def test_zero_local_variance():

    weight = _kuan_weight(
        local_mean=10.0,
        local_variance=0.0,
        noise_variance=1.0,
    )

    assert np.isfinite(weight)
    assert weight == pytest.approx(0.0)


def test_zero_local_mean():

    weight = _kuan_weight(
        local_mean=0.0,
        local_variance=5.0,
        noise_variance=1.0,
    )

    assert np.isfinite(weight)


def test_zero_noise_variance():

    weight = _kuan_weight(
        local_mean=10.0,
        local_variance=5.0,
        noise_variance=0.0,
    )

    assert weight == pytest.approx(1.0)


    