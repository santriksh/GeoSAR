import numpy as np
import rasterio

from .sar_image import SARImage
from .sar_metadata import (
    AcquisitionMetadata,
    CustomMetadata,
    ProcessingMetadata,
    ProvenanceMetadata,
    SARMetadata,
    SpatialMetadata,
)


def load_sar(path:str,acquisition:AcquisitionMetadata | None = None,):
    with rasterio.open(path) as src:
    
        image = src.read(1)
    
        #mask = ~np.isnan(image)
        mask = np.isfinite(image)
    
        spatial = SpatialMetadata(
            crs=src.crs,
            transform=src.transform,
            bounds=src.bounds,
            resolution=src.res,
            shape=image.shape
        )
    
        # acquisition = AcquisitionMetadata(
        #    platform="Sentinel-1",
        #    sensor="SAR"
        # )

        if acquisition is None:

            acquisition = AcquisitionMetadata()
    
        processing = ProcessingMetadata(
            product_type=src.profile.get("driver", ""),
            processing_level="GRD",
            value_scale="dB"
        )
    
        provenance = ProvenanceMetadata(
            operation="load_sar",
            inputs=[path]
        )
    
        metadata = SARMetadata(
            spatial=spatial,
            acquisition=acquisition,
            processing=processing,
            provenance=provenance,
            custom=CustomMetadata()
        )
    
        return SARImage(
            data=image,
            mask=mask,
            metadata=metadata
        )