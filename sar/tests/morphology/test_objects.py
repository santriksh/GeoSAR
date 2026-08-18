"""
Tests for object filtering.

Important:

remove_small_objects() operates on
CONNECTED COMPONENTS.

A single foreground pixel is removed only
if it forms a connected component whose size
is smaller than min_size.

"""

import numpy as np
import pytest

from sar.morphology.objects import (
    remove_small_objects,
)

from sar.tests.utils import (
    make_test_image,
)

def test_small_connected_component_is_removed(
    sample_image,
):
    """
    Input

    [1,1,1,0,0],
    [1,1,1,0,0],
    [0,0,0,0,1],

    min_size = 2

    Expected

    [1,1,1,0,0],
    [1,1,1,0,0],
    [0,0,0,0,0],
    """

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,1,1,0,0],
                [1,1,1,0,0],
                [0,0,0,0,1],
            ],
            dtype=np.uint8,
        ),
    )

    result = remove_small_objects(
        image,
        min_size=2,
    )

    expected = np.array(
        [
            [1,1,1,0,0],
            [1,1,1,0,0],
            [0,0,0,0,0],
        ],
        dtype=np.uint8,
    )

    assert np.array_equal(
        result.data,
        expected,
    )

def test_large_object_is_preserved(
    sample_image,
):
    """
    Input

    111

    111

    min_size = 4

    Expected

    unchanged
    """

    data = np.ones(
        (2,3),
        dtype=np.uint8,
    )

    image = make_test_image(
        template=sample_image,
        data=data,
    )

    result = remove_small_objects(
        image,
        min_size=4,
    )

    assert np.array_equal(
        result.data,
        data,
    )

def test_all_objects_removed_when_threshold_is_large(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,0,1],
                [0,0,0],
                [1,0,0],
            ],
            dtype=np.uint8,
        ),
    )

    result = remove_small_objects(
        image,
        min_size=100,
    )

    assert np.all(result.data == 0)


def test_min_size_one_keeps_every_object(
    sample_image,
):

    data = np.array(
        [
            [1,0,1],
            [0,0,0],
            [1,0,0],
        ],
        dtype=np.uint8,
    )

    image = make_test_image(
        template=sample_image,
        data=data,
    )

    result = remove_small_objects(
        image,
        min_size=1,
    )

    assert np.array_equal(
        result.data,
        data,
    )

def test_diagonal_pixels_are_removed_under_four_connectivity(
    sample_image,
):
    """
    Three diagonal pixels are three separate
    one-pixel objects under 4-connectivity.
    """

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,0,0],
                [0,1,0],
                [0,0,1],
            ],
            dtype=np.uint8,
        ),
    )

    result = remove_small_objects(
        image,
        min_size=2,
        connectivity=1,
    )

    assert np.all(result.data == 0)

def test_diagonal_pixels_form_one_object_under_eight_connectivity(
    sample_image,
):
    """
    Three diagonal pixels form one object
    under 8-connectivity.
    """

    data = np.array(
        [
            [1,0,0],
            [0,1,0],
            [0,0,1],
        ],
        dtype=np.uint8,
    )

    image = make_test_image(
        template=sample_image,
        data=data,
    )

    result = remove_small_objects(
        image,
        min_size=2,
        connectivity=2,
    )

    assert np.array_equal(
        result.data,
        data,
    )

def test_invalid_min_size_raises_value_error(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.ones(
            (3,3),
            dtype=np.uint8,
        ),
    )

    with pytest.raises(ValueError):

        remove_small_objects(
            image,
            min_size=0,
        )

def test_invalid_connectivity_raises_value_error(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.ones(
            (3,3),
            dtype=np.uint8,
        ),
    )

    with pytest.raises(ValueError):

        remove_small_objects(
            image,
            connectivity=5,
        )

def test_non_binary_image_raises_value_error(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [0,2],
                [1,1],
            ],
            dtype=np.uint8,
        ),
    )

    with pytest.raises(ValueError):

        remove_small_objects(
            image,
        )

def test_mask_is_preserved(
    sample_image,
):

    mask = np.array(
        [
            [True,False],
            [True,True],
        ]
    )

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,1],
                [0,1],
            ],
            dtype=np.uint8,
        ),
        mask=mask,
    )

    result = remove_small_objects(
        image,
    )

    assert np.array_equal(
        result.mask,
        mask,
    )

def test_operation_metadata_is_updated(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.ones(
            (3,3),
            dtype=np.uint8,
        ),
    )

    result = remove_small_objects(
        image,
    )

    assert (
        result.metadata.provenance.operation
        ==
        "remove_small_objects"
    )

    assert (
        result.value_scale
        ==
        image.value_scale
    )

def test_output_geometry_is_preserved(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.ones(
            (5,7),
            dtype=np.uint8,
        ),
    )

    result = remove_small_objects(
        image,
    )

    assert result.shape == image.shape
    assert result.crs == image.crs

    

