import numpy as np

from sar.plotting import show_difference


def test_show_difference():

    image = np.ones(
        (10, 10),
    )

    fig, ax = show_difference(
        image,
        image,
    )

    assert fig is not None