from sar.io.raster import read_raster
from pathlib import Path

TEST_DATA = (
    Path(__file__).resolve().parent.parent
    / "data"
)

def test_read_raster():

    image, info = read_raster(
        str(TEST_DATA / "sample_image_preflood1.tif"),
)

    assert image.shape == (
        info.height,
        info.width,
    )

    assert image.dtype.name == info.dtype