# Morphology

## Introduction

After thresholding, the flood detection process produces a **binary flood mask** in which each pixel is classified as either flooded or non-flooded.

Although this binary image identifies the major flooded regions, it often contains imperfections caused by residual speckle, thresholding uncertainty, and isolated misclassified pixels.

Common artifacts include:

- Small isolated flooded pixels
- Tiny non-flooded holes inside flooded regions
- Broken river segments
- Jagged boundaries
- Small disconnected objects

Morphological image processing provides a set of operations that improve the quality of binary images while preserving the overall flood extent.

GeoSAR includes several morphology functions that simplify this post-processing step.

---

# Why Morphology is Needed

Consider the binary flood mask immediately after thresholding.

Conceptually, it may look like:

```text
███████████
██████░████
███████████
██░████████
███████████
```

The isolated pixels (░) are often classification noise rather than real flood features.

Morphological operations remove these artifacts and produce a cleaner, more interpretable flood map.

---

# Binary Morphology

Morphological operations work on **binary images**.

Each pixel belongs to one of two classes:

- **1** → Flooded
- **0** → Not Flooded

Instead of modifying pixel values directly, morphology modifies the **shape** of connected regions.

This makes morphology particularly useful for cleaning segmentation and classification results.

---

# Structuring Elements

Morphological operations examine the neighborhood surrounding each pixel.

This neighborhood is called the **structuring element**.

GeoSAR currently supports configurable pixel connectivity.

Typical choices are:

- **4-connectivity**
- **8-connectivity**

Higher connectivity generally produces smoother connected regions.

---

# Removing Small Objects

Small isolated regions are frequently produced by residual speckle or thresholding errors.

GeoSAR provides:

```python
from sar.morphology import remove_small_objects

clean = remove_small_objects(
    flood_mask,
    min_size=25,
)
```

Objects smaller than the specified size are removed while larger connected flood regions are preserved.

This operation is usually the first post-processing step after thresholding.

---

# Binary Opening

Binary opening removes small foreground objects while preserving larger structures.

It is particularly useful for eliminating isolated flooded pixels.

GeoSAR provides:

```python
from sar.morphology import binary_opening

opened = binary_opening(
    flood_mask,
)
```

Opening is commonly applied before closing.

---

# Binary Closing

Binary closing fills small holes and connects nearby flooded regions.

GeoSAR provides:

```python
from sar.morphology import binary_closing

closed = binary_closing(
    flood_mask,
)
```

Closing is useful for:

- Filling small gaps
- Connecting fragmented flood regions
- Producing smoother flood boundaries

---

# Typical Morphological Workflow

A common post-processing sequence is:

```text
Threshold
     │
     ▼
Remove Small Objects
     │
     ▼
Binary Opening
     │
     ▼
Binary Closing
     │
     ▼
Final Flood Mask
```

Each operation progressively improves the binary flood mask while preserving the major flooded regions.

---

# Morphology in GeoSAR

GeoSAR combines these operations into the flood detection pipeline.

The default workflow is:

1. Generate a change image.
2. Estimate an automatic threshold.
3. Create a binary flood mask.
4. Remove isolated objects.
5. Apply binary opening.
6. Apply binary closing.

This sequence produces a cleaner flood map without requiring extensive manual tuning.

---

# Choosing Parameters

The effectiveness of morphological processing depends on the selected parameters.

### Minimum Object Size

The `min_size` parameter determines the smallest connected flooded region that will be retained.

Small values preserve fine details.

Larger values remove more noise but may also eliminate small genuine flooded regions.

### Connectivity

Connectivity determines how neighboring pixels are grouped into connected objects.

Higher connectivity generally produces smoother and more continuous flood regions.

The optimal choice depends on the spatial resolution of the SAR image and the characteristics of the landscape.

---

# Best Practices

- Perform morphology only after thresholding.
- Remove isolated objects before applying opening or closing.
- Avoid excessively large minimum object sizes.
- Visually inspect the cleaned flood mask.
- Choose parameters appropriate for the image resolution.

---

# Complete Flood Detection Workflow

The complete GeoSAR flood mapping pipeline is:

```text
Load SAR Images
        │
        ▼
Convert to Linear
        │
        ▼
Speckle Filtering
        │
        ▼
Change Detection
        │
        ▼
Thresholding
        │
        ▼
Morphological Processing
        │
        ▼
Flood Statistics
        │
        ▼
Final Flood Map
```

This workflow forms the basis of the `detect_flood()` pipeline implemented in GeoSAR.

---

# Summary

In this chapter, you learned:

- Why binary flood masks require post-processing.
- How morphology improves flood maps.
- How to remove isolated objects.
- How opening and closing modify connected regions.
- How morphology fits into the complete GeoSAR workflow.

---

## What's Next?

You have now completed the core GeoSAR User Guide.

The next step is to explore the **API Reference**, where each GeoSAR function is documented in detail, including its parameters, return values, and usage examples.