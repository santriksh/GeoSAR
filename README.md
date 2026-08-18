# GeoSAR

*A modern Python library for Synthetic Aperture Radar (SAR) image processing, change detection, and flood mapping.*

---

## Overview

GeoSAR is an open-source Python library for processing Synthetic Aperture Radar (SAR) imagery. It provides a clean, modular, and well-tested framework for building remote sensing workflows, from loading SAR data to generating flood maps.

The library includes implementations of commonly used SAR algorithms for radiometric conversion, speckle filtering, change detection, thresholding, and morphological processing, while preserving image metadata throughout the processing pipeline.

GeoSAR is designed for:

- Remote sensing researchers
- Earth Observation scientists
- Disaster management applications
- Geospatial data scientists
- Students learning SAR image processing

Although the current release focuses on Sentinel-1 Ground Range Detected (GRD) imagery and flood detection, the architecture has been designed to support future extensions such as multi-temporal analysis, Polarimetric SAR (PolSAR), Interferometric SAR (InSAR), and NISAR data products.

---

## Why GeoSAR?

Processing SAR imagery typically requires combining multiple independent tools for:

- Reading raster imagery
- Managing spatial metadata
- Radiometric conversion
- Speckle reduction
- Change detection
- Threshold estimation
- Morphological post-processing
- Flood mapping

GeoSAR integrates these capabilities into a single, consistent Python package with a clean API and extensive unit testing.

The library emphasizes:

- Modular architecture
- Scientific reproducibility
- Metadata preservation
- Readable APIs
- Comprehensive testing
- Extensibility for future SAR algorithms

---

## Features

### Image Management

- SARImage abstraction
- Automatic metadata preservation
- Raster I/O utilities

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

### Visualization

- Image display
- Overlay utilities
- Stretching
- Comparison tools

---

## Design Principles

GeoSAR has been developed around a few core principles:

- **Scientific correctness** over convenience
- **Readable APIs** instead of large monolithic functions
- **Metadata preservation** throughout every processing step
- **Modular design** allowing individual algorithms to be used independently
- **Comprehensive unit testing** to ensure reproducibility and reliability

---

## Current Status

GeoSAR Version **1.0.0**

Current release includes:

- SAR image abstraction
- Radiometric processing
- Speckle filtering
- Change detection
- Flood detection workflow
- 300+ automated unit tests
- Fully Ruff-compliant codebase


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


## Highlights

- Modular SAR processing library
- Metadata preserved across every operation
- Consistent `SARImage` abstraction
- Multiple adaptive speckle filters
- Complete flood detection workflow
- 306 automated unit tests
- Ruff-compliant codebase
- Designed for extensibility and research

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
- Speckle Filtering
- Change Detection
- Thresholding
- Morphological Processing

### API Reference

- Image I/O
- SARImage
- Radiometry
- Filters
- Change Detection
- Thresholding
- Morphology
- Visualization

### Developer Guide

- Package Architecture
- Contributing
- Coding Standards
- Testing

Example notebooks demonstrating the library are available in the `examples/` directory.

---

## Project Structure

```text
GeoSAR/
│
├── sar/
│   ├── filters/
│   ├── morphology/
│   ├── visualization/
│   ├── pipeline/
│   ├── examples/
│   ├── tests/
│   ├── sar_image.py
│   ├── sar_io.py
│   ├── sar_change.py
│   └── ...
│
├── docs/
├── README.md
├── pyproject.toml
└── LICENSE
```

The library follows a modular architecture, allowing each processing stage to be used independently or combined into complete processing pipelines.

---

## Roadmap

GeoSAR is under active development.

Future releases are expected to include:

### Version 1.1

- Additional adaptive speckle filters
- Performance optimization
- Improved visualization tools
- Expanded example datasets

### Version 2.0

- Polarimetric SAR (PolSAR)
- Interferometric SAR (InSAR)
- Multi-temporal change detection
- Time-series analysis
- NISAR support
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