from affine import Affine

from rasterio.crs import CRS

from sar.io.models import RasterInfo
from sar.io.raster import bounds


def test_bounds():

    info = RasterInfo(
        width=2,
        height=2,
        count=1,
        dtype="float32",
        crs=CRS.from_epsg(32646),
        transform=Affine(
            10,
            0,
            100,
            0,
            -10,
            200,
        ),
        nodata=None,
    )

    actual = bounds(info)

    assert actual.left == 100
    assert actual.right == 120

    assert actual.top == 200
    assert actual.bottom == 180