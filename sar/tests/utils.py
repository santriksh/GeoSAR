# tests/utils.py

from copy import deepcopy
from sar.sar_image import SARImage

def clone_image(image: SARImage) -> SARImage:
    """Return a deep copy of a SARImage."""
    return deepcopy(image)


from dataclasses import replace

import numpy as np

#from sar.models import BoundingBox
from rasterio.coords import BoundingBox

def make_test_image(
    template,
    data=None,
    mask=None,
    value_scale=None,
    shape=None,
    bounds=None,
):
    """
    Create a new SARImage for tests from an existing image.

    Only the supplied attributes are modified.
    """

    image = deepcopy(template)

    # -----------------------------
    # Data
    # -----------------------------
    if data is not None:
        image.data = data

    # -----------------------------
    # Mask
    # -----------------------------
    if mask is None:
        #mask = np.ones_like(image.data, dtype=bool)
        mask = np.isfinite(image.data)

    image.mask = mask

    # -----------------------------
    # Shape
    # -----------------------------
    if shape is None:
        shape = image.data.shape

    # -----------------------------
    # Bounds
    # -----------------------------
    if bounds is None:
        bounds = BoundingBox(
            left=0,
            bottom=0,
            right=shape[1],
            top=shape[0],
        )

    # -----------------------------
    # Value Scale
    # -----------------------------
    if value_scale is None:
        value_scale = image.value_scale

    image.metadata = replace(
        image.metadata,
        spatial=replace(
            image.metadata.spatial,
            shape=shape,
            bounds=bounds,
        ),
        processing=replace(
            image.metadata.processing,
            value_scale=value_scale,
        ),
    )

    return image


# def make_test_image(
#     template,
#     data,
#     mask=None,
#     value_scale="Linear",
# ):
#     """
#     Create a new SARImage for tests using an existing image as a template.
#     """

#     image = clone_image(template)

#     if mask is None:
#         mask = np.ones_like(data, dtype=bool)

#     image.data = data
#     image.mask = mask

#     image.metadata = replace(
#         image.metadata,
#         spatial=replace(
#             image.metadata.spatial,
#             shape=data.shape,
#             bounds=BoundingBox(
#                 left=0,
#                 bottom=0,
#                 right=data.shape[1],
#                 top=data.shape[0],
#             ),
#         ),
#         processing=replace(
#             image.metadata.processing,
#             value_scale=value_scale,
#         ),
#     )

#     return image
