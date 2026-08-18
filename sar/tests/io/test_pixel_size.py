from affine import Affine

from rasterio.crs import CRS

from sar.io.models import RasterInfo
from sar.io.raster import pixel_size


def test_pixel_size():

    info = RasterInfo(
        width=100,
        height=100,
        count=1,
        dtype="float32",
        crs=CRS.from_epsg(32646),
        transform=Affine(
            10,
            0,
            0,
            0,
            -10,
            0,
        ),
        nodata=None,
    )

    assert pixel_size(info) == (10, 10)