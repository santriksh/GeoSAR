"""
Tests for sar_change.py
"""

import numpy as np
import pytest

from dataclasses import replace

from sar.sar_change import (
    difference_change,
    ratio_change,
    log_ratio_change,
)

from sar.tests.utils import make_test_image


# ==========================================================
# Difference
# ==========================================================

def test_difference_change(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        data=np.array(
            [
                [1, 2],
                [3, 4],
            ],
            dtype=np.float32,
        ),
    )

    after = make_test_image(
        template=sample_linear_image,
        data=np.array(
            [
                [2, 3],
                [2, 6],
            ],
            dtype=np.float32,
        ),
    )

    result = difference_change(before, after)

    expected = np.array(
        [
            [1, 1],
            [-1, 2],
        ],
        dtype=np.float32,
    )

    np.testing.assert_allclose(result.data, expected)


# ==========================================================
# Ratio
# ==========================================================

def test_ratio_change(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        data=np.array(
            [
                [2, 4],
                [5, 10],
            ],
            dtype=np.float32,
        ),
    )

    after = make_test_image(
        template=sample_linear_image,
        data=np.array(
            [
                [4, 8],
                [10, 5],
            ],
            dtype=np.float32,
        ),
    )

    result = ratio_change(before, after)

    expected = np.array(
        [
            [2.0, 2.0],
            [2.0, 0.5],
        ],
        dtype=np.float32,
    )

    np.testing.assert_allclose(result.data, expected)


# ==========================================================
# Log Ratio
# ==========================================================

def test_log_ratio_change(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        data=np.array(
            [
                [1],
                [10],
            ],
            dtype=np.float32,
        ),
    )

    after = make_test_image(
        template=sample_linear_image,
        data=np.array(
            [
                [10],
                [10],
            ],
            dtype=np.float32,
        ),
    )

    result = log_ratio_change(before, after)

    expected = np.array(
        [
            [10.0],
            [0.0],
        ],
        dtype=np.float32,
    )

    np.testing.assert_allclose(
        result.data,
        expected,
        atol=1e-6,
    )


# ==========================================================
# Shape Validation
# ==========================================================

def test_shape_validation(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        data=np.ones((2, 2), dtype=np.float32),
    )

    after = make_test_image(
        template=sample_linear_image,
        data=np.ones((3, 3), dtype=np.float32),
    )

    with pytest.raises(ValueError):
        difference_change(before, after)


# ==========================================================
# CRS Validation
# ==========================================================

def test_crs_validation(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
    )

    after = make_test_image(
        template=sample_linear_image,
    )

    after.metadata = replace(
        after.metadata,
        spatial=replace(
            after.metadata.spatial,
            crs="EPSG:4326",
        ),
    )

    with pytest.raises(ValueError):
        difference_change(before, after)


# ==========================================================
# Value Scale Validation
# ==========================================================

def test_value_scale_validation(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        value_scale="linear",
    )

    after = make_test_image(
        template=sample_linear_image,
        value_scale="dB",
    )

    with pytest.raises(ValueError):
        difference_change(before, after)


# ==========================================================
# Mask Propagation
# ==========================================================

def test_mask_propagation(sample_linear_image):

    mask1 = np.array(
        [
            [True, False],
            [True, True],
        ]
    )

    mask2 = np.array(
        [
            [True, True],
            [False, True],
        ]
    )

    before = make_test_image(
        template=sample_linear_image,
        data=np.ones((2, 2), dtype=np.float32),
        mask=mask1,
    )

    after = make_test_image(
        template=sample_linear_image,
        data=np.ones((2, 2), dtype=np.float32),
        mask=mask2,
    )

    result = difference_change(before, after)

    expected = mask1 & mask2

    np.testing.assert_array_equal(
        result.mask,
        expected,
    )


# ==========================================================
# Divide by Zero
# ==========================================================

def test_ratio_zero_division(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        data=np.array([[0]], dtype=np.float32),
    )

    after = make_test_image(
        template=sample_linear_image,
        data=np.array([[5]], dtype=np.float32),
    )

    result = ratio_change(before, after)

    assert np.isfinite(result.data).all()


def test_log_ratio_zero_division(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        data=np.array([[0]], dtype=np.float32),
    )

    after = make_test_image(
        template=sample_linear_image,
        data=np.array([[5]], dtype=np.float32),
    )

    result = log_ratio_change(before, after)

    assert np.isfinite(result.data).all()


# ==========================================================
# Identity Test
# ==========================================================

def test_identity(sample_linear_image):

    before = make_test_image(
        template=sample_linear_image,
        data=sample_linear_image.data.copy(),
    )

    after = make_test_image(
        template=sample_linear_image,
        data=sample_linear_image.data.copy(),
    )

    diff = difference_change(before, after)
    ratio = ratio_change(before, after)
    log = log_ratio_change(before, after)

    np.testing.assert_allclose(diff.data, 0.0)
    np.testing.assert_allclose(ratio.data, 1.0)
    np.testing.assert_allclose(log.data, 0.0, atol=1e-6)