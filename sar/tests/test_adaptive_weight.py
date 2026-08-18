import numpy as np
import pytest

from sar.filters.refined_lee import (
    #Direction,
    _directional_statistics,
_estimate_signal_variance,_adaptive_weight
)

from sar.constants import refined_lee

def test_adaptive_weight_zero_variance():

    weight = _adaptive_weight(
        signal_variance=5.0,
        observed_variance=0.0,
    )

    assert weight == 0.0


def test_adaptive_weight_zero_signal():

    weight = _adaptive_weight(
        signal_variance=0.0,
        observed_variance=12.0,
    )

    assert weight == 0.0


def test_adaptive_weight():

    weight = _adaptive_weight(
        signal_variance=8.0,
        observed_variance=16.0,
    )

    assert weight == 0.5


def test_adaptive_weight_unity():

    weight = _adaptive_weight(
        signal_variance=15.0,
        observed_variance=15.0,
    )

    assert weight == 1.0