import numpy as np

from sar.plotting import show_mask


def test_show_mask():

    mask = np.zeros(
        (10, 10),
        dtype=bool,
    )

    fig, ax = show_mask(
        mask,
    )

    assert fig is not None