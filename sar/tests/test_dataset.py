"""
Unit tests for DatasetInspector.
"""

import pytest
from affine import Affine
from dataclasses import replace
from sar.validation.dataset import DatasetInspector
from sar.validation.models import DatasetSummary
from dataclasses import replace

def test_dataset_validation_success(dataset_inspector):
    """
    DatasetInspector should successfully validate
    two identical images.
    """

    summary = dataset_inspector.run()

    assert isinstance(summary, DatasetSummary)


def test_shape_mismatch(identical_images):

    pre, post = identical_images

    post.data = post.data[:-1]
    post.mask = post.mask[:-1]

    with pytest.raises(
        ValueError,
        match="Image dimensions do not match",
    ):
        DatasetInspector(pre, post).run()

def test_crs_mismatch(identical_images):

    pre, post = identical_images

    spatial = replace(
        post.metadata.spatial,
        crs="EPSG:4326",
    )

    post.metadata = replace(
        post.metadata,
        spatial=spatial,
    )

    with pytest.raises(
        ValueError,
        match="CRS mismatch",
    ):
        DatasetInspector(pre, post).run()


def test_resolution_mismatch(identical_images):

    pre, post = identical_images

    #post.metadata.spatial.resolution = (20.0, 20.0)

    spatial = replace(
        post.metadata.spatial,
        resolution = (20.0, 20.0),
    )

    post.metadata = replace(
        post.metadata,
        spatial=spatial,
    )

    with pytest.raises(
        ValueError,
        match="Spatial resolution mismatch",
    ):
        DatasetInspector(pre, post).run()


def test_transform_mismatch(identical_images):

    pre, post = identical_images

    # post.metadata.spatial.transform = Affine.translation(
    #     100,
    #     100,
    # )

    spatial = replace(
        post.metadata.spatial,
        transform = Affine.translation(100,100,),)

    post.metadata = replace(
        post.metadata,
        spatial=spatial,
    )

    with pytest.raises(
        ValueError,
        match="Affine transform mismatch",
    ):
        DatasetInspector(pre, post).run()


def test_dataset_summary_contents(dataset_inspector):

    summary = dataset_inspector.run()

    assert summary.width == 3
    assert summary.height == 3

    assert summary.pre_shape == (3, 3)
    assert summary.post_shape == (3, 3)

    assert summary.crs == "EPSG:32646"

    assert summary.pixel_size_x == 10.0
    assert summary.pixel_size_y == 10.0

    assert summary.mean_pre == 5.0
    assert summary.mean_post == 5.0

    assert summary.nan_percentage_pre == pytest.approx(
        100 / 9
    )

    assert summary.nan_percentage_post == pytest.approx(
        100 / 9
    )

    assert summary.satellite == "Sentinel-1"

    assert summary.orbit_direction == "DESCENDING"

    assert summary.relative_orbit == 165


def test_acquisition_dates(dataset_inspector):

    summary = dataset_inspector.run()

    assert summary.acquisition_pre == "2022-05-01"

    assert summary.acquisition_post == "2022-05-01"