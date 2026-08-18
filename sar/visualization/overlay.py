import matplotlib.pyplot as plt
import numpy as np

from sar.sar_image import SARImage

from ._helpers import _draw_overlay


def display_overlay(
    image: SARImage,
    mask: SARImage,
    *,
    title: str = "Flood Overlay",
    figsize=(10, 10),
    alpha: float = 0.45,
):
    """
    Display a binary mask over a SAR image.
    """

    _, ax = plt.subplots(
        figsize=figsize,
    )

    #
    # Background
    #
    background = image.data.astype(np.float32).copy()

    background[~image.mask] = np.nan

    ax.imshow(
        background,
        cmap="gray",
    )

    #
    # Flood mask
    #
    overlay = np.where(
        mask.data == 1,
        1.0,
        np.nan,
    )

    ax.imshow(
        overlay,
        cmap="Reds",
        alpha=alpha,
    )

    ax.set_title(title)

    ax.axis("off")

    plt.show()



from sar.sar_image import SARImage


def overlay(
    image: SARImage,
    mask: SARImage,
    *,
    title: str = "Flood Detection Overlay",
    alpha: float = 0.5,
    color: str = "red",
    figsize=(8, 8),
    stretch: bool = True,
):
    """
    Display a SAR image with a binary overlay.
    """

    _, ax = plt.subplots(
        figsize=figsize,
    )

    _draw_overlay(
        ax,
        image,
        mask,
        title=title,
        alpha=alpha,
        color=color,
        stretch=stretch,
    )

    plt.tight_layout()

    plt.show()