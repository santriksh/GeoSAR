from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SpatialMetadata:

    crs: object

    transform: object

    bounds: object

    resolution: tuple

    shape: tuple

    def as_dict(self):
        return {
            "crs": str(self.crs),
            "transform": self.transform,
            "bounds": self.bounds,
            "resolution": self.resolution,
            "shape": self.shape,
        }

@dataclass
class AcquisitionMetadata:

    platform: str = ""

    sensor: str = ""

    acquisition_date: str = ""

    polarization: str = ""

    orbit_direction: str = ""

    relative_orbit: int | None = None

    beam_mode: str = ""

    frequency_band: str = ""

    incidence_angle: str = ""

    def as_dict(self):

        return {

            "platform": self.platform,

            "sensor": self.sensor,

            "acquisition_date": self.acquisition_date,

            "polarization": self.polarization,

            "orbit_direction": self.orbit_direction,

            "relative_orbit": self.relative_orbit,

            "beam_mode": self.beam_mode,

            "frequency_band": self.frequency_band,

            "incidence_angle": self.incidence_angle,
        }

@dataclass
class ProcessingMetadata:

    processing_level: str = ""

    product_type: str = ""

    value_scale: str = "dB"

    software: str = ""

    calibration: str = ""

    terrain_corrected: bool = False

    speckle_filtered: bool = False

    def as_dict(self):

        return {

        "processing_level": self.processing_level,

        "product_type": self.product_type,

        #"radiometric_calibration": self.radiometric_calibration,

        "terrain_corrected": self.terrain_corrected,

        "speckle_filtered": self.speckle_filtered,

        "software": self.software,

        #"software_version": self.software_version,
    }

@dataclass
class ProvenanceMetadata:

    operation: str = ""

    inputs: list = field(default_factory=list)

    parameters: dict = field(default_factory=dict)

    created_by: str = "GeoSAR"

    version: str = "0.1"

    def as_dict(self):

        return {

        "operation": self.operation,

        "inputs": self.inputs,

        "parameters": self.parameters,

        "created_by": self.created_by,

        "version": self.version,
    }


@dataclass
class CustomMetadata:
    """
    User-defined metadata.
    """

    values: dict[str, Any] = field(default_factory=dict)

    def as_dict(self):

        return self.values

@dataclass
class SARMetadata:

    spatial: SpatialMetadata

    acquisition: AcquisitionMetadata

    processing: ProcessingMetadata

    provenance: ProvenanceMetadata

    custom: CustomMetadata