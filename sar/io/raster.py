from dataclasses import replace

import numpy as np
import rasterio
from rasterio.coords import BoundingBox
from rasterio.transform import array_bounds

from sar.io.models import (
    RasterInfo,
    RasterStatistics,
)


def read_raster(
    path: str,
) -> tuple[np.ndarray, RasterInfo]:
    """
    Read the first band of a raster.

    Parameters
    ----------
    path
        Path to the raster.

    Returns
    -------
    image
        First raster band.

    info
        Raster metadata.
    """

    with rasterio.open(path) as src:

        image = src.read(1)

        info = RasterInfo(
            width=src.width,
            height=src.height,
            count=src.count,
            dtype=src.dtypes[0],
            crs=src.crs,
            transform=src.transform,
            nodata=src.nodata,
        )

    return image, info


def read_metadata(
    path: str,
) -> RasterInfo:
    """
    Read raster metadata without loading pixel values.
    """

    with rasterio.open(path) as src:

        return RasterInfo(
            width=src.width,
            height=src.height,
            count=src.count,
            dtype=src.dtypes[0],
            crs=src.crs,
            transform=src.transform,
            nodata=src.nodata,
        )


def raster_statistics(
    image: np.ndarray,
) -> RasterStatistics:
    """
    Compute summary statistics.
    """

    return RasterStatistics(
        minimum=float(np.nanmin(image)),
        maximum=float(np.nanmax(image)),
        mean=float(np.nanmean(image)),
        std=float(np.nanstd(image)),
    )

def pixel_size(
    info: RasterInfo,
) -> tuple[float, float]:
    """
    Return pixel spacing.
    """

    return (
        abs(info.transform.a),
        abs(info.transform.e),
    )


def bounds(
    info: RasterInfo,
) -> BoundingBox:
    """
    Return raster bounds.
    """

    left, bottom, right, top = array_bounds(
        info.height,
        info.width,
        info.transform,
    )

    return BoundingBox(
        left=left,
        bottom=bottom,
        right=right,
        top=top,
    )


def validate_alignment(
    raster1: RasterInfo,
    raster2: RasterInfo,
) -> None:
    """
    Raise ValueError if rasters are not aligned.
    """

    if raster1.crs != raster2.crs:
        raise ValueError(
            "Rasters have different CRS."
        )

    if raster1.transform != raster2.transform:
        raise ValueError(
            "Rasters have different affine transforms."
        )

    if raster1.width != raster2.width:
        raise ValueError(
            "Rasters have different widths."
        )

    if raster1.height != raster2.height:
        raise ValueError(
            "Rasters have different heights."
        )

def same_extent(
    raster1: RasterInfo,
    raster2: RasterInfo,
) -> bool:
    """
    Return True if rasters are aligned.
    """

    try:

        validate_alignment(
            raster1,
            raster2,
        )

        return True

    except ValueError:

        return False


def crop_to_common_extent(
    image1: np.ndarray,
    raster1: RasterInfo,
    image2: np.ndarray,
    raster2: RasterInfo,
) -> tuple[
    np.ndarray,
    np.ndarray,
    RasterInfo,
]:
    """
    Crop two rasters to their common size.
    """

    height = min(
        raster1.height,
        raster2.height,
    )

    width = min(
        raster1.width,
        raster2.width,
    )

    cropped1 = image1[
        :height,
        :width,
    ]

    cropped2 = image2[
        :height,
        :width,
    ]

    info = replace(
        raster1,
        width=width,
        height=height,
    )

    return (
        cropped1,
        cropped2,
        info,
    )



