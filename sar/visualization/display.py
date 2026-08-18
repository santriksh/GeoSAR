"""
Display utilities.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from sar.sar_image import SARImage

from ._helpers import _draw_image


def display(
    image: SARImage,
    *,
    title: str = "",
    figsize=(8, 8),
    stretch: bool = True,
    convert_linear_to_db: bool = True,
):
    """
    Display a SAR image.
    """

    _, ax = plt.subplots(
        figsize=figsize,
    )

    _draw_image(
        ax,
        image,
        title=title,
        stretch=stretch,
        convert_linear_to_db=convert_linear_to_db,
    )

    plt.tight_layout()

    plt.show()