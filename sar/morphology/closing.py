"""
Binary closing.
"""

from __future__ import annotations

import numpy as np
from scipy.ndimage import (
    binary_closing as scipy_binary_closing,
)

from sar.sar_image import SARImage
from sar.utils import _create_result

from .structure import binary_structure
from .validation import validate_binary_image


def binary_closing(
    image: SARImage,
    iterations: int = 1,
    connectivity: int = 2,
) -> SARImage:
    """
    Perform binary closing.

    Parameters
    ----------
    image
        Binary SAR image.

    iterations
        Number of closing iterations.

    connectivity

        1 -> 4-connected

        2 -> 8-connected

    Returns
    -------
    SARImage
    """

    validate_binary_image(
        image,
    )

    if iterations < 1:
        raise ValueError(
            "iterations must be >= 1."
        )

    structure = binary_structure(
        connectivity,
    )

    data = scipy_binary_closing(
        image.data.astype(bool),
        structure=structure,
        iterations=iterations,
    )

    data = data.astype(
        np.uint8,
    )

    data[~image.mask] = 0

    return _create_result(
        reference=image,
        data=data,
        mask=image.mask.copy(),
        operation="binary_closing",
        value_scale=image.value_scale,
    )
