# Thresholding

## Introduction

After computing a change image, each pixel contains a continuous value representing the magnitude of change between two SAR acquisitions.

While these continuous values are useful for visualization, many practical applications require a binary decision:

- Flooded or Not Flooded
- Changed or Unchanged
- Water or Land

The process of converting continuous pixel values into discrete classes is known as **thresholding**.

GeoSAR currently provides automatic threshold estimation using **Otsu's method**, one of the most widely used unsupervised thresholding techniques.

---

# Why Thresholding is Needed

Consider a log-ratio change image.

Pixels may have values such as:

| Pixel | Log-Ratio (dB) |
|--------|---------------:|
| A | -6.8 |
| B | -5.1 |
| C | -1.7 |
| D | 0.2 |
| E | 1.1 |

Although these values indicate different levels of change, they do not directly identify flooded areas.

Thresholding converts these continuous measurements into a binary classification.

For example,

| Log-Ratio | Classification |
|-----------|----------------|
| ≤ Threshold | Flooded |
| > Threshold | Not Flooded |

This binary representation forms the basis for subsequent morphological processing and flood mapping.

---

# Histogram-Based Thresholding

Thresholding methods typically operate on the histogram of the change image.

A histogram shows the distribution of pixel values.

In many flood mapping applications:

- One group of pixels corresponds to unchanged land.
- Another group corresponds to flooded regions.

The objective is to find a threshold that best separates these two groups.

A typical histogram may appear conceptually as:

```text
Frequency
 ^
 |
 |                 Land
 |               /^^^^^^\
 |              /        \
 |             /          \
 |            /            \
 |____Flood__/______________\________> Pixel Value
          ^
      Threshold
```

The threshold is chosen so that the separation between the two classes is maximized.

---

# Otsu's Method

GeoSAR implements **Otsu's thresholding algorithm**.

Otsu's method automatically determines a threshold by maximizing the **between-class variance** of the histogram.

Unlike manually selecting a threshold, Otsu's method:

- Requires no user-defined threshold value.
- Adapts to different datasets.
- Is completely unsupervised.

This makes it an excellent first choice for many SAR applications.

---

# GeoSAR Example

```python
import sar

threshold = sar.otsu_threshold(
    change_image,
)
```

The function returns a single threshold value.

For example,

```python
print(threshold)

-3.84
```

This value can then be used to classify flooded pixels.

---

# Creating a Binary Flood Mask

Once a threshold has been estimated, each pixel can be classified.

Conceptually,

```text
Pixel ≤ Threshold
        │
        ├── Yes → Flooded
        │
        └── No  → Not Flooded
```

GeoSAR internally performs this step during the flood detection workflow.

The resulting binary image contains:

- 1 → Flooded
- 0 → Not Flooded

---

# Why Otsu Works Well

Otsu's method performs particularly well when the histogram contains two reasonably distinct groups.

For flood mapping this often corresponds to:

- Flooded regions with lower backscatter.
- Non-flooded land with higher backscatter.

When these groups are well separated, Otsu's method usually produces an effective threshold automatically.

---

# Limitations

No thresholding method is universally optimal.

Otsu's method may perform less effectively when:

- The histogram contains only one dominant peak.
- The flooded area occupies a very small fraction of the image.
- Multiple land-cover types produce overlapping backscatter values.
- Significant speckle remains in the image.

In these situations, applying an adaptive speckle filter before thresholding often improves the histogram separation.

---

# Typical Workflow

```text
Before Image
        │
        ▼
After Image
        │
        ▼
Log-Ratio Change
        │
        ▼
Histogram
        │
        ▼
Otsu Threshold
        │
        ▼
Binary Flood Mask
```

Thresholding transforms the continuous change image into a binary representation suitable for further processing.

---

# Best Practices

- Apply speckle filtering before threshold estimation.
- Use log-ratio change images for flood detection.
- Inspect the histogram to ensure that two distinct classes are present.
- Validate the resulting flood mask visually whenever possible.

---

# Summary

In this chapter, you learned:

- Why thresholding is necessary.
- How histograms are used for threshold estimation.
- How Otsu's method selects an automatic threshold.
- How GeoSAR generates binary flood masks.
- The strengths and limitations of automatic thresholding.

---

## What's Next?

Thresholding produces a binary flood mask, but small isolated regions and holes often remain.

The next chapter introduces **Morphology**, where we learn how morphological operations remove noise, fill gaps, and improve the quality of the final flood map.