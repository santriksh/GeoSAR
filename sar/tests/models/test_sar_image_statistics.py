"""
Regression tests for SARImage.statistics().
"""

import numpy as np

from sar.sar_image import SARImage
from sar.sar_metadata import (
    SARMetadata,
    SpatialMetadata,
    AcquisitionMetadata,
    ProcessingMetadata,
    ProvenanceMetadata,
    CustomMetadata,
)


def dummy_metadata():
    """Create minimal metadata required for SARImage."""

    return SARMetadata(
        spatial=SpatialMetadata(
            crs=None,
            transform=None,
            bounds=None,
            resolution=(1, 1),
            shape=(0, 0),
        ),
        acquisition=AcquisitionMetadata(),
        processing=ProcessingMetadata(),
        provenance=ProvenanceMetadata(),
        custom=CustomMetadata(),
    )


def test_statistics_normal_image():
    """Statistics for a normal image."""

    data = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
    )

    mask = np.ones_like(data, dtype=bool)

    image = SARImage(data, mask, dummy_metadata())

    stats = image.statistics()

    assert stats["minimum"] == 1.0
    assert stats["maximum"] == 4.0
    assert stats["mean"] == 2.5
    assert stats["median"] == 2.5
    assert np.isclose(stats["std"], np.std(data))
    assert stats["valid_pixels"] == 4
    assert stats["nodata_pixels"] == 0
    assert stats["nan_percentage"] == 0.0


def test_statistics_ignore_masked_pixels():
    """Statistics should ignore masked pixels."""

    data = np.array(
        [
            [1.0, np.nan],
            [3.0, 4.0],
        ]
    )

    mask = np.array(
        [
            [True, False],
            [True, True],
        ]
    )

    image = SARImage(data, mask, dummy_metadata())

    stats = image.statistics()

    assert stats["minimum"] == 1.0
    assert stats["maximum"] == 4.0
    assert np.isclose(stats["mean"], (1 + 3 + 4) / 3)
    assert stats["valid_pixels"] == 3
    assert stats["nodata_pixels"] == 1
    assert stats["nan_percentage"] == 25.0


def test_statistics_fully_masked_image():
    """Fully masked image should return None statistics."""

    data = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
    )

    mask = np.zeros_like(data, dtype=bool)

    image = SARImage(data, mask, dummy_metadata())

    stats = image.statistics()

    assert stats["minimum"] is None
    assert stats["maximum"] is None
    assert stats["mean"] is None
    assert stats["median"] is None
    assert stats["std"] is None

    assert stats["valid_pixels"] == 0
    assert stats["nodata_pixels"] == 4
    assert stats["nan_percentage"] == 100.0


def test_statistics_single_valid_pixel():
    """Statistics for one valid pixel."""

    data = np.array(
        [
            [10.0, 20.0],
            [30.0, 40.0],
        ]
    )

    mask = np.array(
        [
            [False, False],
            [False, True],
        ]
    )

    image = SARImage(data, mask, dummy_metadata())

    stats = image.statistics()

    assert stats["minimum"] == 40.0
    assert stats["maximum"] == 40.0
    assert stats["mean"] == 40.0
    assert stats["median"] == 40.0
    assert stats["std"] == 0.0

    assert stats["valid_pixels"] == 1
    assert stats["nodata_pixels"] == 3
    assert stats["nan_percentage"] == 75.0


def test_statistics_pixel_accounting():
    """Valid pixels + NoData pixels must equal total pixels."""

    rng = np.random.default_rng(42)

    data = rng.random((10, 10))

    mask = rng.random((10, 10)) > 0.3

    image = SARImage(data, mask, dummy_metadata())

    stats = image.statistics()

    assert (
        stats["valid_pixels"] +
        stats["nodata_pixels"]
    ) == data.size