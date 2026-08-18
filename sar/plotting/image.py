import matplotlib.pyplot as plt
import numpy as np


def show_image(
    image: np.ndarray,
    *,
    title: str = "",
    cmap: str = "gray",
):
    """
    Display an image.

    Returns
    -------
    fig, ax
    """

    fig, ax = plt.subplots(
        figsize=(8, 8),
    )

    im = ax.imshow(
        image,
        cmap=cmap,
    )

    ax.set_title(title)

    fig.colorbar(
        im,
        ax=ax,
    )

    return fig, ax


def show_histogram(
    image: np.ndarray,
    *,
    bins: int = 100,
):
    """
    Display an image histogram.
    """

    fig, ax = plt.subplots(
        figsize=(8, 5),
    )

    ax.hist(
        image.ravel(),
        bins=bins,
    )

    ax.set_xlabel("Pixel value")
    ax.set_ylabel("Frequency")

    return fig, ax


def compare_images(
    image1: np.ndarray,
    image2: np.ndarray,
    *,
    title1: str = "Image 1",
    title2: str = "Image 2",
    cmap: str = "gray",
):
    """
    Compare two images side by side.
    """

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(12, 6),
    )

    axes[0].imshow(
        image1,
        cmap=cmap,
    )

    axes[0].set_title(title1)

    axes[1].imshow(
        image2,
        cmap=cmap,
    )

    axes[1].set_title(title2)

    return fig, axes


def show_difference(
    image1: np.ndarray,
    image2: np.ndarray,
):
    """
    Display image2-image1.
    """

    difference = image2 - image1

    fig, ax = plt.subplots(
        figsize=(8, 8),
    )

    im = ax.imshow(
        difference,
        cmap="RdBu",
    )

    fig.colorbar(
        im,
        ax=ax,
    )

    ax.set_title("Difference")

    return fig, ax


def show_mask(
    mask: np.ndarray,
):
    """
    Display a binary mask.
    """

    fig, ax = plt.subplots(
        figsize=(8, 8),
    )

    ax.imshow(
        mask,
        cmap="gray",
    )

    ax.set_title("Mask")

    return fig, ax