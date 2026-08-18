import numpy as np
import pytest

from sar.constants.refined_lee import (
    Direction,
    DIRECTION_MASKS,
)
from sar.filters.refined_lee import (
    _extract_directional_pixels,
)

@pytest.mark.parametrize(
    "direction",
    list(Direction),
)
def test_extracts_28_pixels(direction):

    window = np.arange(49).reshape(7, 7)

    pixels = _extract_directional_pixels(
        window,
        direction,
    )

    assert pixels.shape == (28,)


@pytest.mark.parametrize(
    "direction",
    list(Direction),
)
def test_pixels_are_unique(direction):

    window = np.arange(49).reshape(7, 7)

    pixels = _extract_directional_pixels(
        window,
        direction,
    )

    assert len(np.unique(pixels)) == 28


@pytest.mark.parametrize(
    "direction",
    list(Direction),
)
def test_matches_direction_mask(direction):

    window = np.arange(49).reshape(7, 7)

    expected = window[
        DIRECTION_MASKS[direction]
    ]

    actual = _extract_directional_pixels(
        window,
        direction,
    )

    np.testing.assert_array_equal(
        actual,
        expected,
    )


def test_direction_masks():

    for mask in DIRECTION_MASKS.values():

        assert mask.shape == (7, 7)
        assert mask.dtype == bool
        assert mask.sum() == 28

@pytest.mark.parametrize(
    "direction",
    list(Direction),
)
def test_contains_center_pixel(direction):

    mask = DIRECTION_MASKS[direction]

    assert mask[3, 3]