# Statistics Module

## Overview

The Statistics module provides neighborhood-based statistical operations
for Synthetic Aperture Radar (SAR) images.

Unlike global image statistics, these algorithms compute statistics
within a moving window centered on each pixel.

The resulting images describe the local statistical properties of the
scene and form the foundation for many subsequent SAR processing
algorithms, including:

- Speckle filtering
- Texture analysis
- Feature engineering
- Image segmentation
- Machine learning

Current functions

- local_mean()
- local_variance()
- local_std()
- coefficient_of_variation()

Future functions

- equivalent_number_of_looks()
- local_median()
- local_percentile()
- local_entropy()

---

# Why Local Statistics?

A SAR image contains millions of pixels.

Looking at a single pixel rarely provides enough information to
understand the underlying terrain.

Instead, we examine a neighborhood around each pixel.

Example

5 × 5 Window

□ □ □ □ □

□ □ □ □ □

□ □ ■ □ □

□ □ □ □ □

□ □ □ □ □

The center pixel is replaced by a statistic computed from all valid
pixels in the surrounding window.

This produces a new image describing the local properties of the scene.

---

# Moving Window Concept

Every statistical function follows the same pattern.

Input Image

↓

Moving Window

↓

Compute Statistic

↓

Output Image

Each output pixel summarizes the neighborhood surrounding the
corresponding input pixel.

Only valid pixels contribute to the computation.

NaN values are ignored.

---

# local_mean()

Purpose

Estimate the average local backscatter.

Formula

μ = (1/N) Σ xi

Implementation

- NaN-aware
- Moving window
- uniform_filter()
- Safe division using numpy.divide()

Applications

- Speckle reduction
- Lee Filter
- Local intensity estimation
- Baseline for higher-order statistics

Characteristics

- Smooths the image
- Reduces speckle
- Blurs edges

---

# local_variance()

Purpose

Measure local variability.

```
The canonical identity is illustrated below.
```


::contentReference[oaicite:0]{index=0}


Implementation

Rather than computing deviations directly, GeoSAR uses

Mean of Squares

↓

Minus

↓

Square of Mean

Advantages

- Reuses local_mean()
- Efficient
- Numerically stable

Applications

- Lee Filter
- ENL estimation
- Texture analysis
- Land-cover characterization

Characteristics

Low variance

↓

Homogeneous regions

High variance

↓

Heterogeneous regions

---

# local_std()

Purpose

Measure the local spread of backscatter values.


::contentReference[oaicite:1]{index=1}


Implementation

local_std()

↓

local_variance()

↓

Square root

Applications

- Relative variability
- Texture analysis
- Coefficient of Variation

Characteristics

Always non-negative.

Window size = 1

↓

Standard deviation = 0

---

# coefficient_of_variation()

Purpose

Measure relative variability independent of absolute intensity.

Definition

CV = Standard Deviation / Mean

Input Requirements

✔ Linear images only

GeoSAR validates this automatically.

Attempting to compute CV on dB images raises a ValueError.

Applications

- Flood detection
- Surface roughness
- Relative heterogeneity
- Feature engineering

Characteristics

Low CV

↓

Uniform surfaces

High CV

↓

Highly textured surfaces

---

# Choosing the Right Statistic

| Objective | Recommended Statistic |
|------------|-----------------------|
| Estimate average backscatter | local_mean() |
| Measure variability | local_variance() |
| Measure spread | local_std() |
| Compare relative variability | coefficient_of_variation() |

---

# Common Pitfalls

## Even window sizes

Incorrect

window_size = 4

Correct

window_size = 5

GeoSAR requires odd window sizes so that every neighborhood has a
well-defined center pixel.

---

## Computing CV on dB images

Incorrect

cv = coefficient_of_variation(pre)

Correct

linear = db_to_linear(pre)

cv = coefficient_of_variation(linear)

---

## Interpreting variance

Variance is not a measure of brightness.

Two neighborhoods may have the same mean backscatter but very different
variance.

Variance measures local heterogeneity rather than intensity.

---

# Design Principles

Every statistical function

- accepts SARImage
- returns SARImage
- preserves metadata
- updates provenance
- ignores NaN values
- validates inputs

---

# Relationship to Other Modules

Statistics

↓

Filtering

↓

Texture

↓

Feature Engineering

↓

Machine Learning

The Statistics module forms the computational foundation for many
higher-level SAR algorithms.

---

# Current Status

Completed

✓ local_mean()

✓ local_variance()

✓ local_std()

✓ coefficient_of_variation()

Planned

• equivalent_number_of_looks()

• local_median()

• local_entropy()

• Robust statistics


# Design Decisions

## NaN Handling

All statistical computations ignore NaN values.

This allows partially masked SAR images to be processed without
introducing bias.

---

## Window Size

Only odd window sizes are supported.

This guarantees that every neighborhood has a unique center pixel.

---

## Safe Numerical Operations

GeoSAR uses `numpy.divide()` with the `where=` parameter instead of
direct division.

This prevents divide-by-zero warnings and improves numerical stability.

---

## Metadata Preservation

Every statistical operation returns a new `SARImage`.

The original image is never modified.
