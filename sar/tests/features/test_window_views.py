import numpy as np

from sar.features.window_views import (
    build_window_view,
)


def test_window_view_shape():

    image = np.ones((20, 30))

    windows = build_window_view(image)

    assert windows.shape == (20, 30, 7, 7)


def test_window_view_constant():

    image = np.full((10, 10), 5.0)

    windows = build_window_view(image)

    np.testing.assert_allclose(
        windows,
        5.0,
    )

def test_window_view_center():

    image = np.arange(
        100,
        dtype=float,
    ).reshape(10, 10)

    windows = build_window_view(image)

    expected = image[2:9, 2:9]

    np.testing.assert_array_equal(
        windows[5, 5],
        expected,
    )


def test_window_view_corner():

    image = np.arange(
        25,
        dtype=float,
    ).reshape(5, 5)

    windows = build_window_view(
        image,
        window_size=3,
    )

    expected = np.pad(
        image,
        1,
        mode="reflect",
    )[0:3, 0:3]

    np.testing.assert_array_equal(
        windows[0, 0],
        expected,
    )


import pytest


def test_window_view_even_size():

    image = np.ones((10, 10))

    with pytest.raises(ValueError):
        build_window_view(
            image,
            window_size=4,
        )