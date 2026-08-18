# First Flood Detection

This tutorial demonstrates a complete flood detection workflow using Sentinel-1 Synthetic Aperture Radar (SAR) imagery.

Unlike the Quick Start guide, this tutorial explains why each processing step is required and how the intermediate results should be interpreted.

By the end of this tutorial you will understand the complete GeoSAR flood detection workflow.

---

# Dataset

The tutorial assumes two co-registered Sentinel-1 Ground Range Detected (GRD) images:

- Pre-flood acquisition
- Post-flood acquisition

Both images should:

- Cover the same geographic region
- Have the same spatial resolution
- Share the same coordinate reference system (CRS)
- Already be terrain corrected

GeoSAR automatically validates that both images occupy the same spatial grid before change detection.

---

# Flood Detection Workflow

```

Pre-Flood SAR
│
▼
Load Image
│
▼
Convert to Linear
│
▼
Refined Lee Filter
│
▼
Log-Ratio Change
│
▲
Refined Lee Filter
│
▼
Convert to Linear
│
▼
Load Image
│
Post-Flood SAR

↓

Otsu Threshold

↓

Flood Mask

↓

Morphological Cleanup

↓

Flood Statistics

```

---

# Step 1 — Load the Images

```python
import sar

pre = sar.load_sar("pre_flood.tif")

post = sar.load_sar("post_flood.tif")
```

GeoSAR stores both raster values and metadata inside the `SARImage` object.

This metadata is preserved throughout the workflow.

---

# Step 2 — Convert to Linear Scale

Most adaptive speckle filters operate on linear backscatter values rather than logarithmic (dB) values.

```python
pre = sar.db_to_linear(pre)

post = sar.db_to_linear(post)
```

---

# Step 3 — Reduce Speckle

Speckle is an inherent property of coherent radar imaging.

Apply the Refined Lee filter to both images.

```python
pre = sar.refined_lee(pre)

post = sar.refined_lee(post)
```

The objective is to reduce noise while preserving the boundaries of flooded regions.

---

# Step 4 — Compute the Change Image

GeoSAR provides several change detection methods.

For flood detection, the logarithmic ratio is commonly used.

```python
change = sar.log_ratio_change(
    pre,
    post,
)
```

Display the result.

```python
change.show()
```

Areas with strong negative values often correspond to newly flooded regions because smooth water surfaces reflect radar energy away from the sensor.

---

# Step 5 — Estimate the Threshold

Instead of selecting a threshold manually, estimate one automatically.

```python
threshold = sar.otsu_threshold(change)
```

GeoSAR analyzes the histogram of the change image and identifies the threshold that best separates two classes.

---

# Step 6 — Generate the Flood Mask

```python
flood = sar.threshold_flood(
    change,
    threshold=threshold,
    direction="less",
)
```

Pixels below the threshold are classified as flooded.

Display the binary result.

```python
flood.show()
```

---

# Step 7 — Morphological Processing

Binary masks often contain isolated pixels and small noisy regions.

Improve the mask.

```python
flood = sar.binary_opening(flood)

flood = sar.binary_closing(flood)

flood = sar.remove_small_objects(
    flood,
    min_size=20,
)
```

These operations remove small artifacts while preserving larger flooded regions.

---

# Step 8 — Flood Statistics

GeoSAR can summarize the resulting flood map.

Example statistics include:

- Flooded pixel count
- Flooded area (m²)
- Flooded area (hectares)
- Flooded area (km²)
- Percentage of flooded pixels

These statistics can be used for reporting or comparison between events.

---

# Visualizing the Workflow

Display the intermediate products.

```python
pre.show()

post.show()

change.show()

flood.show()
```

Examining intermediate outputs helps verify that each processing step behaves as expected.

---

# Common Pitfalls

## Images are not aligned

Flood detection requires both images to share the same spatial grid.

GeoSAR validates image compatibility before processing.

---

## Images remain in dB

Adaptive speckle filters require linear backscatter values.

Always convert using:

```python
sar.db_to_linear()
```

before filtering.

---

## Threshold selects excessive flooding

Inspect the change image and histogram before adjusting the threshold manually.

---

# Summary

You have completed an end-to-end flood detection workflow using GeoSAR.

The workflow consisted of:

1. Loading Sentinel-1 imagery
2. Radiometric conversion
3. Speckle reduction
4. Log-ratio change detection
5. Automatic threshold estimation
6. Flood mask generation
7. Morphological cleanup
8. Flood statistics

---

# Next Steps

Continue with the User Guide to understand the theory behind each processing step.

Recommended reading:

- SAR Basics
- Radiometric Processing
- Speckle Filtering