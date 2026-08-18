"""
Validation utilities for binary morphology operations.
"""

from __future__ import annotations

import numpy as np

from sar.sar_image import SARImage


def validate_binary_image(
    image: SARImage,
) -> None:
    """
    Validate that a SARImage contains binary values.

    Parameters
    ----------
    image
        Binary SAR image.

    Raises
    ------
    ValueError
        If the mask shape differs from the data shape or
        the valid pixels contain values other than 0 or 1.
    """

    if image.mask.shape != image.data.shape:
        raise ValueError(
            "Mask shape must match data shape."
        )

    valid = image.data[
        image.mask
    ]

    valid = valid[
        np.isfinite(valid)
    ]

    if not np.all(
        (valid == 0)
        |
        (valid == 1)
    ):
        raise ValueError(
            "Image must contain only binary values (0 or 1)."
        )