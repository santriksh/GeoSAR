from __future__ import annotations

from copy import deepcopy

import numpy as np

from .sar_image import SARImage


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