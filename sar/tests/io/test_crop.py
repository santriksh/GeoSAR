import numpy as np

from affine import Affine

from rasterio.crs import CRS

from sar.io.models import RasterInfo
from sar.io.raster import crop_to_common_extent

def make_info(
    width,
    height,
):

    return RasterInfo(
        width=width,
        height=height,
        count=1,
        dtype="float32",
        crs=CRS.from_epsg(32646),
        transform=Affine.identity(),
        nodata=None,
    )

def test_crop():

    image1 = np.ones(
        (
            10,
            12,
        )
    )

    image2 = np.ones(
        (
            8,
            15,
        )
    )

    info1 = make_info(
        12,
        10,
    )

    info2 = make_info(
        15,
        8,
    )

    crop1, crop2, info = crop_to_common_extent(
        image1,
        info1,
        image2,
        info2,
    )

    assert crop1.shape == (
        8,
        12,
    )

    assert crop2.shape == (
        8,
        12,
    )

    assert info.width == 12
    assert info.height == 8