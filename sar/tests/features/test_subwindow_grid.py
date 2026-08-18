import numpy as np
from sar.features.subwindow_grid import build_subwindow_mean_grid

def test_shape():

    image = np.ones((10, 15))

    grid = build_subwindow_mean_grid(image)

    assert grid.shape == (10, 15, 3, 3)


def test_constant():

    image = np.full((8, 8), 7.5)

    grid = build_subwindow_mean_grid(image)

    np.testing.assert_allclose(
        grid,
        7.5,
    )

def test_center_slice():

    image = np.arange(25).reshape(5,5).astype(float)

    grid = build_subwindow_mean_grid(image)

    np.testing.assert_array_equal(
        grid[...,1,1],
        image,
    )

def test_subwindow_grid_matches_reference():

    rng = np.random.default_rng(42)

    mean_image = rng.random((20, 20))

    grid = build_subwindow_mean_grid(mean_image)

    for _ in range(100):

        row = rng.integers(2, 18)
        col = rng.integers(2, 18)

        expected = mean_image[
            row-2:row+3:2,
            col-2:col+3:2,
        ]

        np.testing.assert_allclose(
            grid[row, col],
            expected,
        )

    



