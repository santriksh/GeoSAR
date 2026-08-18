from __future__ import annotations

from .flood import detect_flood
from .models import (
    FloodResult,
    FloodStatistics,
)

__all__ = [
    "FloodResult",
    "FloodStatistics",
    "detect_flood",
]

