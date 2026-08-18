import numpy as np
import pytest

from sar.filters.refined_lee import _extract_subwindows

def test_returns_nine_subwindows():

    window = np.arange(1, 50).reshape(7, 7)

    subwindows = _extract_subwindows(window)

    assert subwindows.shape == (9, 3, 3)


def test_extracts_top_left_window():

    window = np.arange(1, 50).reshape(7, 7)

    subwindows = _extract_subwindows(window)

    expected = np.array([
        [1, 2, 3],
        [8, 9, 10],
        [15,16,17],
    ])

    np.testing.assert_array_equal(
        subwindows[0],
        expected,
    )


def test_extracts_central_window():

    window = np.arange(1, 50).reshape(7, 7)

    subwindows = _extract_subwindows(window)

    expected = np.array([
        [17,18,19],
        [24,25,26],
        [31,32,33],
    ])

    np.testing.assert_array_equal(
        subwindows[4],
        expected,
    )

def test_extracts_bottom_right_window():

    window = np.arange(1, 50).reshape(7, 7)

    subwindows = _extract_subwindows(window)

    expected = np.array([
        [33,34,35],
        [40,41,42],
        [47,48,49],
    ])

    np.testing.assert_array_equal(
        subwindows[8],
        expected,
    )


def test_requires_7_by_7_window():

    with pytest.raises(ValueError):

        _extract_subwindows(
            np.ones((5,5))
        )

    with pytest.raises(ValueError):

        _extract_subwindows(
            np.ones((7,6))
        )




