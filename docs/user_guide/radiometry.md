# Radiometry

## Introduction

Radiometry describes how the strength of the radar signal returned from the Earth's surface is represented and processed.

When a Synthetic Aperture Radar (SAR) sensor transmits a microwave pulse, part of the energy is reflected back toward the satellite. The amount of returned energy depends on several factors, including:

- Surface roughness
- Soil moisture
- Vegetation
- Water bodies
- Radar wavelength
- Incidence angle

The returned signal is called **backscatter**. Radiometric processing focuses on representing, comparing, and transforming these backscatter values in a physically meaningful way.

Unlike optical imagery, SAR images measure microwave energy rather than reflected sunlight. This allows SAR to operate day and night and through cloud cover, making radiometric interpretation an essential part of SAR analysis.

---

## SAR Backscatter

Every pixel in a SAR image stores a measurement of the reflected radar energy from a small area on the ground.

Typical interpretation:

| Surface | Typical Backscatter |
|----------|--------------------|
| Calm water | Very low |
| Smooth roads | Low |
| Agricultural fields | Moderate |
| Forest | Moderate to High |
| Urban areas | High |

A lower backscatter value generally indicates that most of the radar energy was reflected away from the sensor, while higher values indicate stronger reflections toward the radar.

!!! note

    Backscatter values depend on the radar sensor, wavelength, polarization, incidence angle, terrain, and environmental conditions. They should always be interpreted in the context of the specific dataset rather than as fixed absolute values.

---

## Linear vs dB Scale

SAR backscatter can be represented in two different ways:

- **Linear scale**
- **Decibel (dB) scale**

Both representations contain the same physical information but are useful for different tasks.

### Linear Scale

In the linear scale, each pixel represents the measured radar power directly. The values are proportional to the amount of microwave energy returned to the radar sensor.

Illustrative example:

| Surface | Linear Backscatter |
|----------|------------------:|
| Calm water | 0.01 |
| Wet soil | 0.08 |
| Vegetation | 0.20 |
| Urban area | 0.75 |

These values are illustrative only and should not be interpreted as universal physical values.

The linear representation preserves the physical relationships between measurements and is therefore required by many SAR processing algorithms.

For example, the Lee, Frost, Kuan, Gamma-MAP, and Refined Lee filters all assume that the input image represents radar power in the linear domain.

### Decibel (dB) Scale

Because radar backscatter often spans several orders of magnitude, it is commonly expressed on the logarithmic decibel scale.

The conversion is

\\[
\mathrm{dB}=10\log_{10}(\mathrm{Linear})
\\]

Illustrative values:

| Linear | dB |
|--------:|---:|
| 1.00 | 0 dB |
| 0.50 | -3 dB |
| 0.10 | -10 dB |
| 0.01 | -20 dB |

The logarithmic transformation compresses the dynamic range, making SAR images much easier to visualize and interpret.

---

## Why Both Scales Are Important

Different SAR operations require different value representations.

| Task | Recommended Scale |
|------|-------------------|
| Visualization | dB |
| Human interpretation | dB |
| Speckle filtering | Linear |
| Physical calculations | Linear |
| Statistical analysis | Linear |

GeoSAR follows this convention throughout the library.

Several functions automatically validate the input scale and raise informative errors when an incorrect representation is supplied.

---

## Radiometric Operations in GeoSAR

GeoSAR provides several fundamental radiometric operations that form the basis for many SAR processing workflows.

| Function | Purpose |
|----------|---------|
| `db_to_linear()` | Convert a SAR image from dB to linear power. |
| `linear_to_db()` | Convert a SAR image from linear power to dB. |
| `difference()` | Compute the pixel-wise difference between two aligned SAR images. |
| `ratio()` | Compute the linear backscatter ratio between two aligned SAR images. |

These operations form the foundation for more advanced processing such as speckle filtering and change detection.

---

## Converting from dB to Linear

Many SAR processing algorithms operate on linear backscatter values.

GeoSAR provides the `db_to_linear()` function for this conversion.

```python
import sar

image_db = sar.load_sar("preflood.tif")

image_linear = sar.db_to_linear(image_db)
```

Internally, the conversion is

\\[
\mathrm{Linear}=10^{\frac{\mathrm{dB}}{10}}
\\]

The returned image preserves the spatial metadata and validity mask while updating the metadata to indicate that the image is now represented in the linear domain.

---

## Converting from Linear to dB

After processing has been completed in the linear domain, the results are commonly converted back to decibel units for visualization.

```python
image_db = sar.linear_to_db(image_linear)
```

Internally, the conversion is

\\[
\mathrm{dB}=10\log_{10}(\mathrm{Linear})
\\]

Pixels with non-positive values cannot be represented in the logarithmic domain. GeoSAR automatically marks these pixels as invalid in the output image.

---

## Difference Image

A difference image measures the absolute change in backscatter between two aligned SAR acquisitions.

\[
Difference = I_{after}-I_{before}
\]

```python
difference = sar.difference(
    before,
    after,
)
```

Difference images are simple to compute and are useful for identifying areas where large absolute changes have occurred.

---

## Ratio Image

A ratio image measures the relative change in radar backscatter.

\[
Ratio=\frac{I_{after}}{I_{before}}
\]

```python
ratio = sar.ratio(
    before,
    after,
)
```

Ratio images are widely used for SAR change detection because they emphasize proportional changes while reducing the influence of overall scene brightness.

---

## Choosing the Appropriate Operation

| Objective | Recommended Operation |
|-----------|-----------------------|
| Prepare images for SAR filtering | `db_to_linear()` |
| Visualize processed images | `linear_to_db()` |
| Measure absolute change | `difference()` |
| Measure relative change | `ratio()` |

GeoSAR validates that the two input images have identical dimensions, coordinate reference systems, affine transforms, and pixel alignment before performing pixel-wise operations.

---

## Typical Workflow

```text
Load SAR image (dB)
        │
        ▼
Convert to Linear
        │
        ▼
Apply SAR Processing
        │
        ▼
Convert back to dB
        │
        ▼
Visualize or Export
```

---

## Best Practices

- Perform speckle filtering in the linear domain.
- Use dB values for visualization and interpretation.
- Ensure images are spatially aligned before comparing them.
- Choose ratio images when relative changes are more important than absolute differences.

---

## Summary

In this chapter, you learned:

- What SAR backscatter represents.
- Why SAR images use both linear and dB scales.
- When each representation should be used.
- How GeoSAR converts between the two scales.
- How to compute difference and ratio images.
- Why image alignment is essential before comparing SAR acquisitions.

The next chapter introduces **Speckle Filtering**, where we explore why SAR images contain speckle noise and how adaptive filters reduce it while preserving important image features.