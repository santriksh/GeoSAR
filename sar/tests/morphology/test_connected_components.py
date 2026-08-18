"""
Tests for connected component labeling.
"""

import numpy as np
import pytest

from sar.morphology.connected_components import (
    label_connected_components,
)

from sar.tests.utils import (
    make_test_image,
)

def test_empty_image_has_zero_objects(
    sample_image,
):
    """
    Input

    000
    000
    000

    Expected

    0 objects
    """

    image = make_test_image(
        template=sample_image,
        data=np.zeros(
            (3,3),
            dtype=np.uint8,
        ),
    )

    labels, num = label_connected_components(
        image,
    )

    assert num == 0

    assert np.all(labels == 0)


def test_full_image_is_single_object(
    sample_image,
):
    """
    Input

    111
    111
    111

    Expected

    1 object
    """

    image = make_test_image(
        template=sample_image,
        data=np.ones(
            (3,3),
            dtype=np.uint8,
        ),
    )

    labels, num = label_connected_components(
        image,
    )

    assert num == 1

def test_three_isolated_pixels_form_three_objects(
    sample_image,
):
    """
    Input

    100

    001

    010
    """

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,0,0],
                [0,0,1],
                [0,1,0],
            ],
            dtype=np.uint8,
        ),
    )

    _, num = label_connected_components(
        image,
        connectivity=1,
    )

    assert num == 3

def test_diagonal_pixels_are_separate_under_four_connectivity(
    sample_image,
):
    """
    Input

    10

    01

    Expected

    2 objects
    """

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,0],
                [0,1],
            ],
            dtype=np.uint8,
        ),
    )

    _, num = label_connected_components(
        image,
        connectivity=1,
    )

    assert num == 2


def test_diagonal_pixels_are_connected_under_eight_connectivity(
    sample_image,
):
    """
    Input

    10

    01

    Expected

    1 object
    """

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,0],
                [0,1],
            ],
            dtype=np.uint8,
        ),
    )

    _, num = label_connected_components(
        image,
        connectivity=2,
    )

    assert num == 1

def test_diagonally_touching_regions_merge_under_eight_connectivity(
    sample_image,
):
    """
    Input

    1100

    1100

    0011

    0011
    """

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,1,0,0],
                [1,1,0,0],
                [0,0,1,1],
                [0,0,1,1],
            ],
            dtype=np.uint8,
        ),
    )

    _, num = label_connected_components(
        image,
    )

    assert num == 1

def test_separated_regions_remain_two_objects(
    sample_image,
):
    """
    Input
    11000
    11000
    00011
    00011
    """

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,1,0,0,0],
                [1,1,0,0,0],
                [0,0,0,1,1],
                [0,0,0,1,1],
            ],
            dtype=np.uint8,
        ),
    )

    _, num = label_connected_components(
        image,
    )

    assert num == 2


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

        label_connected_components(
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

        label_connected_components(
            image,
        )

def test_background_is_label_zero(
    sample_image,
):

    image = make_test_image(
        template=sample_image,
        data=np.array(
            [
                [1,0],
                [0,1],
            ],
            dtype=np.uint8,
        ),
    )

    labels, _ = label_connected_components(
        image,
        connectivity=1,
    )

    assert 0 in np.unique(labels)


def test_labels_are_consecutive(
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

    labels, _ = label_connected_components(
        image,
    )

    unique = np.unique(labels)

    assert np.array_equal(
        unique,
        np.arange(unique.max()+1),
    )