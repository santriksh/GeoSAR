from __future__ import annotations

from copy import deepcopy
from functools import cache

import numpy as np
from rasterio.warp import Resampling, reproject

from .sar_image import SARImage


def _validate_pair(
    image1: SARImage,
    image2: SARImage,
) -> None:
    """
    Validate that two SAR images are compatible for
    pixel-wise operations.
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
            "Resolution mismatch."
        )

def copy_image(image: SARImage) -> SARImage:
    """
    Create a deep copy of a SARImage.

    Parameters
    ----------
    image : SARImage

    Returns
    -------
    SARImage
    """

    return SARImage(

        data=image.data.copy(),

        mask=image.mask.copy(),

        metadata=image.metadata)

def create_empty_like(image: SARImage,dtype=None) -> np.ndarray:
    """
    Create an empty NumPy array having the same
    shape as the reference image.
    """

    if dtype is None:
        dtype = image.data.dtype

    return np.empty(
        image.shape,
        dtype=dtype
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


def align_to_reference(reference: SARImage,moving: SARImage,resampling: Resampling = Resampling.bilinear,) -> SARImage:
    # print("\nInside align_to_reference()")
    # print("Reference :", reference.data.shape)
    # print("Moving    :", moving.data.shape)

    if reference.crs != moving.crs:
        raise ValueError("Both CRS are not same")

    aligned = create_empty_like(
    reference,
    dtype=np.float32)

    reproject(
    source=moving.data,
    destination=aligned,

    src_transform=moving.metadata.spatial.transform,
    src_crs=moving.crs,

    dst_transform=reference.metadata.spatial.transform,
    dst_crs=reference.crs,

    resampling=resampling)

    mask = ~np.isnan(aligned)

    print("Aligned   :", aligned.shape)

    return SARImage(data=aligned,

    mask=mask,

    metadata=deepcopy(reference.metadata))
    
@cache
def _distance_matrix(
    window_size: int,
) -> np.ndarray:
    """
    Compute the Euclidean distance from the center pixel.

    Parameters
    ----------
    window_size : int
        Size of the square moving window.
        Must be a positive odd integer.

    Returns
    -------
    np.ndarray
        Distance matrix of shape
        (window_size, window_size).
    """

    if window_size < 1:
        raise ValueError(
            "window_size must be positive."
        )

    if window_size % 2 == 0:
        raise ValueError(
            "window_size must be odd."
        )

    radius = window_size // 2

    y, x = np.mgrid[
        -radius:radius + 1,
        -radius:radius + 1
    ]

    distance = np.sqrt(
        x**2 + y**2
    )

    return distance.astype(float)



