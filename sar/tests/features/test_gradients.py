import numpy as np
from sar.features.gradients import compute_composite_gradients
from sar.features.subwindow_grid import build_subwindow_mean_grid
from sar.features.directions import dominant_gradient
from sar.features.gradients import compute_signed_composite_gradients,compute_gradient_directions
from sar.filters.refined_lee import (
    _compute_signed_composite_gradients,_gradient_direction,Direction
)

def test_gradient_shape():

    image = np.ones((20,20))

    grid = build_subwindow_mean_grid(image)

    gradients = compute_composite_gradients(
        grid,
    )

    assert gradients.shape == (20,20,4)

def test_constant_image():

    image = np.full((20,20), 5.0)

    grid = build_subwindow_mean_grid(image)

    gradients = compute_composite_gradients(
        grid,
    )

    np.testing.assert_allclose(
        gradients,
        0.0,
    )


def test_signed_gradients_match_reference():
    rng = np.random.default_rng(42)

    mean_image = rng.random((30, 30))

    mean_grid = build_subwindow_mean_grid(
    mean_image
)

    assert mean_grid.shape == (30, 30, 3, 3)
    signed_gradients = compute_signed_composite_gradients(
    mean_grid
)
    row = 15
    col = 18

    grid = mean_grid[row, col]
    assert grid.shape == (3,3)

    means = grid.reshape(-1)

    expected = _compute_signed_composite_gradients(
    means
)
    np.testing.assert_allclose(
    signed_gradients[row, col],
    expected,
)

def test_signed_gradients_match_reference_random_pixels():

    rng = np.random.default_rng(42)

    mean_image = rng.random((40, 40))

    mean_grid = build_subwindow_mean_grid(
        mean_image
    )

    signed_gradients = compute_signed_composite_gradients(
        mean_grid
    )

    for _ in range(100):

        row = rng.integers(2, 38)
        col = rng.integers(2, 38)

        expected = _compute_signed_composite_gradients(
            mean_grid[row, col].reshape(-1)
        )

        actual = signed_gradients[row, col]

        np.testing.assert_allclose(
            actual,
            expected,
        )


def test_unsigned_gradients_are_absolute_value():

    rng = np.random.default_rng(0)

    mean_image = rng.random((30,30))

    mean_grid = build_subwindow_mean_grid(
        mean_image
    )

    signed = compute_signed_composite_gradients(
        mean_grid
    )

    unsigned = compute_composite_gradients(
        mean_grid
    )

    np.testing.assert_allclose(
        unsigned,
        np.abs(signed),
    )

from sar.filters.refined_lee import (
    _compute_composite_gradients,
)


def test_unsigned_gradients_match_reference():

    rng = np.random.default_rng(42)

    mean_image = rng.random((30,30))

    mean_grid = build_subwindow_mean_grid(
        mean_image
    )

    gradients = compute_composite_gradients(
        mean_grid
    )

    for _ in range(100):

        row = rng.integers(2,28)
        col = rng.integers(2,28)

        expected = _compute_composite_gradients(
            mean_grid[row,col].reshape(-1)
        )

        actual = gradients[row,col]

        np.testing.assert_allclose(
            actual,
            expected,
        )

def test_dominant_gradient_shape():

    rng = np.random.default_rng(42)

    gradients = rng.random(
        (20,20,4)
    )

    dominant = dominant_gradient(
        gradients
    )

    assert dominant.shape == (20,20)


def test_direction_shape():

    rng = np.random.default_rng(42)

    signed = rng.normal(
        size=(20,20,4)
    )

    directions = compute_gradient_directions(
        signed,
    )

    assert directions.shape == (20,20)

def test_positive_direction():

    signed = np.array(
        [[[2,5,1,3]]],
        dtype=float,
    )

    direction = compute_gradient_directions(
        signed,
    )

    assert direction[0,0] == Direction.NORTH_EAST

def test_negative_direction():

    signed = np.array(
        [[[-8,2,1,3]]],
        dtype=float,
    )

    direction = compute_gradient_directions(
        signed,
    )

    assert direction[0,0] == Direction.SOUTH

def test_reference_comparison():
    rng = np.random.default_rng(42)

    mean_image = rng.random((40,40))
    
    mean_grid = build_subwindow_mean_grid(
        mean_image,
    )
    
    signed = compute_signed_composite_gradients(
        mean_grid,
    )
    
    direction_image = compute_gradient_directions(
        signed,
    )
    
    for _ in range(100):
    
        row = rng.integers(2,38)
        col = rng.integers(2,38)
    
        expected = _gradient_direction(
            mean_grid[row,col].reshape(-1)
        )
    
        actual = Direction(
            direction_image[row,col])
