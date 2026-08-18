from dataclasses import dataclass

from affine import Affine
from rasterio.crs import CRS


@dataclass(frozen=True)
class RasterInfo:
    """
    Metadata describing a raster.
    """

    width: int
    height: int

    count: int
    dtype: str

    crs: CRS
    transform: Affine

    nodata: float | None


@dataclass(frozen=True)
class RasterStatistics:
    """
    Summary statistics for a raster.
    """

    minimum: float
    maximum: float
    mean: float
    std: float