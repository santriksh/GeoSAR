"""
Flood detection algorithms for SAR imagery.

This module converts SAR change images into
binary flood masks.
"""

import numpy as np

from .sar_image import SARImage
from .sar_radiometry import _create_result


def _validate_threshold_inputs(
    image: SARImage,
    direction: str,
) -> None:
    """
    Validate inputs for flood thresholding.

    Parameters
    ----------
    image : SARImage
        Input change image.

    direction : str
        Threshold direction.

    Raises
    ------
    ValueError
        If direction is invalid.
    """

    if direction not in ("less", "greater"):
        raise ValueError(
            "direction must be either "
            "'less' or 'greater'."
        )


def threshold_flood(
    image: SARImage,
    threshold: float,
    direction: str = "less",
) -> SARImage:
    """
    Convert a SAR change image into a binary flood mask.

    Parameters
    ----------
    image : SARImage
        Input change image.

    threshold : float
        Flood threshold.

    direction : {"less", "greater"}, default="less"
        Threshold direction.

        "less"
            Flood if pixel < threshold.

        "greater"
            Flood if pixel > threshold.

    Returns
    -------
    SARImage
        Binary flood mask.
    """

    _validate_threshold_inputs(
        image,
        direction,
    )

    if direction == "less":

        flood = (
            image.mask
            &
            (image.data < threshold)
        )

    else:

        flood = (
            image.mask
            &
            (image.data > threshold)
        )

    data = flood.astype(np.float32)

    mask = image.mask.copy()

    return _create_result(
        reference=image,
        data=data,
        mask=mask,
        operation="threshold_flood",
        #value_scale=image.value_scale,
        value_scale="Binary",
    )
