"""
GeoSAR
=======

A Python library for Synthetic Aperture Radar (SAR) processing.

This module exposes the stable public API for GeoSAR.
"""

__version__ = "1.0.0"
__author__ = "Santosh Kumar Singh"
__license__ = "MIT"

#
# Core I/O
#
#
# Filters
#
from .filters.refined_lee_geosar import refined_lee

#
# Processing Pipelines
#
from .pipeline.flood import detect_flood

#
# Change Detection
#
from .sar_change import (
    difference_change,
    ratio_change,
)
from .sar_io import load_sar

__all__ = [
    "__author__",
    "__license__",
    "__version__",
    "detect_flood",
    "difference_change",
    "load_sar",
    "ratio_change",
    "refined_lee",
]