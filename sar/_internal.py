from __future__ import annotations

from copy import deepcopy

import numpy as np

from .sar_image import SARImage

"""
Internal helper functions shared across GeoSAR modules.

These utilities are not part of the public API.
"""

def _validate_same_grid(
    image1: SARImage,
    image2: SARImage,
) -> None:
    """
    Validate that two images occupy the same spatial grid.
    """

    if image1.shape != image2.shape:
        raise ValueError(
            f"Shape mismatch: {image1.shape} vs {image2.shape}"
        )

    if image1.crs != image2.crs:
        raise ValueError(
            "CRS mismatch."
        )

    if image1.transform != image2.transform:
        raise ValueError(
            "Transform mismatch."
        )


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

    if value_scale is not None:
        metadata.processing.value_scale = value_scale

    metadata.provenance.operation = operation

    metadata.provenance.inputs = [
        "Derived from GeoSAR operation"
    ]

    return SARImage(
        data=data,
        mask=mask,
        metadata=metadata,
        )
