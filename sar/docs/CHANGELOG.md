# Changelog

All notable changes to GeoSAR will be documented in this file.

The project follows Semantic Versioning.

---

# Version 1.0.0

Release Date: June 2026

## Added

### Core

- SARImage data model
- Metadata preservation
- Valid-data mask propagation
- Processing history

### Statistics

- Local Mean
- Local Variance
- Equivalent Number of Looks (ENL)

### Radiometric Processing

- dB → Linear conversion
- Linear → dB conversion

### Speckle Filtering

- Lee Filter
- Frost Filter

### Change Detection

- Ratio Change
- Log-Ratio Change
- Difference Image

### Thresholding

- Otsu Thresholding
- Binary Flood Classification

### Morphological Processing

- Binary Opening
- Binary Closing
- Connected Component Labeling
- Remove Small Objects

### Pipeline

- End-to-End Flood Detection (`detect_flood()`)

### Documentation

- README
- Architecture Guide
- Philosophy
- Developer Guide
- Coding Standards
- Release Notes

### Examples

- Assam Flood Detection Example

### Testing

- Unit Tests
- Integration Tests
- Pipeline Validation

---

## Validation

The complete pipeline was validated against the manually implemented Sentinel-1 workflow.

```
Manual Pipeline : 4,084,999 pixels

Pipeline API    : 4,084,999 pixels

Difference      : 0 pixels
```

---

## First Stable Release

GeoSAR Version 1.0 establishes the core architecture for modular SAR image processing and flood detection.

Future versions will extend the library with additional SAR processing capabilities while preserving backward compatibility whenever possible.
