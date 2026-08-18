from sar.io.raster import read_metadata
from pathlib import Path

TEST_DATA = (
    Path(__file__).resolve().parent.parent
    / "data"
)

def test_read_metadata():

    info = read_metadata(
        str(TEST_DATA / "sample_image_preflood1.tif"),
)

    assert info.width > 0
    assert info.height > 0

    assert info.count == 1

    assert info.crs.to_epsg() == 32646