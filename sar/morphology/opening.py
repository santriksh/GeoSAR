from __future__ import annotations

import numpy as np
from scipy.ndimage import binary_opening as scipy_binary_opening

from sar.sar_image import SARImage
from sar.utils import _create_result

from .structure import binary_structure
from .validation import validate_binary_image


def binary_opening(
    image: SARImage,
    iterations: int = 1,
    connectivity: int = 2,
) -> SARImage:
    """
    Perform binary opening on a binary image.

    Parameters
    ----------
    image : SARImage
        Binary input image.

    iterations : int
        Number of opening iterations.

    connectivity : int
        Connectivity of the structuring element.

        1 -> 4-connected
        2 -> 8-connected

    Returns
    -------
    SARImage
        Opened binary image.
    """

    validate_binary_image(image)

    # ---------------------------------------------------
    # Validate iterations
    # ---------------------------------------------------
    if iterations < 1:
        raise ValueError(
            "iterations must be >= 1."
        )

    # ---------------------------------------------------
    # Validate connectivity
    # ---------------------------------------------------
    if connectivity not in (1, 2):
        raise ValueError(
            "connectivity must be either 1 (4-connected) "
            "or 2 (8-connected)."
        )


    structure = binary_structure(
    #rank=2,
    connectivity=connectivity,
)

        # ---------------------------------------------------
    # Binary Opening
    # ---------------------------------------------------
    data = scipy_binary_opening(
        image.data.astype(bool),
        structure=structure,
        iterations=iterations,
    )

    # ---------------------------------------------------
    # Preserve only valid pixels
    # ---------------------------------------------------
    data = data.astype(np.uint8)

    data[~image.mask] = 0

    # ---------------------------------------------------
    # Return SARImage
    # ---------------------------------------------------
    return _create_result(
        reference=image,
        data=data,
        mask=image.mask.copy(),
        operation="binary_opening",
        value_scale=image.value_scale,
    )