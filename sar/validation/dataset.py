"""
Dataset validation module.

Provides validation utilities for ensuring two SAR images are
compatible for comparison and generates a summary describing
the dataset.
"""

from __future__ import annotations

from sar.sar_image import SARImage

from .models import DatasetSummary


class DatasetInspector:
    """
    Validate a pair of SAR images and generate a dataset summary.

    Parameters
    ----------
    pre_image : SARImage
        Reference (pre-event) SAR image.
    post_image : SARImage
        Comparison (post-event) SAR image.
    """

    def __init__(
        self,
        pre_image: SARImage,
        post_image: SARImage,
    ) -> None:

        self.pre = pre_image
        self.post = post_image

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def summarize(self) -> DatasetSummary:
        """
        Validate the input images and generate a DatasetSummary.

        Returns
        -------
        DatasetSummary
            Summary describing both SAR datasets.
        """

        self._validate()

        return self._build_summary()

    def run(self) -> DatasetSummary:
        """
        Alias for summarize().

        Returns
        -------
        DatasetSummary
        """

        return self.summarize()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate(self) -> None:
        """Run all validation checks."""

        self._validate_shape()
        self._validate_crs()
        self._validate_resolution()
        self._validate_transform()

    def _validate_shape(self) -> None:
        """Validate image dimensions."""

        if self.pre.shape != self.post.shape:
            raise ValueError("Image dimensions do not match.")

    def _validate_crs(self) -> None:
        """Validate coordinate reference systems."""

        if self.pre.crs != self.post.crs:
            raise ValueError("CRS mismatch.")

    def _validate_resolution(self) -> None:
        """Validate spatial resolution."""

        if self.pre.resolution != self.post.resolution:
            raise ValueError("Spatial resolution mismatch.")

    def _validate_transform(self) -> None:
        """Validate affine transforms."""

        if self.pre.transform != self.post.transform:
            raise ValueError("Affine transform mismatch.")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _build_summary(self) -> DatasetSummary:
        """
        Build a DatasetSummary from both SAR images.

        Returns
        -------
        DatasetSummary
        """

        pre_stats = self.pre.statistics()
        post_stats = self.post.statistics()

        pre_acq = self.pre.metadata.acquisition
        post_acq = self.post.metadata.acquisition

        return DatasetSummary(

            # ----------------------------------------------------------
            # Image geometry
            # ----------------------------------------------------------

            width=self.pre.width,
            height=self.pre.height,

            pre_shape=self.pre.shape,
            post_shape=self.post.shape,

            crs=str(self.pre.crs),

            transform=str(self.pre.transform),

            pixel_size_x=self.pre.pixel_size_x,
            pixel_size_y=self.pre.pixel_size_y,

            # ----------------------------------------------------------
            # Image statistics
            # ----------------------------------------------------------

            nan_percentage_pre=pre_stats["nan_percentage"],
            nan_percentage_post=post_stats["nan_percentage"],

            mean_pre=pre_stats["mean"],
            std_pre=pre_stats["std"],
            min_pre=pre_stats["minimum"],
            max_pre=pre_stats["maximum"],

            mean_post=post_stats["mean"],
            std_post=post_stats["std"],
            min_post=post_stats["minimum"],
            max_post=post_stats["maximum"],

            # ----------------------------------------------------------
            # Acquisition metadata
            # ----------------------------------------------------------

            acquisition_pre=pre_acq.acquisition_date,
            acquisition_post=post_acq.acquisition_date,

            satellite=pre_acq.platform,

            orbit_direction=pre_acq.orbit_direction,

            relative_orbit=pre_acq.relative_orbit,
        )