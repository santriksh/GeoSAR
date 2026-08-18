"""
Shared pytest fixtures for sar tests.
"""

import numpy as np
import pytest
from datetime import date
from affine import Affine
from rasterio.coords import BoundingBox
import copy
from sar.validation.dataset import DatasetInspector
from sar.sar_image import SARImage
from sar.sar_metadata import (
    SARMetadata,
    SpatialMetadata,
    AcquisitionMetadata,
    ProcessingMetadata,
    ProvenanceMetadata,
    CustomMetadata,
)
from copy import deepcopy
from sar.tests.utils import clone_image
from dataclasses import replace
from sar.tests.utils import make_test_image

@pytest.fixture
def sample_metadata():

    spatial = SpatialMetadata(
        crs="EPSG:32646",
        transform=Affine.identity(),
        bounds=BoundingBox(
            left=0,
            bottom=0,
            right=30,
            top=30,
        ),
        resolution=(10.0, 10.0),
        shape=(3, 3),
    )

    acquisition = AcquisitionMetadata(
        platform="Sentinel-1",
        sensor="SAR",
        acquisition_date="2022-05-01",
        orbit_direction="DESCENDING",
        relative_orbit=165,
    )

    processing = ProcessingMetadata(
        processing_level="GRD",
        product_type="GeoTIFF",
        value_scale="dB",
    )

    provenance = ProvenanceMetadata(
        operation="unit_test",
        inputs=["dummy.tif"],
    )

    return SARMetadata(
        spatial=spatial,
        acquisition=acquisition,
        processing=processing,
        provenance=provenance,
        custom=CustomMetadata(),
    )


# ==========================================================
# Single Image Fixture
# ==========================================================

@pytest.fixture
def sample_image(sample_metadata):

    data = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, np.nan, 6.0],
            [7.0, 8.0, 9.0],
        ],
        dtype=np.float32,
    )

    mask = np.isfinite(data)

    return SARImage(
        data=data,
        mask=mask,
        metadata=sample_metadata,
    )


# ==========================================================
# Pre/Post Image Pair
# ==========================================================

@pytest.fixture
def pre_post_images(sample_metadata):

    pre = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, np.nan, 6.0],
            [7.0, 8.0, 9.0],
        ],
        dtype=np.float32,
    )

    post = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, np.nan, 5.0],   # changed
            [6.0, 8.0, 9.0],      # changed
        ],
        dtype=np.float32,
    )

    pre_image = SARImage(
        data=pre,
        mask=np.isfinite(pre),
        metadata=copy.deepcopy(sample_metadata),
    )

    post_image = SARImage(
        data=post,
        mask=np.isfinite(post),
        metadata=copy.deepcopy(sample_metadata),
    )

    return pre_image, post_image

@pytest.fixture
def sentinel1_metadata():
    """
    Metadata representative of a real Sentinel-1 GRD scene.

    This fixture is intended for integration-style tests and
    mirrors a typical Sentinel-1 acquisition.
    """

    spatial = SpatialMetadata(

        crs="EPSG:32646",

        transform=Affine(
            10.0,
            0.0,
            148111.7409010494,
            0.0,
            -10.0,
            3046706.081705877,
        ),

        bounds=BoundingBox(
            left=148111.7409010494,
            bottom=2820406.081705877,
            right=381071.7409010494,
            top=3046706.081705877,
        ),

        resolution=(10.0, 10.0),

        shape=(22630, 23296),
    )

    acquisition = AcquisitionMetadata(

        platform="Sentinel-1A",

        sensor="C-band SAR",

        acquisition_date=date(2018, 7, 28),

        polarization="VV",

        orbit_direction="DESCENDING",

        relative_orbit=165,

        beam_mode="IW",

        frequency_band="C",
    )

    processing = ProcessingMetadata(

        processing_level="GRD",

        product_type="Ground Range Detected",

        value_scale="dB",

        software="ESA SNAP",

        calibration=True,

        terrain_corrected=True,

        speckle_filtered=False,
    )

    provenance = ProvenanceMetadata(

        operation="integration_test",

        inputs=["Sentinel-1_GRD.tif"],

        parameters={},

        created_by="sar Tests",

        version="1.0",
    )

    return SARMetadata(

        spatial=spatial,

        acquisition=acquisition,

        processing=processing,

        provenance=provenance,

        custom=CustomMetadata(),
    )


@pytest.fixture
def identical_images(sample_metadata):
    """
    Return two identical SAR images.

    Used for validation tests where only metadata consistency
    is being verified.
    """

    data = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, np.nan, 6.0],
            [7.0, 8.0, 9.0],
        ],
        dtype=np.float32,
    )

    mask = np.isfinite(data)

    image1 = SARImage(
        data=data.copy(),
        mask=mask.copy(),
        metadata=copy.deepcopy(sample_metadata),
    )

    image2 = SARImage(
        data=data.copy(),
        mask=mask.copy(),
        metadata=copy.deepcopy(sample_metadata),
    )

    return image1, image2


@pytest.fixture
def dataset_inspector(identical_images):

    pre, post = identical_images

    return DatasetInspector(pre, post)


@pytest.fixture
def noisy_image(sample_image):

    image = deepcopy(sample_image)

    rng = np.random.default_rng(42)

    # image.data = rng.normal(
    #     loc=10,
    #     scale=3,
    #     size=image.data.shape,
    # ).astype(np.float32)
    image.data = rng.lognormal(
    mean=2.0,
    sigma=0.35,
    size=(100,100),
).astype(np.float32)

    return image


@pytest.fixture
def small_linear_image(sample_image):

    image = clone_image(sample_image)

    image.metadata = replace(
        image.metadata,
        processing=replace(
            image.metadata.processing,
            value_scale="Linear",
        ),
    )

    return image


@pytest.fixture
def noisy_linear_image(linear_image):

    rng = np.random.default_rng(123)

    # noisy_data = (
    #     linear_image.data
    #     + rng.normal(
    #         0,
    #         2.0,
    #         linear_image.data.shape,
    #     ).astype(np.float32)
    # )
    noisy_data = (
        linear_image.data
        * rng.gamma(
    shape=4,
    scale=0.25,
    size=linear_image.data.shape,
))

    return make_test_image(
        template=linear_image,
        data=noisy_data,
    )



@pytest.fixture
def linear_image(sample_image):

    rng = np.random.default_rng(42)

    data = rng.lognormal(
    mean=2.0,
    sigma=0.35,
    size=(100,100),
).astype(np.float32)

    return make_test_image(
        template=sample_image,
        data=data,
        value_scale="Linear",
    )


# @pytest.fixture
# def uniform_linear_image(linear_image):

#     image = clone_image(linear_image)

#     image.data.fill(10.0)

#     return image

@pytest.fixture
def uniform_linear_image(sample_image):

    data = np.full(
        (100, 100),
        10.0,
        dtype=np.float32,
    )

    return make_test_image(
        template=sample_image,
        data=data,
        value_scale="Linear"
    )

@pytest.fixture
def db_image(linear_image):

    data = 10.0 * np.log10(linear_image.data)

    return make_test_image(
        template=linear_image,
        data=data,
        value_scale="dB",
    )


@pytest.fixture
def sample_linear_image(sample_metadata):

    metadata = deepcopy(sample_metadata)

    metadata.processing.value_scale = "linear"

    rng = np.random.default_rng(42)

    data = rng.random(
        (21,21),
    ).astype(np.float32)

    mask = np.ones_like(
    data,
    dtype=bool,
)

    return SARImage(
        data=data,
        mask=mask,
        metadata=metadata,
    )