# GeoSAR

*A modern Python library for Synthetic Aperture Radar (SAR) image processing, change detection, flood mapping, and emerging polarimetric SAR analysis.*

---

## Overview

GeoSAR is an open-source Python library for processing Synthetic Aperture Radar (SAR) imagery. It provides a clean, modular, and well-tested framework for building remote sensing workflows, from loading SAR data and performing radiometric processing to change detection, flood mapping, and polarimetric SAR analysis.

The library currently provides a mature processing workflow for **Sentinel-1 Ground Range Detected (GRD)** imagery, while development is underway to extend GeoSAR to advanced SAR data products, including **NISAR GCOV** and quad-polarization SAR analysis.

GeoSAR includes implementations of commonly used SAR algorithms for:

- SAR image management
- Radiometric conversion
- Local statistical analysis
- Speckle filtering
- Change detection
- Threshold estimation
- Morphological processing
- Flood mapping
- Polarimetric covariance analysis
- Pauli decomposition and RGB visualization

Throughout the processing pipeline, GeoSAR emphasizes **metadata preservation, scientific correctness, reproducibility, modularity, and comprehensive testing**.

GeoSAR is designed for:

- Remote sensing researchers
- Earth Observation scientists
- Disaster management applications
- Geospatial data scientists
- Students learning SAR image processing

---

## Why GeoSAR?

Processing SAR imagery typically requires combining multiple independent tools for:

- Reading raster imagery
- Managing spatial and SAR metadata
- Radiometric conversion
- Speckle reduction
- Statistical analysis
- Change detection
- Threshold estimation
- Morphological post-processing
- Flood mapping
- Polarimetric analysis

GeoSAR integrates these capabilities into a consistent Python package with a clean API and extensive testing.

The library emphasizes:

- **Modular architecture**
- **Scientific reproducibility**
- **Metadata preservation**
- **Readable APIs**
- **Independent algorithm implementation**
- **Comprehensive testing**
- **Validation of intermediate processing results**
- **Extensibility for advanced SAR algorithms**

---

## Supported SAR Data

### Sentinel-1

GeoSAR currently provides a mature workflow for **Sentinel-1 Ground Range Detected (GRD)** imagery, including:

- SAR image abstraction
- Radiometric conversion
- Local statistics
- Speckle filtering
- Change detection
- Automatic thresholding
- Morphological processing
- Flood detection
- Visualization

### NISAR

Development is underway to support **NISAR SAR data products**, with current work focused on **NISAR GCOV** and quad-polarization SAR analysis.

The NISAR work includes exploration and implementation of:

- GCOV product structure and data organization
- Quad-polarization covariance data
- Complex-valued covariance elements
- Hermitian covariance matrix representation
- Covariance channel management
- Pixel-level covariance matrix construction
- Polarimetric analysis
- Pauli decomposition
- Pauli RGB visualization

The NISAR capability is currently **work in progress** and is being developed incrementally with an emphasis on scientific correctness, validation, reusable APIs, and integration with the existing GeoSAR architecture.

---

## Features

### Image Management

- `SARImage` abstraction
- Automatic metadata preservation
- Raster I/O utilities
- Valid-data mask propagation

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

GeoSAR is being extended to support quad-polarization SAR analysis.

Current capabilities include:

- Quad-polarimetric covariance image representation
- Six independent covariance elements of a 3 × 3 Hermitian covariance matrix
- Hermitian counterpart reconstruction using complex conjugation
- Pixel-level complex Hermitian covariance matrix construction
- Covariance channel access
- Pauli decomposition
- Pauli RGB channel generation

The current Pauli representation provides:

- **Red → Double-bounce scattering**
- **Green → Volume scattering**
- **Blue → Surface scattering**

### Visualization

- Image display
- Overlay utilities
- Stretching
- Comparison tools
- Pauli RGB visualization

---

## Design Principles

GeoSAR has been developed around a few core principles:

- **Scientific correctness** over convenience
- **Readable APIs** instead of large monolithic functions
- **Metadata preservation** throughout every processing step
- **Modular design** allowing individual algorithms to be used independently
- **Explicit intermediate representations** for scientific inspection and validation
- **Comprehensive unit testing** to ensure reproducibility and reliability

---

## Current Status

GeoSAR Version **1.0.0**

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
- 300+ automated unit tests
- Ruff-compliant codebase

### In Development

Advanced SAR capabilities are currently being developed, including:

- NISAR GCOV data support
- Quad-polarization SAR analysis
- Hermitian covariance matrix representation
- Polarimetric SAR processing
- Pauli decomposition and RGB visualization
- Multi-temporal SAR analysis

---

## Quick Start

The example below demonstrates a typical flood detection workflow using two Sentinel-1 SAR images.

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

For a complete end-to-end example, see the tutorials in the `examples/` directory.

---

## Polarimetric SAR

GeoSAR is progressively expanding from conventional intensity-based SAR processing toward **quad-polarization SAR analysis**.

The current implementation introduces a dedicated covariance representation for quad-polarimetric data.

A `CovarianceImage` stores the six independent elements of a **3 × 3 Hermitian covariance matrix**, while Hermitian counterparts can be reconstructed using complex conjugation.

This representation provides a foundation for:

- Pixel-level covariance analysis
- Polarimetric feature extraction
- Polarimetric decomposition
- Scattering mechanism analysis
- Pauli RGB visualization
- Future polarimetric processing algorithms

This component is currently under active development and validation.

---

## Highlights

- Modular SAR processing library
- Sentinel-1 GRD processing workflow
- Metadata preserved across processing operations
- Multiple adaptive speckle filters
- Complete flood detection workflow
- Quad-polarization covariance representation
- Hermitian covariance matrix construction
- Pauli decomposition / RGB visualization
- NISAR GCOV processing under development
- 300+ automated unit tests
- Ruff-compliant codebase
- Designed for scientific reproducibility and extensibility

---

## Documentation

Comprehensive documentation is available in the `docs/` directory.

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
- SARImage
- SAR Metadata
- Radiometry
- Statistics
- Filters
- Change Detection
- Thresholding
- Morphology
- Covariance
- Polarimetric Processing
- Visualization

### Developer Guide

- Package Architecture
- Contributing
- Coding Standards
- Testing
- Validation

Example notebooks demonstrating the library are available in the `examples/` directory.

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
│   ├── sar_filters.py
│   ├── sar_flood.py
│   ├── sar_geometry.py
│   ├── sar_image.py
│   ├── sar_io.py
│   ├── sar_metadata.py
│   ├── sar_radiometry.py
│   ├── sar_statistics.py
│   ├── sar_threshold.py
│   └── ...
│
├── docs/
├── README.md
├── ARCHITECTURE.md
├── PROJECT_STATUS.md
├── ROADMAP.md
├── pyproject.toml
└── LICENSE
```

The library follows a modular architecture, allowing each processing stage to be used independently or combined into complete processing pipelines.

---

## Roadmap

GeoSAR is under active development.

### Current Development

- NISAR GCOV support
- Quad-polarization data handling
- Covariance matrix validation
- Polarimetric decomposition
- Pauli RGB visualization
- Expanded validation datasets
- Additional scientific test cases

### Future Releases

#### Version 1.1

- Additional adaptive speckle filters
- Performance optimization
- Improved visualization tools
- Expanded example datasets
- Enhanced NISAR support

#### Version 2.0

- Advanced Polarimetric SAR (PolSAR)
- Interferometric SAR (InSAR)
- Multi-temporal change detection
- Time-series analysis
- Extended NISAR product support
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
