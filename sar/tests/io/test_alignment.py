import pytest

from affine import Affine

from rasterio.crs import CRS

from sar.io.models import RasterInfo
from sar.io.raster import (
    same_extent,
    validate_alignment,
)


def make_info():

    return RasterInfo(
        width=100,
        height=200,
        count=1,
        dtype="float32",
        crs=CRS.from_epsg(32646),
        transform=Affine.identity(),
        nodata=None,
    )


def test_validate_alignment():

    info = make_info()

    validate_alignment(
        info,
        info,
    )

def test_different_width():

    info1 = make_info()

    info2 = RasterInfo(
        **{
            **info1.__dict__,
            "width": 50,
        }
    )

    with pytest.raises(ValueError):

        validate_alignment(
            info1,
            info2,
        )


def test_same_extent():

    info = make_info()

    assert same_extent(
        info,
        info,
    )

def test_not_same_extent():

    info1 = make_info()

    info2 = RasterInfo(
        **{
            **info1.__dict__,
            "height": 50,
        }
    )

    assert not same_extent(
        info1,
        info2,
    )