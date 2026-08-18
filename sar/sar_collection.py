"""
sar_collection.py

Container class for multiple SARImage objects.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from .sar_image import SARImage


@dataclass
class SARCollection:
    """
    Represents a collection of SARImage objects.

    The collection behaves like a Python sequence while also
    providing SAR-specific utilities.
    """

    images: list[SARImage] = field(default_factory=list)

    def __len__(self) -> int:
        """Return number of images."""
        return len(self.images)

    def __getitem__(self, index):
        return self.images[index]

    def __iter__(self) -> Iterator[SARImage]:
        """Iterate over images."""
        return iter(self.images)

    def add(self, image: SARImage) -> None:
        """
        Add a SARImage to the collection.
        """
    
        if not isinstance(image, SARImage):
            raise TypeError(
                "Only SARImage objects can be added."
            )
    
        self.images.append(image)


    def remove(self, image: SARImage) -> None:
        """
        Remove an image from the collection.
        """
        self.images.remove(image)


    def clear(self) -> None:
        """Remove all images."""
        self.images.clear()

    @property
    def is_empty(self) -> bool:
        return len(self.images) == 0


    def summary(self) -> dict[str, Any]:
        """
        Return summary information about the collection.
        """
    
        if self.is_empty:
            return {
                "number_of_images": 0
            }
    
        return {
    
            "number_of_images": len(self),
    
            "platforms": sorted(
                {
                    image.metadata.acquisition.platform
                    for image in self
                }
            ),
    
            "polarizations": sorted(
                {
                    image.metadata.acquisition.polarization
                    for image in self
                }
            ),
    
            "orbit_directions": sorted(
                {
                    image.metadata.acquisition.orbit_direction
                    for image in self
                }
            ),
    
            "relative_orbits": sorted(
                {
                    image.metadata.acquisition.relative_orbit
                    for image in self
                    if image.metadata.acquisition.relative_orbit is not None
                }
            )
        }

    
