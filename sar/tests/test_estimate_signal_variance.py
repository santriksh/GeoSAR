import numpy as np
import pytest
from sar.models.statistics import NeighborhoodStatistics
from sar.filters.refined_lee import (
    Direction,
    _directional_statistics,
_estimate_signal_variance
)


def test_estimate_signal_variance_positive():

    statistics = NeighborhoodStatistics(
        mean=10.0,
        variance=30.0,
        noise_variance=0.1,
    )

    signal = _estimate_signal_variance(statistics)

    assert signal > 0


def test_estimate_signal_variance_without_noise():

    statistics = NeighborhoodStatistics(
        mean=12.0,
        variance=18.0,
        noise_variance=0.0,
    )

    signal = _estimate_signal_variance(statistics)

    assert signal == 18.0


def test_estimate_signal_variance_clamped():

    statistics = NeighborhoodStatistics(
        mean=20.0,
        variance=5.0,
        noise_variance=0.5,
    )

    signal = _estimate_signal_variance(statistics)

    assert signal == 0.0


def test_estimate_signal_variance_without_noise():

    statistics = NeighborhoodStatistics(
        mean=12.0,
        variance=18.0,
        noise_variance=0.0,
    )

    signal = _estimate_signal_variance(statistics)


    assert signal == 18.0