from sar.visualization.stretch import percentile_stretch
import numpy as np


def test_output_between_zero_and_one():

    image = np.arange(
        100,
        dtype=np.float32,
    ).reshape(10,10)

    result = percentile_stretch(
        image,
    )

    assert result.min() >= 0

    assert result.max() <= 1


def test_nan_preserved():

    image = np.array(
        [
            [1,2],
            [np.nan,4],
        ],
        dtype=np.float32,
    )

    result = percentile_stretch(
        image,
    )

    assert np.isnan(
        result[1,0]
    )


import pytest

def test_invalid_percentiles():

    image = np.ones((5,5))

    with pytest.raises(ValueError):

        percentile_stretch(
            image,
            95,
            5,
        )

def test_constant_image():

    image = np.full(
        (10,10),
        7.0,
    )

    result = percentile_stretch(
        image,
    )

    assert np.all(
        np.isfinite(result)
    )


def test_all_nan():

    image = np.full(
        (10,10),
        np.nan,
    )

    with pytest.raises(ValueError):

        percentile_stretch(
            image,
        )