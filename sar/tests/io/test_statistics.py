import numpy as np

from sar.io.raster import raster_statistics


def test_statistics():

    image = np.array(
        [
            [1, 2],
            [3, 4],
        ],
        dtype=float,
    )

    stats = raster_statistics(image)

    assert stats.minimum == 1.0
    assert stats.maximum == 4.0
    assert stats.mean == 2.5
    assert stats.std == np.std(image)

    