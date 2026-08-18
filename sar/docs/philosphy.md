# GeoSAR Philosophy

GeoSAR was developed around one central idea:

> Every SAR processing algorithm should be understandable, reusable, independently testable, and scientifically reproducible.

---

## Core Principles

### Modularity

Each processing step solves one problem.

### Consistency

Every function:

- validates inputs
- preserves metadata
- preserves masks
- returns a new SARImage

### Reproducibility

Every algorithm is validated through:

- Unit Tests
- Edge Cases
- Integration Tests
- Real Sentinel-1 Imagery

### Transparency

Every intermediate processing step remains accessible.

Users can inspect:

- filtered images
- change images
- threshold values
- morphology outputs

### Extensibility

New algorithms should integrate naturally into the existing architecture without modifying existing modules.

---

## Why SARImage?

SARImage serves as the common data model throughout GeoSAR.

It keeps:

- image data
- metadata
- CRS
- affine transform
- masks
- processing history

together throughout the processing pipeline.

---

## Engineering Philosophy

Understanding comes before automation.

GeoSAR is designed not only to produce results but also to help users understand every stage of SAR image processing.