import matplotlib.pyplot as plt

from sar.sar_image import SARImage

from ._helpers import (
    _draw_image,
    _draw_overlay,
)


def compare(
    before: SARImage,
    after: SARImage,
    log_ratio: SARImage,
    flood_mask: SARImage,
    *,
    figsize=(12, 12),
    stretch: bool = True,
):
    """
    Display a 2×2 comparison figure showing

    - Before image
    - After image
    - Log-ratio image
    - Flood overlay
    """

    fig, axes = plt.subplots(
        2,
        2,
        figsize=figsize,
    )

    #
    # Before
    #
    _draw_image(
        axes[0, 0],
        before,
        title="Before",
        stretch=stretch,
    )

    #
    # After
    #
    _draw_image(
        axes[0, 1],
        after,
        title="After",
        stretch=stretch,
    )

    #
    # Log Ratio
    #
    _draw_image(
        axes[1, 0],
        log_ratio,
        title="Log Ratio (dB)",
        stretch=stretch,
        convert_linear_to_db=False,
    )

    #
    # Flood Overlay
    #
    _draw_overlay(
        axes[1, 1],
        after,
        flood_mask,
        title="Flood Detection Overlay",
        stretch=stretch,
    )

    fig.suptitle(
        "GeoSAR Flood Detection Summary",
        fontsize=16,
        fontweight="bold",
    )

    plt.tight_layout()

    plt.show()