import logging

logger = logging.getLogger(__name__)
from sar.filters.refined_lee_geosar import refined_lee
from sar.pipeline.models import (
    FloodResult,
    _compute_log_ratio,
    _compute_statistics,
    _postprocess,
    _threshold,
)
from sar.sar_geometry import align_to_reference
from sar.sar_image import SARImage
from sar.sar_radiometry import db_to_linear


def _validate_inputs(
    before: SARImage,
    after: SARImage,
) -> None:
    """
    Validate the two pipeline inputs.

    Raises
    ------
    ValueError
        If the images cannot be processed
        together.
    """

    if before.crs != after.crs:
        raise ValueError(
            "Images must have the same CRS."
        )

    if before.value_scale != after.value_scale:
        raise ValueError(
            "Images must have the same value scale."
        )

    if (
        before.metadata.spatial.resolution
        !=
        after.metadata.spatial.resolution
    ):
        raise ValueError(
            "Images must have the same resolution."
        )

def _requires_alignment(
    reference: SARImage,
    moving: SARImage,
) -> bool:
    """
    Determine whether two SAR images require alignment.

    Returns
    -------
    bool
        True if the moving image should be aligned
        to the reference image.
    """

    spatial_ref = reference.metadata.spatial
    spatial_mov = moving.metadata.spatial

    #
    # Shape
    #
    if spatial_ref.shape != spatial_mov.shape:
        return True

    #
    # Affine transform
    #
    if spatial_ref.transform != spatial_mov.transform:
        return True

    #
    # Bounds
    #
    return spatial_ref.bounds != spatial_mov.bounds
        




def _prepare_inputs(
    before: SARImage,
    after: SARImage,
    apply_refined_lee: bool = True,
) -> tuple[SARImage, SARImage]:
    """
    Prepare two SAR images for change detection.

    The returned images satisfy the following:

    - Same CRS
    - Same shape
    - Same transform
    - Same bounds
    - Linear value scale
    - Optionally speckle filtered

    Parameters
    ----------
    before
        Pre-event image.

    after
        Post-event image.

    apply_refined_lee
        Apply Refined Lee filtering.

    Returns
    -------
    tuple[SARImage, SARImage]
        Prepared images.
    """

    #
    # Align images if required
    #
    # print("\n========== PREPARE INPUTS ==========")
    # print("Before :", before.data.shape)
    # print("After  :", after.data.shape)
    if _requires_alignment(
        before,
        after,
    ):
        print("Needs alignment : True")
        after = align_to_reference(
            reference=before,
            moving=after,
        )
        print("After aligned :", after.data.shape)

    # print("Returning:")
    # print("Before :", before.data.shape)
    # print("After  :", after.data.shape)
    # print("====================================\n")

    #
    # Convert to Linear if necessary
    #
    if before.value_scale.lower() == "db":

        before = db_to_linear(before)

        after = db_to_linear(after)

    #
    # Optional speckle filtering
    #
    if apply_refined_lee:

        before = refined_lee(before)

        after = refined_lee(after)

    return before, after

def detect_flood(
    before: SARImage,
    after: SARImage,
    *,
    threshold: float = -2.5,
    apply_refined_lee: bool = True,
    min_object_size: int = 50,
    opening_iterations: int = 1,
    closing_iterations: int = 1,
    connectivity: int = 2,
) -> FloodResult:
    """
    Detect flooded areas between two SAR images.
    """

    #
    # Validate inputs
    #
    logger.info("Validating inputs...")
    _validate_inputs(
        before,
        after,
    )

    #
    # Prepare images
    #
    logger.info("Preparing inputs...")
    before, after = _prepare_inputs(
        before,
        after,
        apply_refined_lee=apply_refined_lee,
    )
    if before.data.shape != after.data.shape:
        raise RuntimeError(
            "Prepared images must have identical shapes."
        )

    #
    # Compute change image
    #
    logger.info("Computing log-ratio image...")
    log_ratio = _compute_log_ratio(
        before,
        after,
    )

    #
    # Threshold
    #
    logger.info(
    "Applying threshold (%.2f dB)...",
    threshold,
)
    flood_mask = _threshold(
        log_ratio,
        threshold=threshold,
    )

    #
    # Morphological cleanup
    #
    logger.info("Running morphological cleanup...")
    flood_mask = _postprocess(
        flood_mask=flood_mask,
        min_object_size=min_object_size,
        opening_iterations=opening_iterations,
        closing_iterations=closing_iterations,
        connectivity=connectivity,
    )

    #
    # Statistics
    #
    logger.info("Computing flood statistics...")
    statistics = _compute_statistics(
        flood_mask,
    )

    #
    # Return result
    #
    logger.info("Flood detection complete.")
    return FloodResult(
        before=before,
        after=after,
        flood_mask=flood_mask,
        log_ratio=log_ratio,
        threshold=threshold,
        statistics=statistics,
        refined_lee_applied=apply_refined_lee,
        min_object_size=min_object_size,
    )