import numpy as np

from sar.sar_image import SARImage

from .stretch import percentile_stretch


def _draw_image(
    ax,
    image,
    *,
    title,
    stretch=True,
    convert_linear_to_db=True,
):

    data = image.data.astype(
        np.float32,
    ).copy()

    data[~image.mask] = np.nan

    if (
        convert_linear_to_db
        and
        image.value_scale.lower() == "linear"
    ):

        data = (
            10
            *
            np.log10(
                np.maximum(
                    data,
                    1e-12,
                )
            )
        )

    if stretch:

        data = percentile_stretch(
            data,
        )

    ax.imshow(
        data,
        cmap="gray",
        interpolation="nearest",
    )

    ax.set_title(title)

    ax.set_axis_off()


def _draw_overlay(
    ax,
    image: SARImage,
    mask: SARImage,
    *,
    title: str,
    alpha: float = 0.5,
    color: str = "red",
    stretch: bool = True,
):
    """
    Draw a SAR image with a semi-transparent binary overlay.

    Parameters
    ----------
    ax
        Matplotlib Axes.

    image
        Background SAR image.

    mask
        Binary mask.

    title
        Figure title.

    alpha
        Overlay transparency.

    color
        Overlay colour ("red", "green", "blue").

    stretch
        Apply percentile stretching to the background image.
    """

    #
    # Validate shapes
    #
    if image.data.shape != mask.data.shape:
        raise ValueError(
            "Image and mask must have identical shape."
        )

    #
    # Validate binary mask
    #
    values = np.unique(
        mask.data[mask.mask]
    )

    if not np.all(
        np.isin(values, [0, 1])
    ):
        raise ValueError(
            "Mask must contain only 0 and 1."
        )

    #
    # Draw background image
    #
    _draw_image(
        ax,
        image,
        title=title,
        stretch=stretch,
    )

    #
    # Build RGBA overlay
    #
    rgba = np.zeros(
        (*mask.data.shape, 4),
        dtype=np.float32,
    )

    #
    # Colour channels
    #
    if color == "red":

        rgba[..., 0] = 1.0

    elif color == "green":

        rgba[..., 1] = 1.0

    elif color == "blue":

        rgba[..., 2] = 1.0

    else:

        raise ValueError(
            "Unsupported colour."
        )

    #
    # Alpha channel
    #
    rgba[..., 3] = (
        mask.data.astype(np.float32)
        * alpha
    )

    #
    # Respect invalid pixels
    #
    rgba[~mask.mask, 3] = 0.0

    #
    # Draw overlay
    #
    ax.imshow(
        rgba,
        interpolation="nearest",
    )
    