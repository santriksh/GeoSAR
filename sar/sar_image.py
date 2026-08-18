"""
sar_image.py

Core SARImage class used throughout GeoSAR.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .sar_metadata import SARMetadata


@dataclass
class SARImage:
    """
    Represents a single SAR raster together with
    its metadata and validity mask.
    """

    data: np.ndarray

    mask: np.ndarray

    metadata: SARMetadata

    def statistics(self) -> dict[str, Any]:
        """
        Compute basic statistics of valid pixels.
        """
    
        valid = self.valid_pixels
    
        return {
    
            "minimum": float(np.min(valid)),
    
            "maximum": float(np.max(valid)),
    
            "mean": float(np.mean(valid)),
    
            "median": float(np.median(valid)),
    
            "std": float(np.std(valid)),
    
            "valid_pixels": int(self.mask.sum()),
    
            "nodata_pixels": int((~self.mask).sum()),
    
            "nan_percentage":
                100.0 * (~self.mask).sum() / self.mask.size,
        }


    #def summary(self):
    def as_dict(self):

        return {

        "spatial": self.metadata.spatial.as_dict(),

        "acquisition": self.metadata.acquisition.as_dict(),

        "processing": self.metadata.processing.as_dict(),

        "provenance": self.metadata.provenance.as_dict(),

        "custom": self.metadata.custom.as_dict(),

        "statistics": self.statistics()
    }



    def plot(self,cmap: str = "gray",stretch: str = "percentile", lower=1,upper=99,figsize: tuple = (8, 8),title: str | None = None,colorbar: bool = True,):
        """
        Display the SAR image.
    
        Parameters
        ----------
        cmap : str
            Matplotlib colormap.
    
        figsize : tuple
            Figure size.
    
        vmin, vmax : float
            Color scaling limits.
    
        title : str
            Plot title.
    
        colorbar : bool
            Display colorbar.
        """
    
        import matplotlib.pyplot as plt
    
        _, ax = plt.subplots(figsize=figsize)
    
        img = ax.imshow(
            self.data,
            cmap=cmap,
            vmin=np.nanpercentile(self.data, lower),
            vmax=np.nanpercentile(self.data, upper),
        )
    
        if colorbar:
            plt.colorbar(img, ax=ax, label="Backscatter (dB)")
    
        if title is None:
            title = "SAR Image"
    
        ax.set_title(title)
        ax.set_xlabel("Column")
        ax.set_ylabel("Row")
    
        plt.tight_layout()
        plt.show()


    def histogram(
    self,
    bins: int = 100,
    figsize: tuple = (8, 5),
    title: str | None = None,
):
        """
        Display histogram of valid pixels.
        """
    
        import matplotlib.pyplot as plt
    
        #valid = self.data[self.mask]
        valid = self.valid_pixels
    
        _, ax = plt.subplots(figsize=figsize)
    
        ax.hist(valid, bins=bins)
    
        if title is None:
            title = "Backscatter Histogram"
    
        ax.set_title(title)
        ax.set_xlabel("Backscatter (dB)")
        ax.set_ylabel("Pixel Count")
    
        ax.grid(alpha=0.3)
    
        plt.tight_layout()
        plt.show()

    @property
    def shape(self):
        #return self.metadata.spatial.shape
        return self.data.shape
    
    @property
    def crs(self):
        return self.metadata.spatial.crs
    
    @property
    def bounds(self):
        return self.metadata.spatial.bounds
    
    @property
    def resolution(self):
        return self.metadata.spatial.resolution

    @property
    def valid_pixels(self):
        return self.data[self.mask]

    @property
    def transform(self):
        """Affine transform."""
        return self.metadata.spatial.transform

    @property
    def value_scale(self):
        return self.metadata.processing.value_scale

    @property
    def width(self) -> int:
        """Image width (columns)."""
        return self.shape[1]

    @property
    def height(self) -> int:
        """Image height (rows)."""
        return self.shape[0]

    @property
    def pixel_size_x(self) -> float:
        """Pixel size in X direction."""
        return abs(self.resolution[0])

    @property
    def pixel_size_y(self) -> float:
        """Pixel size in Y direction."""
        return abs(self.resolution[1])


    
    
