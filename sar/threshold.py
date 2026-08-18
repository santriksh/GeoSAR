"""
Thresholding utilities for SAR change detection.
"""

from __future__ import annotations

import numpy as np

from .sar_image import SARImage
from .utils import _create_result


def threshold_less_than(
    image: SARImage,
    threshold: float,
) -> SARImage:
    """
    Pixels below threshold become True.
    """

    mask = (
        image.mask
        &
        (image.data < threshold)
    )

    data = mask.astype(
        np.uint8,
    )

    return _create_result(
        reference=image,
        data=data,
        mask=mask,
        operation="threshold_less_than",
    )


import matplotlib.pyplot as plt


def show_binary(
    image,
    title,
):
    plt.figure(figsize=(10, 8))

    plt.imshow(
        image.data,
        cmap="gray",
    )

    plt.title(title)

    plt.axis("off")

    plt.show()


