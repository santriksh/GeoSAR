import numpy as np

import pytest

from affine import Affine

from rasterio.coords import BoundingBox

# from geosar.core.sar_image import SARImage

# from geosar.core.sar_metadata import (
#     SARMetadata,
#     SpatialMetadata,
#     AcquisitionMetadata,
#     ProcessingMetadata,
#     ProvenanceMetadata,
#     CustomMetadata,
# )

# @pytest.fixture
# def sample_metadata():

#     spatial = SpatialMetadata(

#         crs="EPSG:32646",

#         transform=Affine.identity(),

#         bounds=BoundingBox(
#             left=0,
#             bottom=0,
#             right=30,
#             top=30,
#         ),

#         resolution=(10.0, 10.0),

#         shape=(3,3),
#     )

#     acquisition = AcquisitionMetadata(

#         platform="Sentinel-1",

#         sensor="SAR",

#         acquisition_date="2022-05-01",

#         orbit_direction="DESCENDING",

#         relative_orbit=165,
#     )

#     return SARMetadata(

#         spatial=spatial,

#         acquisition=acquisition,

#         processing=ProcessingMetadata(),

#         provenance=ProvenanceMetadata(),

#         custom=CustomMetadata(),
#     )


# @pytest.fixture
# def sample_image(sample_metadata):

#     data = np.array([

#         [1.0,2.0,3.0],

#         [4.0,np.nan,6.0],

#         [7.0,8.0,9.0]

#     ])

#     mask = np.isfinite(data)

#     return SARImage(

#         data=data,

#         mask=mask,

#         metadata=sample_metadata,
#     )


def test_statistics(sample_image):

    stats = sample_image.statistics()

    assert stats["minimum"] == 1.0

    assert stats["maximum"] == 9.0

    assert stats["mean"] == 5.0

    assert stats["median"] == 5.0

    assert stats["valid_pixels"] == 8

    assert stats["nodata_pixels"] == 1

    assert stats["nan_percentage"] == pytest.approx(100/9)

def test_properties(sample_image):

    assert sample_image.width == 3

    assert sample_image.height == 3

    assert sample_image.shape == (3,3)

    assert sample_image.pixel_size_x == 10

    assert sample_image.pixel_size_y == 10

    assert sample_image.crs == "EPSG:32646"

    assert sample_image.value_scale == "dB"

def test_valid_pixels(sample_image):

    valid = sample_image.valid_pixels

    assert len(valid) == 8

    assert np.isnan(valid).sum() == 0


def test_summary(sample_image):

    summary = sample_image.as_dict()

    assert "statistics" in summary

    assert "spatial" in summary

    assert "processing" in summary

    assert "acquisition" in summary

    assert summary["statistics"]["mean"] == 5.0
