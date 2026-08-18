from __future__ import annotations

import numpy as np
from scipy.ndimage import (
    label as scipy_label,
)

from sar.sar_image import SARImage

from .structure import binary_structure
from .validation import validate_binary_image


def label_connected_components(
    image: SARImage,
    connectivity: int = 2,
) -> tuple[np.ndarray, int]:
    """
    Label connected components in a binary image.

    Parameters
    ----------
    image
        Binary SAR image.

    connectivity

        1 -> 4-connected

        2 -> 8-connected

    Returns
    -------
    labels

        Integer label image.

    num_labels

        Number of connected components.
    """

    validate_binary_image(image)

    structure = binary_structure(
        connectivity,
    )
    
    labels, num_labels = scipy_label(
        image.data.astype(bool),
        structure=structure,
    )
    
    return labels, num_labels