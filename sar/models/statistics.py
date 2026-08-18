
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NeighborhoodStatistics:
    mean: float
    variance: float
    noise_variance: float