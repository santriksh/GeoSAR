"""
Radiometric operations for GeoSAR.
"""

from __future__ import annotations

import logging
from copy import deepcopy

import numpy as np

from .sar_geometry import _validate_pair
from .sar_image import SARImage

logger = logging.getLogger(__name__)

def _create_result(
    reference: SARImage,
    data: np.ndarray,
    mask: np.ndarray,
    operation: str,
    value_scale: str | None = None,
) -> SARImage:
    """
    Create a new SARImage from the result of an operation.

    Parameters
    ----------
    reference : SARImage
        Reference image whose metadata will be copied.

    data : np.ndarray
        Output raster.

    mask : np.ndarray
        Valid pixel mask.

    operation : str
        Name of the operation that generated the result.

    Returns
    -------
    SARImage
    """

    metadata = deepcopy(reference.metadata)
    metadata.provenance.operation = operation

    if value_scale is not None:
        metadata.processing.value_scale = value_scale

    metadata.provenance.operation = operation

    metadata.provenance.inputs = [
        "Derived from GeoSAR operation"
    ]

    return SARImage(
        data=data,
        mask=mask,
        metadata=metadata
    )

def difference(image1: SARImage,image2: SARImage,) -> SARImage:
    """
    Compute pixel-wise difference between two aligned SAR images.

    Parameters
    ----------
    image1 : SARImage
        Reference image.

    image2 : SARImage
        Second image.

    Returns
    -------
    SARImage
        Difference image (image2 - image1).
    """

    _validate_pair(image1, image2)

    data = image2.data - image1.data

    mask = image1.mask & image2.mask

    valid_fraction = mask.sum() / mask.size

    if valid_fraction < 0.5:
        #print(f"Warning: Only {valid_fraction:.1%} of pixels are valid in both images.")
        logger.warning(
    "Only %.1f%% of pixels are valid in both images.",
    valid_fraction * 100,
)

    

    return _create_result(
        reference=image1,
        data=data,
        mask=mask,
        operation="difference",
    )


def db_to_linear(image: SARImage) -> SARImage:
    """
    Convert SAR image from dB to linear scale.
    """

    if image.value_scale != "dB":
        raise ValueError(
            f"Expected image in dB. Found '{image.value_scale}'."
        )

    data = np.power(10.0, image.data / 10.0)

    mask = image.mask.copy()
    mask = image.mask & np.isfinite(data)
    
    return _create_result(
        reference=image,
        data=data,
        mask=mask,
        operation="db_to_linear",
        value_scale="Linear",
    )


def linear_to_db(image: SARImage) -> SARImage:
    """
    Convert SAR image from Linear power to dB.

    Parameters
    ----------
    image : SARImage
        SAR image in linear scale.

    Returns
    -------
    SARImage
        SAR image in dB scale.
    """

    if image.value_scale != "Linear":
        raise ValueError(
            f"Expected image in Linear scale. Found '{image.value_scale}'."
        )

    # Avoid log10(0) and negative values
    data = np.where(
        image.data > 0,
        10.0 * np.log10(image.data),
        np.nan
    )

    mask = image.mask.copy()
    mask = image.mask & np.isfinite(data)

    return _create_result(
        reference=image,
        data=data,
        mask=mask,
        operation="linear_to_db",
        value_scale="dB"
    )


def ratio(
    image1: SARImage,
    image2: SARImage,
) -> SARImage:
    """
    Compute the linear backscatter ratio between two SAR images.

    Parameters
    ----------
    image1 : SARImage
        Reference (pre-event) image in dB.

    image2 : SARImage
        Comparison (post-event) image in dB.

    Returns
    -------
    SARImage
        Linear ratio image (image2 / image1).
    """

    _validate_pair(image1, image2)

    pre_linear = db_to_linear(image1)

    post_linear = db_to_linear(image2)

    data = np.divide(
        post_linear.data,
        pre_linear.data,
        out=np.full_like(pre_linear.data, np.nan),
        where=pre_linear.data > 0
    )

    mask = (
        pre_linear.mask
        &
        post_linear.mask
        &
        np.isfinite(data)
    )

    return _create_result(
        reference=image1,
        data=data,
        mask=mask,
        operation="ratio",
        value_scale="Linear"
    )
