import numpy as np
import pytest

from sar.filters.refined_lee import (
    Direction,
    _directional_statistics,
_estimate_signal_variance,_adaptive_weight,_mmse_estimate
)

def test_mmse_estimate_zero_weight():

    estimate = _mmse_estimate(
        center_pixel=12.0,
        local_mean=8.0,
        weight=0.0,
    )

    assert estimate == 8.0


def test_mmse_estimate_unity_weight():

    estimate = _mmse_estimate(
        center_pixel=12.0,
        local_mean=8.0,
        weight=1.0,
    )

    assert estimate == 12.0


def test_mmse_estimate_half_weight():

    estimate = _mmse_estimate(
        center_pixel=10.0,
        local_mean=6.0,
        weight=0.5,
    )

    assert estimate == 8.0

def test_mmse_estimate_center_equals_mean():

    estimate = _mmse_estimate(
        center_pixel=7.0,
        local_mean=7.0,
        weight=0.35,
    )

    assert estimate == 7.0