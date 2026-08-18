"""
Image stretching utilities.

These functions improve image visualization without
changing the underlying SAR values.
"""

from __future__ import annotations

import numpy as np

EPS = 1e-12

def percentile_stretch(
    image: np.ndarray,
    lower: float = 2.0,
    upper: float = 98.0,
) -> np.ndarray:
    """
    Stretch an image using percentile clipping.

    Parameters
    ----------
    image
        Input image.

    lower
        Lower percentile.

    upper
        Upper percentile.

    Returns
    -------
    ndarray
        Image normalized to [0,1].
    """

    if lower >= upper:
        raise ValueError(
            "lower must be smaller than upper."
        )

    valid = image[np.isfinite(image)]

    if valid.size == 0:
        raise ValueError(
            "Image contains no finite pixels."
        )

    vmin = np.percentile(
        valid,
        lower,
    )

    vmax = np.percentile(
        valid,
        upper,
    )

    stretched = np.clip(
        image,
        vmin,
        vmax,
    )

    return (
        stretched - vmin
    ) / max(
        vmax - vmin,
        EPS,
    )


