from sar.io.raster import read_raster


def test_read_raster():

    image, info = read_raster(
        "tests/data/sample_image_preflood1.tif",
    )

    assert image.shape == (
        info.height,
        info.width,
    )

    assert image.dtype.name == info.dtype