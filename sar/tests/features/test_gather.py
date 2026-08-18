import numpy as np
from sar.filters.refined_lee import _estimate_noise_variance

from sar.features.gather import (
    gather_directional_values,
)


def test_gather_shape():

    values = np.ones((20,30,8))

    directions = np.zeros(
        (20,30),
        dtype=int,
    )

    result = gather_directional_values(
        values,
        directions,
    )

    assert result.shape == (20,30)



def test_gather_constant():

    values = np.full(
        (10,10,8),
        5.0,
    )

    directions = np.random.randint(
        0,
        8,
        size=(10,10),
    )

    result = gather_directional_values(
        values,
        directions,
    )

    np.testing.assert_allclose(
        result,
        5.0,
    )


def test_gather_unique():

    values = np.zeros(
        (2,2,8),
        dtype=float,
    )

    for d in range(8):

        values[...,d] = d

    directions = np.array(
        [
            [0,3],
            [5,7],
        ]
    )

    expected = np.array(
        [
            [0,3],
            [5,7],
        ],
        dtype=float,
    )

    actual = gather_directional_values(
        values,
        directions,
    )

    np.testing.assert_array_equal(
        actual,
        expected,
    )


def test_gather_matches_loop():

    rng = np.random.default_rng(42)

    values = rng.random((20,20,8))

    directions = rng.integers(
        0,
        8,
        size=(20,20),
    )

    expected = np.empty((20,20))

    for r in range(20):
        for c in range(20):

            expected[r,c] = values[
                r,
                c,
                directions[r,c],
            ]

    actual = gather_directional_values(
        values,
        directions,
    )

    np.testing.assert_allclose(
        actual,
        expected,
    )