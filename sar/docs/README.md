# GeoSAR

**GeoSAR** is an open-source Python library for Synthetic Aperture Radar (SAR) image processing, designed with an emphasis on modularity, reproducibility, and scientific transparency.

Version 1.0 implements a complete Sentinel-1 flood detection workflow, from radiometric conversion to a validated binary flood mask.

Rather than functioning as a black-box application, GeoSAR exposes every intermediate processing step, enabling researchers, students, and practitioners to inspect, validate, and extend the workflow.

GeoSAR is built around a simple philosophy:

> Build reusable SAR processing components that are scientifically correct, independently testable, and easy to combine into complete workflows.

## Why GeoSAR?

Most SAR processing software provides complete processing pipelines but exposes little of the underlying implementation.

GeoSAR takes a different approach.

Every algorithm is implemented as an independent, reusable component with a consistent API. This allows users to:

- understand each processing step
- validate intermediate results
- replace algorithms easily
- build custom workflows
- reproduce published experiments

The result is a library that is both practical and educational.

                    GeoSAR

                        │

        ┌───────────────┼────────────────┐

        ▼               ▼               ▼

   Image Model      Processing      Pipelines

        │               │               │

        ▼               ▼               ▼

    SARImage      Filters, Change   detect_flood()

                    Thresholding

                    Morphology


## Engineering Principles

GeoSAR follows a consistent engineering philosophy.

Every public function:

- validates its inputs
- preserves metadata
- preserves valid-data masks
- never modifies input objects
- returns a new `SARImage`
- includes NumPy-style documentation
- has unit tests
- has integration tests

These principles ensure that every module behaves consistently throughout the library.

## Validation

GeoSAR has been validated at three levels.

### Unit Testing

Each processing module has dedicated unit tests covering

- functional correctness
- input validation
- edge cases
- mask propagation

### Integration Testing

The complete processing pipeline has been validated against a manually implemented Sentinel-1 workflow.

## Vision

Version 1 establishes the core architecture for SAR image processing.

Future versions will extend GeoSAR into a general-purpose framework supporting

- flood monitoring
- agriculture
- forestry
- land cover analysis
- disaster management
- multi-temporal SAR analysis
- polarimetric SAR

## Philosophy

GeoSAR was developed from first principles.

Every algorithm was implemented, tested, profiled, validated, and integrated before moving to the next component.

This incremental engineering approach has produced a modular and highly testable SAR processing library that can continue to grow without sacrificing code quality.