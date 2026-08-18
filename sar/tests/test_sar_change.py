import numpy as np

import pytest

from copy import deepcopy

from sar.sar_change import (
    difference_change,ratio_change,log_ratio_change
)

from sar.sar_image import SARImage


def test_difference_returns_sarimage(
    sample_linear_image,
):

    result = difference_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert isinstance(
        result,
        SARImage,
    )


def test_difference_values(
    sample_linear_image,
):

    result = difference_change(
        sample_linear_image,
        sample_linear_image,
    )

    np.testing.assert_allclose(
        result.data,
        0.0,
    )


def test_difference_preserves_mask(
    sample_linear_image,
):

    result = difference_change(
        sample_linear_image,
        sample_linear_image,
    )

    np.testing.assert_array_equal(
        result.mask,
        sample_linear_image.mask,
    )


def test_difference_operation(
    sample_linear_image,
):

    result = difference_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert (
        result.metadata
        .provenance
        .operation
        ==
        "difference_change"
    )



def test_difference_operation(
    sample_linear_image,
):

    result = difference_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert (
        result.metadata
        .provenance
        .operation
        ==
        "difference_change"
    )


def test_difference_shape_mismatch(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    after = deepcopy(
        sample_linear_image,
    )

    after.data = np.zeros(
        (
            10,
            10,
        )
    )

    after.mask = np.ones(
        (
            10,
            10,
        ),
        dtype=bool,
    )

    with pytest.raises(
        ValueError,
    ):

        difference_change(
            before,
            after,
        )


def test_difference_value_scale_mismatch(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    after = deepcopy(
        sample_linear_image,
    )

    after.metadata.processing.value_scale = (
        "dB"
    )

    with pytest.raises(
        ValueError,
    ):

        difference_change(
            before,
            after,
        )

##################################

def test_ratio_returns_sarimage(
    sample_linear_image,
):

    result = ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert isinstance(
        result,
        SARImage,
    )


def test_ratio_values(
    sample_linear_image,
):

    result = ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    np.testing.assert_allclose(
        result.data,
        1.0,
    )


def test_ratio_preserves_mask(
    sample_linear_image,
):

    result = ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    np.testing.assert_array_equal(
        result.mask,
        sample_linear_image.mask,
    )


def test_ratio_operation(
    sample_linear_image,
):

    result = ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert (
        result.metadata
        .provenance
        .operation
        ==
        "ratio_change"
    )



def test_ratio_operation(
    sample_linear_image,
):

    result = ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert (
        result.metadata
        .provenance
        .operation
        ==
        "ratio_change"
    )


def test_ratio_shape_mismatch(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    after = deepcopy(
        sample_linear_image,
    )

    after.data = np.zeros(
        (
            10,
            10,
        )
    )

    after.mask = np.ones(
        (
            10,
            10,
        ),
        dtype=bool,
    )

    with pytest.raises(
        ValueError,
    ):

        ratio_change(
            before,
            after,
        )


def test_ratio_value_scale_mismatch(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    after = deepcopy(
        sample_linear_image,
    )

    after.metadata.processing.value_scale = (
        "dB"
    )

    with pytest.raises(
        ValueError,
    ):

        ratio_change(
            before,
            after,
        )

def test_division_by_zero(sample_linear_image,):
    before = deepcopy(
    sample_linear_image,
)

    before.data[:] = 0
    
    result = ratio_change(
        before,
        sample_linear_image,
    )
    
    assert np.isfinite(
        result.data,
    ).all()

###############################
def test_log_ratio_returns_sarimage(
    sample_linear_image,
):

    result = log_ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert isinstance(
        result,
        SARImage,
    )


def test_log_ratio_identical_images(
    sample_linear_image,
):

    result = log_ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    np.testing.assert_allclose(
        result.data,
        0.0,
    )

def test_log_ratio_known_value(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    after = deepcopy(
        sample_linear_image,
    )

    before.data[:] = 1.0
    after.data[:] = 10.0

    result = log_ratio_change(
        before,
        after,
    )

    np.testing.assert_allclose(
        result.data,
        10.0,
    )


def test_log_ratio_value_scale(
    sample_linear_image,
):

    result = log_ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert (
        result.value_scale
        ==
        "dB"
    )



def test_log_ratio_preserves_mask(
    sample_linear_image,
):

    result = log_ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    np.testing.assert_array_equal(
        result.mask,
        sample_linear_image.mask,
    )


def test_log_ratio_operation(
    sample_linear_image,
):

    result = log_ratio_change(
        sample_linear_image,
        sample_linear_image,
    )

    assert (
        result.metadata.provenance.operation
        ==
        "log_ratio_change"
    )


def test_log_ratio_division_by_zero(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    before.data[:] = 0.0

    result = log_ratio_change(
        before,
        sample_linear_image,
    )

    assert np.isfinite(
        result.data,
    ).all()

def test_log_ratio_shape_mismatch(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    after = deepcopy(
        sample_linear_image,
    )

    after.data = np.zeros(
        (10,10),
    )

    after.mask = np.ones(
        (10,10),
        dtype=bool,
    )

    with pytest.raises(
        ValueError,
    ):
        log_ratio_change(
            before,
            after,
        )

def test_log_ratio_value_scale_mismatch(
    sample_linear_image,
):

    before = deepcopy(
        sample_linear_image,
    )

    after = deepcopy(
        sample_linear_image,
    )

    after.metadata.processing.value_scale = "dB"

    with pytest.raises(
        ValueError,
    ):
        log_ratio_change(
            before,
            after,
        )        
    