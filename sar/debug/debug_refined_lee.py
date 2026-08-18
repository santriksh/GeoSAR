import numpy as np
import os
import sys

# Adds the directory containing 'sar' to the search path
sys.path.append(os.path.abspath(".."))
from sar.features.window_views import build_window_view
from sar.features.subwindow_grid import build_subwindow_mean_grid
from sar.sar_statistics import local_mean
from sar.features.subwindow_variance_grid import (
    build_subwindow_variance_grid,
)
from sar.filters.refined_lee import _extract_subwindows
from sar.features.gradients import (
    compute_signed_composite_gradients,
)

from sar.filters.refined_lee import (
    _compute_signed_composite_gradients,
)
from sar.sar_image import SARImage
from sar.sar_metadata import (
    SARMetadata,
    SpatialMetadata,
    AcquisitionMetadata,
    ProcessingMetadata,
    ProvenanceMetadata,
    CustomMetadata,
)
from rasterio.transform import Affine
from rasterio.coords import BoundingBox
from sar.features.gradients import (
    compute_gradient_directions,
)

from sar.filters.refined_lee import (
    _gradient_direction,
)
from sar.features.directional_statistics import (
    compute_directional_means,
)

from sar.filters.refined_lee import (
    _directional_statistics,
)
from sar.features.directional_statistics import compute_directional_variances

from sar.features.noise import (
    compute_normalized_variance_grid,
    compute_noise_variance,
)

from sar.filters.refined_lee import (
    _estimate_noise_variance,
)
from sar.features.mmse import (compute_signal_variance,compute_mmse_weight)
from sar.constants.refined_lee import EPS
from sar.filters.refined_lee import refined_lee_filter
from sar.filters.refined_lee_geosar import _compute_mean_grid 

rng = np.random.default_rng(42)

data = rng.random((21,21))

mask = np.ones_like(data, dtype=bool)

metadata = SARMetadata(
    spatial=SpatialMetadata(
        crs="EPSG:32646",
        transform=Affine.identity(),
        bounds=BoundingBox(0,0,21,21),
        resolution=(10.0,10.0),
        shape=data.shape,
    ),
    acquisition=AcquisitionMetadata(),
    processing=ProcessingMetadata(
        value_scale="linear",
    ),
    provenance=ProvenanceMetadata(),
    custom=CustomMetadata(),
)

image = SARImage(
    data=data,
    mask=mask,
    metadata=metadata,
)


ROW = 0
COL = 0

windows = build_window_view(
    image.data,
)

window = windows[
    ROW,
    COL,
]

mean_image = local_mean(
    image,
    window_size=3,
).data

mean_grid = build_subwindow_mean_grid(
    mean_image,
)

vector_means = mean_grid[
    ROW,
    COL,
].reshape(-1)



reference_means = np.array(
    [
        np.mean(patch)
        for patch in _extract_subwindows(window)
    ]
)

print("Vector Means")
print(vector_means)

print()

print("Reference Means")
print(reference_means)

print()

print("Difference")
print(vector_means - reference_means)

print()

print("Max Difference")
print(np.max(np.abs(
    vector_means-reference_means
)))


print("\n" + "=" * 60)
print("STAGE 2 : SUBWINDOW VARIANCES")
print("=" * 60)

variance_grid = build_subwindow_variance_grid(
    windows,
)

vector_variances = variance_grid[
    ROW,
    COL,
].reshape(-1)

reference_variances = np.array(
    [
        np.var(patch)
        for patch in _extract_subwindows(window)
    ]
)

print("\nVector Variances")
print(vector_variances)

print("\nReference Variances")
print(reference_variances)

difference = vector_variances - reference_variances

print("\nDifference")
print(difference)

print("\nMax Difference")
print(
    np.max(
        np.abs(difference)
    )
)


print("\n" + "=" * 60)
print("STAGE 3 : SIGNED COMPOSITE GRADIENTS")
print("=" * 60)

vector_signed = compute_signed_composite_gradients(
    mean_grid[
        ROW,
        COL,
    ]
)

reference_signed = (
    _compute_signed_composite_gradients(
        reference_means,
    )
)

print("\nVector Signed Gradients")
print(vector_signed)

print("\nReference Signed Gradients")
print(reference_signed)

difference = (
    vector_signed
    -
    reference_signed
)

print("\nDifference")
print(difference)

print("\nMax Difference")
print(
    np.max(
        np.abs(
            difference
        )
    )
)
##############
vector_direction = compute_gradient_directions(
    vector_signed.reshape(1, 4)
)[0]

reference_direction = _gradient_direction(
    reference_means,
)

print("\n" + "=" * 60)
print("STAGE 4 : GRADIENT DIRECTION")
print("=" * 60)

print("\nVector Direction")
print(vector_direction)

print("\nReference Direction")
print(reference_direction)

print("\nMatch")
print(vector_direction == reference_direction)
#################
directional_means = compute_directional_means(
    windows,
)

vector_mean = directional_means[
    ROW,
    COL,
    vector_direction,
]

reference_mean, _ = _directional_statistics(
    window,
    reference_direction,
)


print("\n" + "=" * 60)
print("STAGE 5 : DIRECTIONAL MEAN")
print("=" * 60)

print("\nVector Mean")
print(vector_mean)

print("\nReference Mean")
print(reference_mean)

print("\nDifference")
print(vector_mean - reference_mean)

print("\nMatch")
print(
    np.isclose(
        vector_mean,
        reference_mean,
        atol=1e-12,
    )
)
##############
directional_variances = compute_directional_variances(
    windows,
)

vector_variance = directional_variances[
    ROW,
    COL,
    vector_direction,
]

reference_mean, reference_variance = (
    _directional_statistics(
        window,
        reference_direction,
    )
)

print("\n" + "=" * 60)
print("STAGE 6 : DIRECTIONAL VARIANCE")
print("=" * 60)

print("\nVector Variance")
print(vector_variance)

print("\nReference Variance")
print(reference_variance)

difference = (
    vector_variance
    -
    reference_variance
)

print("\nDifference")
print(difference)

print("\nMatch")
print(
    np.isclose(
        vector_variance,
        reference_variance,
        atol=1e-12,
    )
)

####################
normalized_grid = compute_normalized_variance_grid(
    mean_grid,
    variance_grid,
)

noise_image = compute_noise_variance(
    normalized_grid,
)

vector_noise = noise_image[
    ROW,
    COL,
]

reference_noise = _estimate_noise_variance(
    reference_means,
    reference_variances,
)

print("\n" + "=" * 60)
print("STAGE 7 : NOISE VARIANCE")
print("=" * 60)

print("\nVector Noise")
print(vector_noise)
#############


print("\nReference Noise")
print(reference_noise)

difference = vector_noise - reference_noise

print("\nDifference")
print(difference)

print("\nMatch")
print(
    np.isclose(
        vector_noise,
        reference_noise,
        atol=1e-12,
    )
)
#######################
vector_signal = compute_signal_variance(
    np.array([[vector_mean]]),
    np.array([[vector_variance]]),
    np.array([[vector_noise]]),
)[0,0]

reference_signal = (
    reference_variance
    -
    reference_mean**2
    * reference_noise
)

reference_signal /= (
    reference_noise
    + 1.0
)

reference_signal = max(
    reference_signal,
    0.0,
)

print("\n" + "=" * 60)
print("STAGE 8 : SIGNAL VARIANCE")
print("=" * 60)

print("\nVector Signal")
print(vector_signal)

print("\nReference Signal")
print(reference_signal)

difference = (
    vector_signal
    -
    reference_signal
)

print("\nDifference")
print(difference)

print("\nMatch")
print(
    np.isclose(
        vector_signal,
        reference_signal,
        atol=1e-12,
    )
)
##################
vector_weight = compute_mmse_weight(
    np.array([[vector_signal]]),
    np.array([[vector_variance]]),
)[0,0]

reference_weight = (
    reference_signal
    /
    max(
        reference_variance,
        EPS,
    )
)

reference_weight = np.clip(
    reference_weight,
    0.0,
    1.0,
)


print("\n" + "=" * 60)
print("STAGE 9 : MMSE WEIGHT")
print("=" * 60)

print("\nVector Weight")
print(vector_weight)

print("\nReference Weight")
print(reference_weight)

difference = (
    vector_weight
    -
    reference_weight
)

print("\nDifference")
print(difference)

print("\nMatch")
print(
    np.isclose(
        vector_weight,
        reference_weight,
        atol=1e-12,
    )
)
##############
vector_filtered = (
    vector_mean
    +
    vector_weight
    * (
        window[3, 3]
        - vector_mean
    )
)

reference_filtered = refined_lee_filter(
    window,
)

print("\n" + "=" * 60)
print("STAGE 10 : FINAL FILTERED PIXEL")
print("=" * 60)

print("\nVector Filtered")
print(vector_filtered)

print("\nReference Filtered")
print(reference_filtered)

difference = vector_filtered - reference_filtered

print("\nDifference")
print(difference)

print("\nMatch")
print(
    np.isclose(
        vector_filtered,
        reference_filtered,
        atol=1e-12,
    )
)
################
manual_mean_image = local_mean(
    image,
    window_size=3,
).data

manual_mean_grid = build_subwindow_mean_grid(
    manual_mean_image,
)

wrapper_mean_grid = _compute_mean_grid(
    image,
)

print("=" * 60)
print("INTEGRATION STEP 1")
print("=" * 60)

print("Manual")
print(
    manual_mean_grid[10,10]
)

print()

print("Wrapper")
print(
    wrapper_mean_grid[10,10]
)

print()

np.testing.assert_allclose(
    manual_mean_grid,
    wrapper_mean_grid,
    atol=1e-12,
)

###########
print("=" * 70)
print("BORDER PIXEL (0,0)")
print("=" * 70)

print()

print("Scalar Means")
print(
    reference_means.reshape(3,3)
)

print()

print("Vector Means")
print(
    vector_means.reshape(3,3)
)

print()

print("Difference")
print(
    (
        vector_means
        -
        reference_means
    ).reshape(3,3)
)

print()

print(
    "Maximum Difference:",
    np.max(
        np.abs(
            vector_means
            -
            reference_means
        )
    ),
)
#########################
print("YYYYYYYYYYY")
reference_patch = _extract_subwindows(
    window
)[4]

print(reference_patch)

print()

print(
    mean_image[
        0:3,
        0:3,
    ]
)
