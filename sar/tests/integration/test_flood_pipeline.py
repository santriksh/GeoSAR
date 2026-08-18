from sar.pipeline.flood import detect_flood
from sar.pipeline.models import FloodResult,FloodStatistics
import numpy as np

def test_pipeline_runs(
    sample_linear_image,
):
    """
    Pipeline should execute successfully and
    return a FloodResult.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    assert isinstance(
        result,
        FloodResult,
    )

    assert result.log_ratio is not None
    assert result.flood_mask is not None
    assert result.statistics is not None


def test_output_shapes(
    sample_linear_image,
):
    """
    Pipeline preserves image dimensions.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    assert (
        result.log_ratio.shape
        ==
        sample_linear_image.shape
    )

    assert (
        result.flood_mask.shape
        ==
        sample_linear_image.shape
    )


def test_flood_mask_is_binary(
    sample_linear_image,
):
    """
    Flood mask should contain only
    0 and 1.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    values = np.unique(
        result.flood_mask.data[
            result.flood_mask.mask
        ]
    )

    assert set(values).issubset(
        {0,1}
    )


def test_statistics_match_mask(
    sample_linear_image,
):
    """
    Flood statistics should agree with
    the flood mask.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    flooded = np.count_nonzero(
        result.flood_mask.data
    )

    assert (
        flooded
        ==
        result.statistics.flooded_pixels
    )


def test_area_is_correct(
    sample_linear_image,
):
    """
    Flood area should equal

    flooded_pixels × pixel_area.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    expected = (
        result.statistics.flooded_pixels
        *
        100
    )

    assert (
        result.statistics.flooded_area_m2
        ==
        expected
    )

def test_threshold_saved(
    sample_linear_image,
):
    """
    Threshold should be stored in
    FloodResult.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        threshold=-3.5,
        apply_refined_lee=False,
    )

    assert (
        result.threshold
        ==
        -3.5
    )


def test_metadata_preserved(
    sample_linear_image,
):
    """
    Output images preserve CRS.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    assert (
        result.log_ratio.crs
        ==
        sample_linear_image.crs
    )

    assert (
        result.flood_mask.crs
        ==
        sample_linear_image.crs
    )



def test_log_ratio_is_db(
    sample_linear_image,
):
    """
    Log-ratio image should be
    in dB.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    assert (
        result.log_ratio.value_scale.lower()
        ==
        "db"
    )


def test_identical_images_produce_no_flood(
    sample_linear_image,
):
    """
    Identical images should not
    produce flooded pixels.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=False,
    )

    assert (
        result.statistics.flooded_pixels
        ==
        0
    )




def test_pipeline_with_refined_lee(
    sample_linear_image,
):
    """
    Pipeline should also execute
    successfully with Refined Lee.
    """

    result = detect_flood(
        before=sample_linear_image,
        after=sample_linear_image,
        apply_refined_lee=True,
    )

    assert isinstance(
        result,
        FloodResult,
    )