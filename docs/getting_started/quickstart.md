# Quick Start

This tutorial introduces the fundamental GeoSAR workflow for detecting flooded regions from a pair of Sentinel-1 SAR images.

By the end of this guide, you will:

- Load Sentinel-1 SAR images
- Convert image values from dB to Linear scale
- Reduce speckle noise
- Compute a change image
- Estimate an automatic threshold
- Generate a binary flood mask
- Remove isolated noise
- Visualize the final result

No prior knowledge of GeoSAR is assumed.

---

# Workflow Overview

A typical flood detection workflow consists of the following steps.

```text
Pre-Flood Image          Post-Flood Image
        │                        │
        └────────────┬───────────┘
                     │
               Load Images
                     │
          Convert dB → Linear
                     │
            Refined Lee Filter
                     │
            Log-Ratio Change
                     │
             Otsu Threshold
                     │
           Binary Flood Mask
                     │
      Morphological Processing
                     │
             Final Flood Map
```

---

# Step 1 — Import GeoSAR

```python
import sar
```

GeoSAR exposes the most commonly used functionality through its top-level package.

---

# Step 2 — Load SAR Images

Load the pre-event and post-event Sentinel-1 images.

```python
pre = sar.load_sar("pre_flood.tif")
post = sar.load_sar("post_flood.tif")
```

Each call returns a `SARImage` object containing:

- Image data
- Valid pixel mask
- Spatial metadata
- Acquisition metadata
- Processing history

The metadata is preserved automatically throughout the processing workflow.

---

# Step 3 — Convert to Linear Scale

Many SAR algorithms operate on linear backscatter rather than decibel (dB) values.

Convert both images.

```python
pre = sar.db_to_linear(pre)
post = sar.db_to_linear(post)
```

---

# Step 4 — Reduce Speckle Noise

SAR imagery contains multiplicative speckle noise.

Apply the Refined Lee filter.

```python
pre = sar.refined_lee(pre)
post = sar.refined_lee(post)
```

The Refined Lee filter reduces speckle while preserving edges and image detail.

---

# Step 5 — Compute the Change Image

Calculate the logarithmic ratio between the filtered images.

```python
change = sar.log_ratio_change(pre, post)
```

The log-ratio image highlights areas where significant changes occurred between the two acquisitions.

---

# Step 6 — Estimate a Threshold

Automatically estimate a threshold using Otsu's method.

```python
threshold = sar.otsu_threshold(change)
```

No manual threshold selection is required.

---

# Step 7 — Generate the Flood Mask

Convert the change image into a binary flood map.

```python
flood = sar.threshold_flood(
    change,
    threshold=threshold,
    direction="less",
)
```

Pixels satisfying the threshold criterion are classified as flooded.

---

# Step 8 — Remove Small Objects

Apply morphological processing to remove isolated noisy regions.

```python
flood = sar.binary_opening(flood)

flood = sar.binary_closing(flood)

flood = sar.remove_small_objects(
    flood,
    min_size=20,
)
```

These operations improve the quality of the final flood mask.

---

# Step 9 — Display the Result

Display the flood map.

```python
flood.show()
```

You can also visualize intermediate processing results.

```python
change.show()

pre.show()

post.show()
```

---

# Complete Example

```python
import sar

pre = sar.load_sar("pre_flood.tif")
post = sar.load_sar("post_flood.tif")

pre = sar.db_to_linear(pre)
post = sar.db_to_linear(post)

pre = sar.refined_lee(pre)
post = sar.refined_lee(post)

change = sar.log_ratio_change(pre, post)

threshold = sar.otsu_threshold(change)

flood = sar.threshold_flood(
    change,
    threshold=threshold,
    direction="less",
)

flood = sar.binary_opening(flood)
flood = sar.binary_closing(flood)
flood = sar.remove_small_objects(
    flood,
    min_size=20,
)

flood.show()
```

---

# Summary

In this tutorial you learned how to:

- Load Sentinel-1 SAR imagery
- Convert to linear scale
- Reduce speckle noise
- Detect change
- Generate a flood mask
- Apply morphological processing
- Visualize the results

---

# Next Steps

Continue with:

**First Flood Detection**

The next tutorial explains the complete flood detection workflow in greater depth, including flood statistics, parameter selection, and interpretation of the results.