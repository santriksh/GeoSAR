from dataclasses import dataclass
from sar.features.pauli import pauli_rgb_from_covariance
from .sar_image import SARImage
import numpy as np

@dataclass(frozen=True)
class CovarianceImage:
    """
    Representation of a quad-polarimetric covariance image.

    Only the six independent elements of the 3 × 3 Hermitian
    covariance matrix are stored.
    """

    hhhh: SARImage
    hhhv: SARImage
    hhvv: SARImage
    hvhv: SARImage
    hvvv: SARImage
    vvvv: SARImage

    def __post_init__(self):

        channels = (
            self.hhhh,
            self.hhhv,
            self.hhvv,
            self.hvhv,
            self.hvvv,
            self.vvvv,
        )

        reference = channels[0]

        for channel in channels[1:]:
            if channel.shape != reference.shape:
                raise ValueError(
                    "All covariance channels must have "
                    "the same shape."
                )

    def __getitem__(self, channel: str) -> SARImage:
        """
        Return a covariance channel.
    
        Stored channels are returned directly. Hermitian
        counterparts are reconstructed using complex conjugation.
        """
    
        channel = channel.upper()
    
        stored = {
            "HHHH": self.hhhh,
            "HHHV": self.hhhv,
            "HHVV": self.hhvv,
            "HVHV": self.hvhv,
            "HVVV": self.hvvv,
            "VVVV": self.vvvv,
        }
    
        if channel in stored:
            return stored[channel]
    
        hermitian = {
            "HVHH": "HHHV",
            "VVHH": "HHVV",
            "VVHV": "HVVV",
        }
    
        if channel in hermitian:
            source = stored[hermitian[channel]]
    
            return SARImage(
                data=np.conjugate(source.data),
                mask=source.mask.copy(),
                metadata=source.metadata,
            )
    
        raise KeyError(
            f"Unknown covariance channel: {channel}"
        )


    def matrix_at(self,row: int,col: int,) -> np.ndarray:
        """
        Return the 3 × 3 covariance matrix at one pixel.
    
        Parameters
        ----------
        row
            Pixel row.
    
        col
            Pixel column.
    
        Returns
        -------
        ndarray
            Complex 3 × 3 Hermitian covariance matrix.
        """
    
        if not 0 <= row < self.hhhh.height:
            raise IndexError(
                f"row {row} is outside image bounds."
            )
    
        if not 0 <= col < self.hhhh.width:
            raise IndexError(
                f"column {col} is outside image bounds."
            )
    
        hhhh = self.hhhh.data[row, col]
        hhhv = self.hhhv.data[row, col]
        hhvv = self.hhvv.data[row, col]
        hvhv = self.hvhv.data[row, col]
        hvvv = self.hvvv.data[row, col]
        vvvv = self.vvvv.data[row, col]
    
        return np.array(
            [
                [hhhh, hhhv, hhvv],
                [np.conjugate(hhhv), hvhv, hvvv],
                [np.conjugate(hhvv), np.conjugate(hvvv), vvvv],
            ],
            dtype=np.complex128,
        )



    def pauli_rgb(
        self,
    ) -> tuple[SARImage, SARImage, SARImage]:
        """
        Compute Pauli RGB channels.
    
        Returns
        -------
        red, green, blue
            SARImage objects representing:
    
            Red   -> Double-bounce scattering
            Green -> Volume scattering
            Blue  -> Surface scattering
        """
    
        red_data, green_data, blue_data = (
            pauli_rgb_from_covariance(
                hhhh=self.hhhh.data,
                hhvv=self.hhvv.data,
                hvhv=self.hvhv.data,
                vvvv=self.vvvv.data,
            )
        )
    
        return (
            SARImage(
                data=red_data,
                mask=self.hhhh.mask.copy(),
                metadata=self.hhhh.metadata,
            ),
            SARImage(
                data=green_data,
                mask=self.hhhh.mask.copy(),
                metadata=self.hhhh.metadata,
            ),
            SARImage(
                data=blue_data,
                mask=self.hhhh.mask.copy(),
                metadata=self.hhhh.metadata,
            ),
        )
    