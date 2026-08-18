"""
Tests for morphology validation.
"""

import numpy as np
import pytest

from sar.morphology.validation import (
    validate_binary_image,
)

from sar.tests.utils import (
    make_test_image,
)

def test_accepts_binary_image(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [0,1,1],
                [0,0,1],
                [1,0,0],
            ],
            dtype=np.uint8,
        ),
    )

    validate_binary_image(
        image,
    )

def test_rejects_grayscale_image(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [0,2,1],
                [0,1,1],
                [1,0,0],
            ],
            dtype=np.uint8,
        ),
    )

    with pytest.raises(ValueError):

        validate_binary_image(
            image,
        )


def test_rejects_float_values(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [0.0,0.4],
                [1.0,0.8],
            ],
            dtype=np.float32,
        ),
    )

    with pytest.raises(ValueError):

        validate_binary_image(
            image,
        )


def test_mask_shape_mismatch(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.zeros(
            (3,3),
            dtype=np.uint8,
        ),
        mask=np.ones(
            (2,2),
            dtype=bool,
        ),
    )

    with pytest.raises(ValueError):

        validate_binary_image(
            image,
        )

def test_ignores_nodata_outside_mask(
    sample_image,
):

    data = np.array(
        [
            [0,1],
            [np.nan,5],
        ],
        dtype=np.float32,
    )

    mask = np.array(
        [
            [True,True],
            [False,False],
        ]
    )

    image = make_test_image(
        template=sample_image,
        data=data,
        mask=mask,
    )

    validate_binary_image(
        image,
    )


