import numpy as np
import pytest

from sar.constants import refined_lee

from sar.filters.refined_lee import _directional_statistics,_extract_directional_pixels

from sar.constants.refined_lee import (
    DIRECTION_MASKS,
    Direction,
    REFINED_LEE_CENTER,
    REFINED_LEE_WINDOW_SHAPE,
)

def test_constant_window():

    window = np.full(
        (7, 7),
        42.0,
    )

    mean, variance = _directional_statistics(
        window,
        Direction.NORTH,
    )

    assert mean == pytest.approx(42.0)
    assert variance == pytest.approx(0.0)

@pytest.mark.parametrize(
    "direction",
    list(Direction),
)
def test_statistics_match_numpy(direction):

    window = np.arange(49).reshape(7, 7)

    pixels = _extract_directional_pixels(
        window,
        direction,
    )

    mean, variance = _directional_statistics(
        window,
        direction,
    )

    assert mean == pytest.approx(
        np.mean(pixels)
    )

    assert variance == pytest.approx(
        np.var(pixels)
    )


@pytest.mark.parametrize(
    "direction",
    list(Direction),
)
def test_variance_non_negative(direction):

    rng = np.random.default_rng(42)

    window = rng.random((7, 7))

    _, variance = _directional_statistics(
        window,
        direction,
    )

    assert variance >= 0


def test_all_masks_have_same_number_of_pixels():

    for mask in DIRECTION_MASKS.values():
        assert mask.sum() == 28