"""
Base reader interface for all SAR products.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sar.sar_image import SARImage


class BaseReader(ABC):
    """
    Abstract base class for all GeoSAR readers.
    """

    @abstractmethod
    def read(self, **kwargs) -> SARImage:
        """
        Read a SAR product and return a SARImage.
        """
        raise NotImplementedError

    def close(self):
        """
        Release any resources held by the reader.
        """
        pass