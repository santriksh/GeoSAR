import numpy as np
import pytest

from sar.filters.refined_lee import _gradient_direction

def test_returns_valid_direction():
    means = np.arange(1, 10, dtype=float)

    direction = _gradient_direction(means)

    assert 0 <= direction <= 7


def test_requires_nine_means():
    with pytest.raises(ValueError):
        _gradient_direction(np.ones(8))

def positive_dominant_gradient():
    means = np.array([
        1, 5, 9,
        2, 5, 8,
        1, 2, 3
    ], dtype=float)
    
    direction = _gradient_direction(means)
    
    assert direction in (0, 1, 2, 3)


def negative_dominant_gradient():
    means = np.array([
    3, 2, 1,
    8, 5, 2,
    9, 5, 1
], dtype=float)

    direction = _gradient_direction(means)
    
    assert direction in (4, 5, 6, 7)
    


