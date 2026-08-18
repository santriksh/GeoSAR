"""
sar_change.py

Change detection algorithms for SAR imagery.

This module provides pixel-wise change operators
used for flood detection and other multi-temporal
SAR applications.
"""

from __future__ import annotations

import numpy as np

from .sar_image import SARImage
from .utils import _create_result

EPS = 1e-12


def _validate_change_inputs(
    before: SARImage,
    after: SARImage,
) -> None:
    """
    Validate that two SAR images are compatible
    for change detection.
    """

    #
    # Shape
    #
    if before.shape != after.shape:

        raise ValueError(
            "Images must have the same shape."
        )

    #
    # CRS
    #
    if before.crs != after.crs:

        raise ValueError(
            "Images must have the same CRS."
        )

    #
    # Value scale
    #
    if (
        before.value_scale
        !=
        after.value_scale
    ):

        raise ValueError(
            "Images must use the same value scale."
        )


def difference_change(
    before: SARImage,
    after: SARImage,
) -> SARImage:
    """
    Compute the pixel-wise difference
    between two SAR images.

    Difference is computed as

        after - before

    Parameters
    ----------
    before
        Pre-event SAR image.

    after
        Post-event SAR image.

    Returns
    -------
    SARImage
        Difference image.
    """

    _validate_change_inputs(
        before,
        after,
    )

    data = (
        after.data
        -
        before.data
    )

    mask = (
    before.mask
    &
    after.mask
    &
    np.isfinite(data)
)

    return _create_result(
        reference=after,
        data=data,
        mask=mask,
        operation="difference_change",
        value_scale=after.value_scale,
    )


def ratio_change(
    before: SARImage,
    after: SARImage,
) -> SARImage:
    """
    Compute the pixel-wise difference
    between two SAR images.

    Difference is computed as

        after - before

    Parameters
    ----------
    before
        Pre-event SAR image.

    after
        Post-event SAR image.

    Returns
    -------
    SARImage
        Difference image.
    """

    _validate_change_inputs(
        before,
        after,
    )

    data = after.data / np.maximum(
    before.data,
    EPS,
)

    mask = (
    before.mask
    &
    after.mask
    &
    np.isfinite(data)
)
    return _create_result(
        reference=after,
        data=data,
        mask=mask,
        operation="ratio_change",
        value_scale=after.value_scale,
    )


def log_ratio_change(
    before: SARImage,
    after: SARImage,
) -> SARImage:
    """
    Compute the logarithmic intensity ratio
    between two SAR images.

    The result is

        10 * log10(after / before)

    and is returned in dB.
    """

    _validate_change_inputs(
        before,
        after,
    )

    ratio = (
        after.data
        /
        np.maximum(
            before.data,
            EPS,
        )
    )

    data = (
        10.0
        *
        np.log10(
            ratio,
        )
    )

    mask = (
    before.mask
    &
    after.mask
    &
    np.isfinite(data)
)

    return _create_result(
        reference=after,
        data=data,
        mask=mask,
        operation="log_ratio_change",
        value_scale="dB",
    )