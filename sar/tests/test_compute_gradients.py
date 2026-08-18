import numpy as np
import pytest

from sar.filters.refined_lee import _compute_composite_gradients


def test_returns_four_gradients():
    means = np.arange(1, 10, dtype=float)

    gradients = _compute_composite_gradients(means)

    assert gradients.shape == (4,)


def test_computes_expected_gradients():
    means = np.array(
        [
            1, 2, 3,
            4, 5, 6,
            7, 8, 9,
        ],
        dtype=float,
    )

    gradients = _compute_composite_gradients(means)

    expected = np.array(
    [
        10.0,
        10.0,
        2.0,
        14.0,
    ]
)

    np.testing.assert_array_equal(
        gradients,
        expected,
    )


def test_requires_nine_means():
    with pytest.raises(ValueError):
        _compute_composite_gradients(np.ones(8))


