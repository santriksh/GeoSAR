# GeoSAR

*A modern Python library for Synthetic Aperture Radar (SAR) image processing, change detection, flood mapping, and emerging polarimetric SAR analysis.*

---

## Overview

GeoSAR is an open-source Python library for processing **Synthetic Aperture Radar (SAR)** imagery. It provides a clean, modular, and well-tested framework for developing remote sensing workflows, from SAR image management and radiometric processing to speckle filtering, change detection, flood mapping, and polarimetric SAR analysis.

The current GeoSAR release provides a mature processing workflow for **Sentinel-1 Ground Range Detected (GRD)** imagery and flood detection.

In parallel, GeoSAR is being extended toward advanced SAR capabilities, including **NISAR GCOV and quad-polarization SAR analysis**.

The project emphasizes:

- Scientific correctness
- Modular and reusable algorithms
- Metadata preservation
- Explicit intermediate processing steps
- Reproducibility
- Comprehensive testing
- Extensible software architecture

GeoSAR is designed for:

- Remote sensing researchers
- Earth Observation scientists
- Disaster management applications
- Geospatial data scientists
- Students learning SAR image processing

---

## Why GeoSAR?

SAR processing often requires combining multiple independent tools for:

- Reading raster imagery
- Managing spatial and SAR metadata
- Radiometric conversion
- Speckle reduction
- Local statistical analysis
- Change detection
- Threshold estimation
- Morphological processing
- Flood mapping
- Polarimetric analysis

GeoSAR brings these capabilities together in a consistent Python framework with a clean API.

Unlike a black-box processing application, GeoSAR exposes the individual processing stages so that intermediate results can be inspected, validated, tested, and reused.

The library follows the philosophy:

> **Build reusable SAR processing components that are scientifically correct, independently testable, and easy to combine into complete workflows.**

---

## Supported SAR Data

### Sentinel-1

GeoSAR currently provides a mature workflow for **Sentinel-1 Ground Range Detected (GRD)** imagery.

The Sentinel-1 workflow includes:

- SAR image abstraction
- Metadata management
- Radiometric conversion
- Local statistical analysis
- Speckle filtering
- Change detection
- Automatic thresholding
- Morphological processing
- Flood detection
- Visualization

---

### NISAR — Work in Progress

GeoSAR is being progressively extended toward **NISAR SAR data products**, with current development focused on **GCOV and quad-polarization SAR data representation and analysis**.

The current work establishes the foundation for handling polarimetric covariance information, including:

- Quad-polarization covariance data representation
- Six independent elements of a 3 × 3 Hermitian covariance matrix
- Covariance channel management
- Reconstruction of Hermitian counterpart channels using complex conjugation
- Pixel-level 3 × 3 complex Hermitian covariance matrix construction
- Polarimetric covariance analysis
- Pauli decomposition
- Pauli RGB visualization

The NISAR capability is currently **under active development and validation**. The current implementation focuses on establishing scientifically correct data representations and reusable processing components before building a complete end-to-end NISAR processing workflow.

---

## Features

### Image Management

- `SARImage` abstraction
- Metadata preservation
- Raster I/O utilities
- Valid-data mask propagation
- Non-destructive processing operations

### Radiometric Processing

- dB → Linear conversion
- Linear → dB conversion

### Local Statistics

- Local mean
- Local variance
- Local standard deviation
- Coefficient of variation
- Equivalent Number of Looks (ENL)
- Local noise variance estimation

### Speckle Filtering

- Mean Filter
- Lee Filter
- Frost Filter
- Kuan Filter
- Gamma-MAP Filter
- Refined Lee Filter

### Change Detection

- Difference
- Ratio
- Log-Ratio

### Thresholding

- Otsu Threshold

### Morphological Processing

- Binary Opening
- Binary Closing
- Connected Components
- Small Object Removal

### Flood Detection

- Binary flood mask generation
- Flood statistics
- End-to-end flood detection workflow

### Polarimetric SAR — Work in Progress

GeoSAR is being extended from conventional intensity-based SAR processing toward **quad-polarization SAR analysis**.

Current polarimetric capabilities include:

- `CovarianceImage` representation
- Six independent covariance elements
- Hermitian covariance reconstruction
- Pixel-level complex covariance matrix construction
- Covariance channel access
- Polarimetric feature processing
- Pauli decomposition
- Pauli RGB generation

The covariance representation is based on a **3 × 3 Hermitian covariance matrix**, with the remaining matrix elements reconstructed through complex conjugation.

Pauli RGB visualization currently represents:

- **Red → Double-bounce scattering**
- **Green → Volume scattering**
- **Blue → Surface scattering**

This functionality forms the foundation for further Polarimetric SAR and NISAR GCOV development.

---

## Design Principles

GeoSAR has been developed around several core principles.

### Scientific Correctness

Algorithms are implemented with explicit attention to the underlying SAR and image-processing mathematics rather than treating processing as a black-box operation.

### Modular Architecture

Individual algorithms and processing stages can be used independently or combined into complete workflows.

### Metadata Preservation

Spatial and image metadata are preserved throughout processing operations wherever applicable.

### Non-Destructive Processing

Processing operations return new image objects rather than modifying the original input data.

### Explicit Intermediate Representations

Intermediate processing results remain accessible, making it possible to inspect and validate individual stages.

### Comprehensive Testing

Processing components are developed with unit and integration testing to improve reliability and reproducibility.

---

## Current Status

**GeoSAR Version 1.0.0**

### Stable / Implemented

The current Sentinel-1 processing framework includes:

- SAR image abstraction
- Radiometric processing
- Local statistical analysis
- Multiple speckle filters
- Change detection
- Otsu thresholding
- Morphological processing
- Flood detection workflow
- Visualization
- Comprehensive automated testing
- Ruff-compliant codebase

### In Development

Advanced SAR capabilities are being developed incrementally:

- NISAR GCOV data handling
- Quad-polarization SAR representation
- Covariance matrix analysis
- Hermitian covariance matrix construction
- Polarimetric SAR processing
- Pauli decomposition
- Pauli RGB visualization
- Multi-temporal SAR analysis

---

## Quick Start

The following example demonstrates a typical Sentinel-1 flood detection workflow using two SAR images.

```python
import sar

# Load Sentinel-1 images
pre = sar.load_sar("pre_flood.tif")
post = sar.load_sar("post_flood.tif")

# Convert from dB to Linear scale
pre = sar.db_to_linear(pre)
post = sar.db_to_linear(post)

# Reduce speckle noise
pre = sar.refined_lee(pre)
post = sar.refined_lee(post)

# Compute log-ratio change image
change = sar.log_ratio_change(pre, post)

# Estimate threshold automatically
threshold = sar.otsu_threshold(change)

# Generate flood mask
flood = sar.threshold_flood(
    change,
    threshold=threshold,
    direction="less",
)

# Remove small isolated objects
flood = sar.binary_opening(flood)
flood = sar.binary_closing(flood)

flood = sar.remove_small_objects(
    flood,
    min_size=20,
)

# Display results
flood.show()
```

The complete workflow consists of:

1. Loading SAR images
2. Radiometric conversion
3. Speckle filtering
4. Change detection
5. Automatic threshold estimation
6. Morphological post-processing
7. Flood map visualization

For complete examples, see the `examples/` and `notebooks/` directories.

---

## Polarimetric SAR

One of the current development directions of GeoSAR is extending the library toward **quad-polarization SAR and polarimetric analysis**.

The `CovarianceImage` abstraction represents the independent elements of a **3 × 3 complex Hermitian covariance matrix**.

Only the six independent covariance channels need to be stored:

```text
        ┌                         ┐
        │ HHHH    HHHV    HHVV   │
        │                         │
C  =    │ HHHV*   HVHV    HVVV   │
        │                         │
        │ HHVV*   HVVV*   VVVV   │
        └                         ┘
```

The Hermitian counterpart channels are reconstructed using complex conjugation.

This representation provides a foundation for:

- Pixel-level covariance analysis
- Polarimetric feature extraction
- Scattering mechanism analysis
- Polarimetric decomposition
- Pauli RGB visualization
- Future PolSAR processing algorithms
- NISAR GCOV integration

### Pauli Decomposition

GeoSAR currently provides Pauli RGB generation from covariance elements.

The resulting channels represent:

| Channel | Scattering mechanism |
|---|---|
| Red | Double-bounce |
| Green | Volume |
| Blue | Surface |

The implementation is currently being validated and will form part of the broader polarimetric SAR processing framework.

---

## Validation and Testing

GeoSAR places strong emphasis on validation and software quality.

### Unit Testing

Processing components are tested for:

- Functional correctness
- Input validation
- Edge cases
- Metadata preservation
- Mask propagation
- Numerical behavior

### Integration Testing

Complete processing workflows are tested to ensure that individual components work correctly when combined.

The Sentinel-1 flood-detection workflow has been validated against an independently implemented processing workflow.

---

## Highlights

- Modular Python SAR processing library
- Sentinel-1 GRD processing workflow
- SAR radiometric processing
- Six adaptive speckle-filtering approaches
- SAR change detection
- Automatic thresholding
- Morphological processing
- End-to-end flood detection
- Quad-polarization covariance representation
- Complex Hermitian covariance matrix construction
- Pauli decomposition and RGB visualization
- NISAR GCOV capability under active development
- Comprehensive automated testing
- Ruff-compliant codebase
- Scientific and reproducible design philosophy

---

## Documentation

Documentation is available in the `docs/` directory.

### Getting Started

- Installation Guide
- Quick Start
- First Flood Detection Workflow

### User Guide

- SAR Fundamentals
- Radiometric Processing
- Local Statistics
- Speckle Filtering
- Change Detection
- Thresholding
- Morphological Processing
- Flood Detection
- Polarimetric SAR

### API Reference

- Image I/O
- `SARImage`
- SAR Metadata
- Radiometry
- Statistics
- Filters
- Change Detection
- Thresholding
- Morphology
- Covariance
- Polarimetric Features
- Visualization

### Developer Guide

- Package Architecture
- Coding Standards
- Testing
- Validation
- Contributing

---

## Project Structure

```text
GeoSAR/
│
├── sar/
│   ├── benchmarks/
│   ├── constants/
│   ├── debug/
│   ├── docs/
│   ├── examples/
│   ├── features/
│   ├── filters/
│   ├── io/
│   ├── models/
│   ├── morphology/
│   ├── notebooks/
│   ├── pipeline/
│   ├── plotting/
│   ├── processing/
│   ├── readers/
│   ├── tests/
│   ├── validation/
│   ├── visualization/
│   ├── covariance.py
│   ├── sar_change.py
│   ├── sar_collection.py
│   ├── sar_filters.py
│   ├── sar_flood.py
│   ├── sar_geometry.py
│   ├── sar_image.py
│   ├── sar_io.py
│   ├── sar_metadata.py
│   ├── sar_metadata_loader.py
│   ├── sar_operations.py
│   ├── sar_radiometry.py
│   ├── sar_statistics.py
│   └── sar_threshold.py
│
├── docs/
├── ARCHITECTURE.md
├── PROJECT_STATUS.md
├── ROADMAP.md
├── README.md
├── pyproject.toml
└── LICENSE
```

The library follows a modular architecture in which individual processing stages can be used independently or combined into complete SAR processing pipelines.

---

## Roadmap

GeoSAR is under active development.

### Near-Term Development

- NISAR GCOV data ingestion and validation
- Expanded quad-polarization data handling
- Covariance matrix validation
- Polarimetric decomposition
- Pauli RGB visualization improvements
- Expanded scientific validation datasets
- Additional numerical and integration tests

### Future Development

- Advanced Polarimetric SAR (PolSAR)
- Interferometric SAR (InSAR)
- Multi-temporal change detection
- SAR time-series analysis
- Extended NISAR product support
- Performance optimization
- GPU acceleration

---

## Contributing

Contributions are welcome.

Whether you are fixing bugs, improving documentation, adding tests, or implementing new algorithms, your contributions are appreciated.

Please read the Developer Guide before submitting pull requests.

---

## License

GeoSAR is released under the MIT License.

See the `LICENSE` file for details.

---

## Citation

If GeoSAR contributes to your research, please cite the project.

Citation information will be provided in a future release.
