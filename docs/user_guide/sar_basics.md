# SAR Basics

This chapter introduces the fundamental concepts of Synthetic Aperture Radar (SAR) required to understand the GeoSAR processing workflow.

No prior knowledge of radar remote sensing is assumed.

By the end of this chapter you will understand:

- What Synthetic Aperture Radar is
- Why SAR is different from optical imagery
- How SAR images are formed
- Why speckle appears in SAR images
- Why flooded areas appear dark
- Why GeoSAR performs each processing step

---

# What is Synthetic Aperture Radar?

Synthetic Aperture Radar (SAR) is an active microwave imaging system.

Unlike optical satellites, which record reflected sunlight, SAR systems actively transmit microwave pulses toward the Earth's surface and measure the returning echoes.

Because the satellite provides its own illumination, SAR imagery can be acquired:

- During the day
- At night
- Through clouds
- During rain
- During haze or smoke

This makes SAR particularly valuable for disaster monitoring and emergency response.

---

# How SAR Differs from Optical Images

| Optical Images | SAR Images |
|---------------|------------|
| Passive sensor | Active sensor |
| Uses sunlight | Transmits microwave energy |
| Affected by clouds | Penetrates clouds |
| Daytime only | Day and night |
| Natural-looking images | Radar backscatter images |

For flood monitoring, this capability is especially important because floods often occur during periods of heavy rainfall when optical imagery is unavailable.

---

# How a SAR Image is Formed

A SAR satellite repeatedly performs the following sequence:

1. Transmit a microwave pulse.
2. The pulse interacts with the Earth's surface.
3. A portion of the energy is scattered back toward the satellite.
4. The satellite records the returned signal.
5. Millions of measurements are combined to produce a radar image.

Each pixel in a SAR image represents the amount of microwave energy returned from a small area on the Earth's surface.

This returned energy is known as **backscatter**.

---

# Understanding Backscatter

Different surfaces reflect microwave energy differently.

| Surface | Typical Backscatter |
|----------|---------------------|
| Calm water | Very low |
| Dense forest | High |
| Urban buildings | Very high |
| Agricultural fields | Moderate |

Smooth water surfaces reflect most of the radar energy away from the satellite, producing dark pixels.

Rough surfaces scatter energy in many directions, increasing the amount of energy returned to the sensor and producing brighter pixels.

This difference in backscatter makes SAR particularly effective for identifying flooded areas.

---

# Why Flooded Areas Look Dark

Before flooding:

- Vegetation
- Soil
- Roads

scatter radar energy back toward the sensor.

After flooding:

- Water creates a smooth reflecting surface.
- Most of the radar energy is reflected away from the satellite.
- Very little energy returns.

As a result, flooded regions typically appear darker than the surrounding land.

This contrast forms the basis of many SAR-based flood detection algorithms.

---

# What is Speckle?

One characteristic of SAR imagery is **speckle**.

Speckle appears as a grainy texture throughout the image.

Unlike random sensor noise, speckle is an inherent property of coherent radar imaging.

It is caused by the constructive and destructive interference of microwave signals reflected from many small scatterers within a single image pixel.

Although speckle contains useful statistical information, it can make interpretation and change detection more difficult.

GeoSAR provides several adaptive filters to reduce speckle while preserving important image features.

---

# Why GeoSAR Converts dB to Linear Scale

SAR imagery is commonly distributed in decibel (dB) units because logarithmic values are easier to visualize.

However, many physical models and adaptive speckle filters assume linear backscatter values.

For this reason, GeoSAR converts images from dB to Linear scale before applying most filtering algorithms.

---

# Typical GeoSAR Workflow

The standard GeoSAR flood detection workflow is shown below.

```text
Sentinel-1 Images
        │
        ▼
Load Images
        │
        ▼
Convert dB → Linear
        │
        ▼
Refined Lee Filter
        │
        ▼
Log-Ratio Change Detection
        │
        ▼
Automatic Threshold
        │
        ▼
Morphological Processing
        │
        ▼
Flood Map
```

Each step addresses a specific challenge:

| Step | Purpose |
|------|---------|
| Load Images | Read raster data and metadata |
| dB → Linear | Prepare data for physical processing |
| Speckle Filter | Reduce multiplicative noise |
| Change Detection | Identify significant backscatter changes |
| Thresholding | Separate flooded and non-flooded pixels |
| Morphology | Remove isolated artifacts |

---

# Summary

In this chapter you learned:

- What SAR is
- How SAR differs from optical imagery
- How radar images are formed
- What backscatter represents
- Why flooded regions appear dark
- Why speckle occurs
- Why GeoSAR converts images to Linear scale
- The overall GeoSAR processing workflow

These concepts provide the foundation for the remaining chapters in the User Guide.

---

# Next Steps

Continue with:

**Radiometric Processing**

The next chapter explains SAR backscatter measurements, decibel and linear scales, and why radiometric conversion is an essential step in GeoSAR workflows.