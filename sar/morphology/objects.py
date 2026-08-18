"""
Object filtering.
"""

from __future__ import annotations

import numpy as np

from sar.sar_image import SARImage
from sar.utils import _create_result

from .connected_components import (
    label_connected_components,
)
from .validation import validate_binary_image


def remove_small_objects(
    image: SARImage,
    min_size: int = 20,
    connectivity: int = 2,
) -> SARImage:

    validate_binary_image(
        image,
    )

    if min_size < 1:
        raise ValueError(
            "min_size must be >= 1."
        )

    labels, _ = label_connected_components(
        image,
        connectivity,
    )  

    sizes = np.bincount(
        labels.ravel(),
    )

    keep = (
        sizes >= min_size
    )

    keep[0] = False

    data = keep[
        labels
    ]

    data = data.astype(
        np.uint8,
    )

    data[~image.mask] = 0

    return _create_result(
        reference=image,
        data=data,
        mask=image.mask.copy(),
        operation="remove_small_objects",
        value_scale=image.value_scale,
    )