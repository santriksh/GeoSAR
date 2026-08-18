# GeoSAR Architecture

## Overview

GeoSAR is a modular Python library for Synthetic Aperture Radar (SAR) image processing with an initial focus on flood detection.

The design follows a layered architecture in which each package has a single responsibility.

```
                +----------------------+
                |     Applications     |
                | Assam Flood Example  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Flood Pipeline     |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
   Morphology                     Visualization
          |                                 |
          +----------------+----------------+
                           |
                           v
                     Feature Extraction
                           |
                           v
                     SAR Filtering
                           |
                           v
                  Radiometry / I/O
                           |
                           v
                        SARImage
```

---

## Core Object

Everything in GeoSAR revolves around the `SARImage` class.

It encapsulates:

- Image data
- Valid pixel mask
- Metadata

All algorithms consume and return `SARImage` objects.