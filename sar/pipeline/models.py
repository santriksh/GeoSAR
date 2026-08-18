from dataclasses import dataclass

import numpy as np

from ..morphology.closing import binary_closing
from ..morphology.objects import remove_small_objects
from ..morphology.opening import binary_opening

# from sar.morphology.closing import binary_closing
# from sar.morphology.objects import remove_small_objects
# from sar.morphology.opening import binary_opening
# from sar.sar_change import log_ratio_change
# from sar.sar_image import SARImage
# from sar.utils import _create_result
from ..sar_change import log_ratio_change
from ..sar_image import SARImage
from ..utils import _create_result


@dataclass(frozen=True)
class FloodStatistics:
    """
    Summary statistics for a flood map.
    """

    flooded_pixels: int

    flooded_area_m2: float

    flooded_area_hectares: float

    flooded_percentage: float

    flooded_area_km2: float      



@dataclass(frozen=True)
class FloodResult:
    """
    Result returned by detect_flood().
    """
    before: SARImage

    after: SARImage

    flood_mask: SARImage

    log_ratio: SARImage

    statistics: FloodStatistics

    threshold: float

    refined_lee_applied: bool    

    min_object_size: int          



def _compute_log_ratio(
    before: SARImage,
    after: SARImage,
) -> SARImage:
    """
    Compute the logarithmic change image.

    Parameters
    ----------
    before
        Prepared pre-event image.

    after
        Prepared post-event image.

    Returns
    -------
    SARImage
        Log-ratio image in dB.
    """

    return log_ratio_change(
        before=before,
        after=after,
    )



def _threshold(
    image: SARImage,
    threshold: float,
    mode: str = "less_equal",
) -> SARImage:
    """
    Threshold a log-ratio image to create
    a binary flood mask.

    Parameters
    ----------
    image
        Log-ratio image.

    threshold
        Flood threshold in dB.

    Returns
    -------
    SARImage
        Binary flood mask.
    """

    data = (
        image.data <= threshold
    ).astype(np.uint8)

    #
    # Preserve NoData
    #
    data[~image.mask] = 0

    return _create_result(
        reference=image,
        data=data,
        mask=image.mask.copy(),
        operation="threshold",
        value_scale=image.value_scale,
    )



def _postprocess(
    flood_mask: SARImage,
    min_object_size: int,
    opening_iterations: int,
    closing_iterations: int,
    connectivity: int,
) -> SARImage:
    """
    Clean a binary flood mask using
    morphological operations.
    """

    result = remove_small_objects(
        flood_mask,
        min_size=min_object_size,
        connectivity=connectivity,
    )

    result = binary_opening(
        result,
        iterations=opening_iterations,
        connectivity=connectivity,
    )

    result = binary_closing(
        result,
        iterations=closing_iterations,
        connectivity=connectivity,
    )

    return result

def _compute_statistics(
    flood_mask: SARImage,
) -> FloodStatistics:
    """
    Compute summary statistics for a
    flood mask.
    """

    flooded_pixels = int(
        flood_mask.data[
            flood_mask.mask
        ].sum()
    )

    pixel_area = (
        flood_mask.metadata.spatial.resolution[0]
        *
        flood_mask.metadata.spatial.resolution[1]
    )

    flooded_area = (
        flooded_pixels
        *
        pixel_area
    )

    valid_pixels = int(
        flood_mask.mask.sum()
    )

    flooded_percentage = (
    100.0 * flooded_pixels / valid_pixels
    if valid_pixels > 0
    else 0.0
)

    return FloodStatistics(
        flooded_pixels=flooded_pixels,
        flooded_area_m2=flooded_area,
        flooded_area_km2=flooded_area / 1000000,
        flooded_area_hectares=flooded_area / 10000,
        flooded_percentage=flooded_percentage,
    )

