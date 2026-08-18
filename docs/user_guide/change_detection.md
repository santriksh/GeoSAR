# Change Detection

## Introduction

One of the most powerful applications of Synthetic Aperture Radar (SAR) is the ability to monitor how the Earth's surface changes over time.

Because SAR systems operate independently of sunlight and can penetrate cloud cover, they are particularly well suited for monitoring dynamic events such as:

- Floods
- Landslides
- Forest disturbance
- Urban expansion
- Agricultural change
- Coastal erosion
- Snow and ice dynamics

GeoSAR provides several change detection methods that compare two SAR acquisitions and quantify changes in radar backscatter.

---

# What is Change Detection?

Change detection is the process of identifying locations where the radar backscatter has changed between two SAR acquisitions.

Typically, two images are required:

- **Before Image (Reference)** – acquired before the event.
- **After Image (Comparison)** – acquired after the event.

The objective is to estimate how much each pixel has changed.

For example, during a flood:

- Open water generally exhibits lower radar backscatter.
- Vegetation may become partially submerged.
- Urban regions may exhibit little change.

Comparing the two acquisitions allows flooded areas to be identified automatically.

---

# Image Alignment

Before comparing two SAR images, they must represent exactly the same geographic area.

GeoSAR validates that the images have identical:

- Image dimensions
- Coordinate Reference System (CRS)
- Affine transformation
- Pixel alignment

Attempting to compare incompatible images raises an informative error.

Accurate image alignment is essential because even a one-pixel shift can produce false change detections.

---

# Difference Change Detection

The simplest approach measures the absolute difference between two images.

The difference image is computed as

\[
Difference = I_{after} - I_{before}
\]

GeoSAR provides:

```python
difference = sar.difference_change(
    before,
    after,
)
```

Positive values indicate an increase in backscatter, while negative values indicate a decrease.

Difference images are straightforward to compute and interpret but may be influenced by overall scene brightness.

---

# Ratio Change Detection

Rather than measuring absolute change, ratio methods measure proportional change.

The ratio is computed in the linear domain:

\[
Ratio=\frac{I_{after}}{I_{before}}
\]

GeoSAR provides:

```python
ratio = sar.ratio_change(
    before,
    after,
)
```

Ratio images reduce the influence of overall radiometric intensity and are widely used for flood detection.

For example:

| Surface | Typical Ratio |
|----------|--------------:|
| No change | ≈ 1 |
| Increased backscatter | > 1 |
| Decreased backscatter | < 1 |

---

# Log-Ratio Change Detection

The logarithmic ratio converts multiplicative changes into additive changes.

It is defined as

\[
LogRatio =
10\log_{10}
\left(
\frac{I_{after}}
{I_{before}}
\right)
\]

GeoSAR provides:

```python
log_ratio = sar.log_ratio_change(
    before,
    after,
)
```

Log-ratio images are especially useful because:

- No change is centred around **0 dB**.
- Negative values indicate decreased backscatter.
- Positive values indicate increased backscatter.

This representation is intuitive and is commonly used for SAR flood mapping.

---

# Choosing a Change Detection Method

Different applications benefit from different approaches.

| Method | Advantages | Limitations |
|---------|------------|-------------|
| Difference | Simple | Sensitive to overall brightness |
| Ratio | Robust to brightness variation | Less intuitive to interpret |
| Log-Ratio | Easy interpretation and robust | Requires logarithmic conversion |

For flood mapping, GeoSAR recommends **Log-Ratio Change Detection** because flooded areas typically exhibit significant reductions in radar backscatter that are easily interpreted in decibel units.

---

# Typical Workflow

```text
Load Before Image
        │
        ▼
Load After Image
        │
        ▼
Convert to Linear
        │
        ▼
Apply Speckle Filtering
        │
        ▼
Compute Change Image
        │
        ▼
Threshold Change Image
        │
        ▼
Morphological Cleanup
        │
        ▼
Flood Map
```

Each step progressively reduces uncertainty while improving the quality of the final flood mask.

---

# GeoSAR Example

```python
import sar

before = sar.load_sar("preflood.tif")
after = sar.load_sar("postflood.tif")

before = sar.db_to_linear(before)
after = sar.db_to_linear(after)

before = sar.refined_lee(before)
after = sar.refined_lee(after)

change = sar.log_ratio_change(
    before,
    after,
)
```

The resulting change image can be thresholded to produce a binary flood mask.

---

# Best Practices

- Compare images acquired using the same polarization.
- Use acquisitions with similar viewing geometry.
- Apply speckle filtering before change detection.
- Ensure accurate spatial alignment.
- Prefer log-ratio methods for flood detection.

---

# Summary

In this chapter, you learned:

- What SAR change detection is.
- Why image alignment is essential.
- The difference between Difference, Ratio, and Log-Ratio methods.
- How GeoSAR implements each approach.
- Recommended workflows for flood mapping.

---

## What's Next?

A change image highlights where backscatter has changed, but it does not directly identify flooded areas.

The next chapter introduces **Thresholding**, where we learn how to convert continuous change measurements into binary flood masks using techniques such as Otsu's threshold.