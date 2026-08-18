import numpy as np

from sar.plotting import compare_images


def test_compare_images():

    image = np.ones(
        (10, 10),
    )

    fig, axes = compare_images(
        image,
        image,
    )

    assert len(axes) == 2