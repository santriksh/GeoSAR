import numpy as np

from sar.filters.refined_lee import refined_lee_filter

import pytest


def test_refined_lee_filter_homogeneous_window():

    window = np.full((7, 7), 100.0)

    filtered = refined_lee_filter(window)

    assert filtered == 100.0



def test_refined_lee_filter_returns_finite_value():

    rng = np.random.default_rng(42)

    window = rng.uniform(10.0, 200.0, size=(7, 7))

    filtered = refined_lee_filter(window)

    assert np.isfinite(filtered)


def test_refined_lee_filter_within_window_range():

    rng = np.random.default_rng(123)

    window = rng.uniform(0.0, 500.0, size=(7, 7))

    filtered = refined_lee_filter(window)

    assert window.min() <= filtered <= window.max()


def test_refined_lee_filter_edge_preservation():

    window = np.ones((7, 7), dtype=float) * 50.0
    window[:, 3:] = 150.0

    filtered = refined_lee_filter(window)

    assert 50.0 <= filtered <= 150.


def test_refined_lee_filter_invalid_window():

    window = np.ones((5, 5))

    with pytest.raises(ValueError):
        refined_lee_filter(window)







