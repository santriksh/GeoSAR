# Speckle Filtering

## Introduction

One of the defining characteristics of Synthetic Aperture Radar (SAR) imagery is the presence of **speckle**. Unlike optical images, SAR images exhibit a grainy appearance, even over surfaces that are physically uniform.

Speckle is not a sensor defect or measurement error. It is an inherent property of coherent imaging systems and is produced by the constructive and destructive interference of microwave signals reflected from many individual scatterers within each image pixel.

Although speckle contains useful statistical information, it also makes visual interpretation and automated image analysis more challenging. The objective of speckle filtering is therefore **not to eliminate speckle completely**, but rather to reduce its effect while preserving meaningful image structures.

GeoSAR provides several adaptive speckle filters that are widely used in the remote sensing community.

---

# Why Does Speckle Occur?

Each SAR pixel represents the combined radar return from many individual scatterers contained within a single ground resolution cell.

These scatterers may include:

- Leaves
- Tree branches
- Soil particles
- Rocks
- Buildings
- Surface roughness

Every scatterer reflects the transmitted microwave pulse with a different phase.

When these reflected waves return to the radar antenna, they interfere with one another.

The interference may be:

- **Constructive**, producing a brighter pixel.
- **Destructive**, producing a darker pixel.

As a result, even completely homogeneous terrain appears noisy.

This granular appearance is known as **speckle**.

---

## Multiplicative Noise

Unlike the additive noise commonly encountered in optical imagery, SAR speckle is **multiplicative**.

This means that the amount of speckle depends on the underlying backscatter intensity.

Consequently:

- Bright regions generally exhibit larger absolute fluctuations.
- Dark regions exhibit smaller fluctuations.

Because of this property, conventional smoothing techniques such as Gaussian or mean filters are generally not suitable for SAR imagery, as they tend to blur important image structures.

---

## Why Speckle Filtering is Necessary

Speckle affects many common SAR processing tasks.

For example:

- Flood boundaries become difficult to identify.
- Water bodies appear fragmented.
- Roads become discontinuous.
- Texture measurements become unstable.
- Image segmentation becomes less reliable.
- Change detection generates more false alarms.

Reducing speckle before further analysis generally improves the robustness of downstream processing.

However, excessive smoothing can remove important information.

A good speckle filter therefore attempts to:

- Reduce speckle.
- Preserve edges.
- Preserve fine structures.
- Preserve radiometric characteristics.

---

# Adaptive Speckle Filters

Unlike conventional image smoothing filters, adaptive speckle filters modify their behaviour depending on the local image statistics.

In homogeneous regions they perform stronger smoothing.

Near edges and image features they reduce smoothing in order to preserve important structures.

GeoSAR currently provides five adaptive speckle filters.

| Filter | Characteristics |
|---------|-----------------|
| Lee Filter | Simple adaptive filter based on local statistics. |
| Frost Filter | Distance-weighted adaptive filter with exponential weighting. |
| Kuan Filter | Minimum Mean Square Error (MMSE) filter with reduced estimation bias. |
| Gamma-MAP Filter | Bayesian estimator designed for multiplicative speckle. |
| Refined Lee Filter | Directional adaptive filter with excellent edge preservation. |

All GeoSAR speckle filters operate on **Linear** backscatter values.

Attempting to apply these filters to dB images will raise an informative error.

---

# Choosing the Appropriate Filter

No single filter is optimal for every application.

The choice depends on the analysis objective.

| Application | Recommended Filter |
|-------------|--------------------|
| General-purpose smoothing | Lee |
| Fast preprocessing | Frost |
| Moderate edge preservation | Kuan |
| Bayesian estimation | Gamma-MAP |
| Highest edge preservation | Refined Lee |

For flood mapping and change detection, GeoSAR generally recommends the **Refined Lee Filter**, which provides an excellent balance between noise reduction and preservation of linear features such as rivers, roads, levees, and field boundaries.

---

# Lee Filter

## Overview

The Lee filter is one of the most widely used adaptive speckle filters.

Instead of applying the same amount of smoothing everywhere, it estimates the local statistics within a moving window and determines how strongly each pixel should be smoothed.

In homogeneous regions, stronger smoothing is applied.

Near edges, the original pixel value is preserved to avoid blurring important structures.

### Advantages

- Simple
- Computationally efficient
- Good general-purpose filter
- Preserves major edges

### Limitations

- May blur narrow structures
- Less effective than more advanced directional filters

### GeoSAR Example

```python
import sar

image = sar.db_to_linear(
    sar.load_sar("preflood.tif")
)

filtered = sar.lee_filter(
    image,
    window_size=5,
)
```

---

# Frost Filter

## Overview

The Frost filter assigns weights according to both the local image statistics and the distance from the centre pixel.

Pixels closer to the centre receive larger weights than distant pixels.

The amount of smoothing adapts automatically according to the local variance.

### Advantages

- Better edge preservation than simple averaging
- Flexible through the damping factor
- Effective in moderately heterogeneous regions

### Limitations

- Sensitive to the damping parameter
- Can still blur very fine structures

### GeoSAR Example

```python
filtered = sar.frost_filter(
    image,
    window_size=5,
    damping_factor=2.0,
)
```

---

# Kuan Filter

## Overview

The Kuan filter is another adaptive Minimum Mean Square Error (MMSE) estimator.

It improves upon the Lee filter by reducing estimation bias while maintaining similar computational complexity.

The filter computes an adaptive weighting factor based on the estimated signal and noise variances.

### Advantages

- Reduced estimation bias
- Good radiometric preservation
- Stable performance

### Limitations

- Slightly more computationally expensive than Lee
- Limited directional awareness

### GeoSAR Example

```python
filtered = sar.kuan_filter(
    image,
    window_size=5,
)
```

---

# Gamma-MAP Filter

## Overview

The Gamma Maximum A Posteriori (Gamma-MAP) filter is based on Bayesian estimation.

Rather than treating all pixels identically, it classifies image regions into:

- Homogeneous regions
- Textured regions
- Strong edge regions

Each class is processed using an appropriate statistical model.

### Advantages

- Excellent preservation of textured regions
- Strong statistical foundation
- Suitable for heterogeneous landscapes

### Limitations

- Requires the Equivalent Number of Looks (ENL)
- More computationally intensive

### GeoSAR Example

```python
filtered = sar.gamma_map_filter(
    image,
    window_size=5,
    enl=4,
)
```

---

# Refined Lee Filter

## Overview

The Refined Lee filter is considered one of the most effective adaptive speckle filters for SAR imagery.

Instead of using a single neighbourhood, it estimates the dominant local edge direction and performs smoothing only along that direction.

This directional processing significantly improves edge preservation.

GeoSAR's implementation follows the refined directional filtering approach while remaining fully vectorised for efficient processing.

### Advantages

- Excellent edge preservation
- Preserves narrow linear structures
- Strong performance for flood mapping
- Recommended for change detection

### Limitations

- Higher computational cost
- More complex algorithm

### GeoSAR Example

```python
filtered = sar.refined_lee(
    image,
)
```

---

# Typical Workflow

A common preprocessing workflow is:

```text
Load SAR image (dB)
        │
        ▼
Convert to Linear
        │
        ▼
Apply Speckle Filter
        │
        ▼
Change Detection
Classification
Flood Mapping
Segmentation
        │
        ▼
Convert back to dB
```

Filtering should generally be performed before change detection so that random speckle does not dominate the computed differences.

---

# Best Practices

- Convert SAR images to Linear scale before filtering.
- Use an appropriate window size (typically 5×5 or 7×7).
- Avoid repeated filtering, which may oversmooth the image.
- Choose Refined Lee when preserving edges is important.
- Convert filtered images back to dB for visualization.

---

# Summary

In this chapter, you learned:

- Why SAR images contain speckle.
- Why speckle is multiplicative.
- Why adaptive filtering is necessary.
- The characteristics of the five filters implemented in GeoSAR.
- How to select an appropriate filter for different applications.
- Typical preprocessing workflows for SAR imagery.

---

## What's Next?

Now that you understand how speckle can be reduced while preserving important image features, the next step is to compare SAR images acquired at different times.

Continue with **Change Detection**, where you will learn how GeoSAR identifies changes in radar backscatter using ratio, difference, and logarithmic ratio methods.