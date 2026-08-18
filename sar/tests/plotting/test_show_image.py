import numpy as np

from sar.plotting import show_image


def test_show_image():

    image = np.random.random(
        (10, 10),
    )

    fig, ax = show_image(
        image,
    )

    assert fig is not None
    assert ax is not None