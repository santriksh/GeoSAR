"""
Data models used by the GeoSAR validation framework.

These dataclasses store the outputs produced by different
validation stages (dataset inspection, speckle analysis,
change detection, threshold benchmarking, etc.).

Author: Santosh Kumar Singh
"""

from dataclasses import dataclass, field
from typing import Optional


# ==========================================================
# Dataset Summary
# ==========================================================

@dataclass
class DatasetSummary:
    """
    Summary statistics and metadata describing
    the input SAR image pair.
    """

    # Image dimensions
    width: int
    height: int

    # Original image shapes
    pre_shape: tuple[int, int]
    post_shape: tuple[int, int]

    # Spatial information
    crs: Optional[str]
    transform: Optional[str]

    pixel_size_x: float
    pixel_size_y: float

    # Missing data
    nan_percentage_pre: float
    nan_percentage_post: float

    # Basic statistics (Pre image)
    mean_pre: float
    std_pre: float
    min_pre: float
    max_pre: float

    # Basic statistics (Post image)
    mean_post: float
    std_post: float
    min_post: float
    max_post: float

    # Optional metadata
    acquisition_pre: Optional[str] = None
    acquisition_post: Optional[str] = None

    satellite: Optional[str] = None
    orbit_direction: Optional[str] = None
    relative_orbit: Optional[int] = None


# ==========================================================
# Speckle Filter Metrics
# ==========================================================

@dataclass
class SpeckleMetrics:
    """
    Metrics describing the effect of speckle filtering.
    """

    filter_name: str

    window_size: int

    damping_factor: Optional[float] = None

    cv_before_pre: float = 0.0
    cv_after_pre: float = 0.0

    cv_before_post: float = 0.0
    cv_after_post: float = 0.0

    reduction_pre: float = 0.0
    reduction_post: float = 0.0


# ==========================================================
# Change Detection Metrics
# ==========================================================

@dataclass
class ChangeMetrics:
    """
    Statistics describing the change image.
    """

    mean: float
    std: float

    minimum: float
    maximum: float

    median: float

    percentiles: dict[float, float]

    otsu_threshold: Optional[float] = None


# ==========================================================
# Threshold Benchmark Result
# ==========================================================

@dataclass
class ThresholdResult:
    """
    Result of one thresholding method.
    """

    method: str

    threshold: float

    flood_percentage: float

    connected_components: int

    largest_component_size: int


# ==========================================================
# Final Validation Result
# ==========================================================

@dataclass
class ValidationResult:
    """
    Complete validation output produced by the
    GeoSAR validation framework.
    """

    dataset_name: str

    dataset: Optional[DatasetSummary] = None

    speckle: Optional[SpeckleMetrics] = None

    change: Optional[ChangeMetrics] = None

    thresholds: list[ThresholdResult] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)