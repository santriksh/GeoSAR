from sar.sar_filters import _lee_weight
import pytest
def test_weight_zero_noise():

    w = _lee_weight(
        local_variance=10.0,
        noise_variance=0.0,
    )

    assert w == 1.0

def test_weight_zero_variance():

    w = _lee_weight(
        local_variance=0.0,
        noise_variance=5.0,
    )

    assert w == 0.0

def test_negative_noise_variance():

    with pytest.raises(ValueError):
        _lee_weight(
            local_variance=10,
            noise_variance=-1,
        )

def test_weight_bounds():

    w = _lee_weight(
        local_variance=4,
        noise_variance=2,
    )

    assert 0 <= w <= 1