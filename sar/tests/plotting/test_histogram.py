import numpy as np

from sar.plotting import show_histogram


def test_show_histogram():

    image = np.random.random(
        (10, 10),
    )

    fig, ax = show_histogram(
        image,
    )

    assert fig is not None
    assert ax is not None