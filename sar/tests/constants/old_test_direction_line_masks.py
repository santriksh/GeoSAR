import numpy as np

from sar.constants.refined_lee import (
    Direction,
    _DIRECTION_LINE_MASKS,
)

from sar.filters.refined_lee import (
    _extract_directional_pixels,
)



def test_line_mask_shape():

    for mask in _DIRECTION_LINE_MASKS.values():

        assert mask.shape == (7, 7)


def test_line_mask_contains_seven_pixels():

    for mask in _DIRECTION_LINE_MASKS.values():

        assert np.sum(mask) == 7


def test_line_mask_contains_center():

    for mask in _DIRECTION_LINE_MASKS.values():

        assert mask[3, 3]



def test_line_masks_match_reference():

    window = np.arange(
        49,
        dtype=float,
    ).reshape(7, 7)

    for direction in Direction:

        expected = _extract_directional_pixels(
            window,
            direction,
        )

        actual = window[
            _DIRECTION_LINE_MASKS[direction]
        ]

        np.testing.assert_array_equal(
            actual,
            expected,
        )