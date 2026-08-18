# GeoSAR Architecture

## Overview

GeoSAR is organized as a collection of independent processing modules built around a common data model (`SARImage`). Each module performs one well-defined task while preserving image metadata, valid-data masks, and processing history.

The modular design allows algorithms to be developed, tested, and extended independently before being combined into complete processing pipelines.

---

## Architecture

                        GeoSAR
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Data Model        Processing Modules     Pipelines
        │                  │                  │
        ▼                  ▼                  ▼
    SARImage     Filters, Change Detection   detect_flood()
                  Thresholding, Morphology

---

## Module Responsibilities

| Module | Responsibility |
|---------|----------------|
| sar_image.py | SARImage data model |
| sar_statistics.py | Local statistics |
| sar_conversion.py | dB ↔ Linear conversion |
| sar_filters.py | Speckle filtering |
| sar_change.py | Change detection |
| sar_threshold.py | Thresholding |
| sar_postprocess.py | Morphological processing |
| sar_pipeline.py | End-to-end workflow orchestration |

---

## Data Flow

Sentinel-1 Image

↓

SARImage

↓

Processing Module

↓

SARImage

↓

Processing Module

↓

SARImage

↓

Flood Detection Pipeline

↓

Flood Mask

---

## Design Goals

- Modular architecture
- Reusable algorithms
- Metadata preservation
- Mask preservation
- Scientific reproducibility
- Extensibility