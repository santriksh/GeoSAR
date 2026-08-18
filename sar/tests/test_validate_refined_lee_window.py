import numpy as np
import pytest
from sar.models.statistics import NeighborhoodStatistics
from sar.filters.refined_lee import (
    Direction,
    _directional_statistics,
_estimate_signal_variance,_validate_refined_lee_window
)

def test_validate_refined_lee_window_valid():

    window = np.ones((7, 7))

    _validate_refined_lee_window(window)


def test_validate_refined_lee_window_invalid_rows():

    window = np.ones((5, 7))

    with pytest.raises(ValueError):
        _validate_refined_lee_window(window)


def test_validate_refined_lee_window_invalid_rows():

    window = np.ones((5, 7))

    with pytest.raises(ValueError):
        _validate_refined_lee_window(window)


def test_validate_refined_lee_window_invalid_columns():

    window = np.ones((7, 5))

    with pytest.raises(ValueError):
        _validate_refined_lee_window(window)


def test_validate_refined_lee_window_one_dimensional():

    window = np.ones(49)

    with pytest.raises(ValueError):
        _validate_refined_lee_window(window)