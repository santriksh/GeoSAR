from sar.io.raster import read_metadata


def test_read_metadata():

    info = read_metadata(
        "tests/data/sample_image_preflood1.tif",
    )

    assert info.width > 0
    assert info.height > 0

    assert info.count == 1

    assert info.crs.to_epsg() == 32646