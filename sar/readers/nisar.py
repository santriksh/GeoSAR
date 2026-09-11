"""
Reader for NASA–ISRO NISAR products.
"""

from __future__ import annotations

import h5py

from .base import BaseReader

from affine import Affine
from rasterio.coords import BoundingBox
from rasterio.crs import CRS
from sar.io.window import Window
from sar.sar_metadata import SpatialMetadata
from sar.sar_metadata import AcquisitionMetadata
from sar.sar_metadata import ProcessingMetadata
from sar.sar_metadata import ProvenanceMetadata
from sar.sar_metadata import (
    SARMetadata,
    CustomMetadata,
)
from sar.sar_image import SARImage
import numpy as np
from sar.covariance import CovarianceImage
from sar.polarimetry import (
    correct_p05023_covariance,
    symmetrize_nisar_covariance,
)

_METADATA_DATASETS = {
    "projection",
    "xCoordinates",
    "yCoordinates",
}

class NISARReader(BaseReader):
    """
    Reader for NISAR HDF5 products.
    """


    def __init__(self, filename: str):

        self.filename = filename

        self.file = h5py.File(filename, "r")

        self._validate_product()

        self._science = self.file["science"]
        self._lsar = self._science["LSAR"]
        self._gcov = self._lsar["GCOV"]
        self._grids = self._gcov["grids"]
        self._discover_product()

        self._default_group = self._grids[self.default_frequency]

    def read(self, **kwargs):
        """
        Read a NISAR product.

        Not implemented yet.
        """

        raise NotImplementedError

    def close(self):

        self.file.close()


    def _validate_product(self):
        """
        Validate that the HDF5 file is a supported
        NISAR GCOV product.
        """

        required_paths = [
            "science",
            "science/LSAR",
            "science/LSAR/GCOV",
        ]

        for path in required_paths:

            if path not in self.file:

                raise ValueError(
                    f"Invalid NISAR GCOV product. "
                    f"Missing '{path}'."
                )



    def _discover_product(self):
        """
        Discover available frequencies, polarizations,
        and covariance terms.
        """

        self._frequencies = sorted(self._grids.keys())

        self._polarizations = {}
        self._covariance_terms = {}

        for frequency in self._frequencies:

            group = self._grids[frequency]

            # ------------------------------------------
            # Polarizations
            # ------------------------------------------

            if "listOfPolarizations" in group:

                values = group["listOfPolarizations"][()]

                self._polarizations[frequency] = sorted(
                    value.decode()
                    if isinstance(value, bytes)
                    else str(value)
                    for value in values
                )

            else:

                # Backward-compatible fallback for our
                # minimal synthetic fixture.
                self._polarizations[frequency] = sorted(
                    name
                    for name in group.keys()
                    if name not in _METADATA_DATASETS
                )

            # ------------------------------------------
            # Covariance terms
            # ------------------------------------------

            if "listOfCovarianceTerms" in group:

                values = group["listOfCovarianceTerms"][()]

                self._covariance_terms[frequency] = sorted(
                    value.decode()
                    if isinstance(value, bytes)
                    else str(value)
                    for value in values
                )

            else:

                #self._covariance_terms[frequency] = []
                required_terms = {
                    "HHHH",
                    "HHHV",
                    "HHVV",
                    "HVHV",
                    "HVVV",
                    "VVVV",
                }

                self._covariance_terms[frequency] = sorted(
                    name
                    for name in group.keys()
                    if name in required_terms
                )

    def _resolve_polarization_dataset(
        self,
        frequency: str,
        polarization: str,
    ) -> str:
        """
        Resolve a polarization to its corresponding NISAR dataset.

        Parameters
        ----------
        frequency : str
            Frequency group.

        polarization : str
            Polarization, e.g. "HH".

        Returns
        -------
        str
            Dataset name containing the polarization data.
        """

        if polarization == "HH":
            return "HHHH"

        raise ValueError(
            f"Unsupported polarization '{polarization}'."
        )

    def _read_image(self,frequency: str | None = None,polarization: str | None = None,):
        """
        Read a polarization image from the NISAR product.

        Parameters
        ----------
        frequency : str, optional
            Frequency group (e.g. "frequencyA").

        polarization : str, optional
            Polarization dataset (e.g. "HHHH").

        Returns
        -------
        numpy.ndarray
            Image data.
        """

        frequency = frequency or self.default_frequency

        polarization = (
        polarization or self.default_polarization
    )
        if frequency not in self.frequencies:
            raise ValueError(
                f"Unknown frequency '{frequency}'."
            )

        if polarization not in self.polarizations[frequency]:
            raise ValueError(
                f"Unknown polarization '{polarization}'."
            )

        dataset_name = self._resolve_polarization_dataset(
            frequency,
            polarization,
        )

        return self._grids[
            frequency
        ][dataset_name][()]

    #     return self._grids[
    #     frequency
    # ][polarization][()]


    def _read_covariance_window(
        self,
        frequency: str,
        rows: slice,
        cols: slice,
    ) -> dict[str, np.ndarray]:
        """
        Read the raw NISAR covariance terms for a spatial window.

        Parameters
        ----------
        frequency:
            NISAR GCOV frequency group, e.g. ``"frequencyA"``.

        rows:
            Row slice defining the requested spatial window.

        cols:
            Column slice defining the requested spatial window.

        Returns
        -------
        dict[str, np.ndarray]
            The ten raw NISAR covariance terms for the window.
        """

        required_terms = (
            "HHHH",
            "HHHV",
            "HHVH",
            "HHVV",
            "HVHV",
            "HVVH",
            "HVVV",
            "VHVH",
            "VHVV",
            "VVVV",
        )

        if frequency not in self.frequencies:
            raise ValueError(
                f"Unknown frequency '{frequency}'. "
                f"Available frequencies: {self.frequencies}"
            )

        group = self._grids[frequency]

        available_terms = set(self.covariance_terms[frequency])

        missing_terms = [
            term
            for term in required_terms
            if term not in available_terms
        ]

        if missing_terms:
            raise ValueError(
                "Incomplete covariance: "
                f"missing covariance terms {missing_terms}"
            )

        return {
            term: group[term][rows, cols]
            for term in required_terms
        }



    def _read_spatial_metadata(self) -> SpatialMetadata:
        """
        Read spatial metadata from the NISAR product.
        """

        projection = self._default_group["projection"]

        x = self._default_group["xCoordinates"][()]
        y = self._default_group["yCoordinates"][()]

        pixel_size_x = float(x[1] - x[0])
        pixel_size_y = float(abs(y[1] - y[0]))

        transform = Affine(
            pixel_size_x,
            0.0,
            float(x[0]),
            0.0,
            -pixel_size_y,
            float(y[0]),
        )

        width = len(x)
        height = len(y)

        bounds = BoundingBox(
            left=float(x[0]),
            bottom=float(y[-1] - pixel_size_y),
            right=float(x[-1] + pixel_size_x),
            top=float(y[0]),
        )

        crs = CRS.from_epsg(
            int(projection.attrs["epsg_code"])
        )

        return SpatialMetadata(
            crs=crs,
            transform=transform,
            bounds=bounds,
            resolution=(pixel_size_x, pixel_size_y),
            shape=(height, width),
        )


    def _read_acquisition_metadata(self) -> AcquisitionMetadata:
        """
        Read acquisition metadata from the NISAR product.
        """

        return AcquisitionMetadata(
            platform="NISAR",
            sensor="LSAR",
            polarization=self.default_polarization,
            frequency_band=self.default_frequency,
        )



    def _read_processing_metadata(self) -> ProcessingMetadata:
        """
        Read processing metadata from the NISAR product.
        """

        return ProcessingMetadata(
            processing_level="L2",
            product_type="GCOV",
            value_scale="Linear",
            terrain_corrected=True,
            speckle_filtered=False,
        )


    def _build_provenance_metadata(self) -> ProvenanceMetadata:
        """
        Build provenance metadata for the loaded product.
        """

        return ProvenanceMetadata(
            operation="load_nisar",
            inputs=[str(self.filename)],
            parameters={},
            created_by="GeoSAR",
        )


    def _build_metadata(self) -> SARMetadata:
        """
        Build the complete metadata for the product.
        """

        return SARMetadata(
            spatial=self._read_spatial_metadata(),
            acquisition=self._read_acquisition_metadata(),
            processing=self._read_processing_metadata(),
            provenance=self._build_provenance_metadata(),
            custom=CustomMetadata(),
        )


    def read(
        self,
        frequency: str | None = None,
        polarization: str | None = None,
    ) -> SARImage:
        """
        Read a NISAR product and return a SARImage.
        """

        image = self._read_image(
            frequency=frequency,
            polarization=polarization,
        )

        metadata = self._build_metadata()

        mask = np.isfinite(image)

        return SARImage(
            data=image,
            mask=mask,
            metadata=metadata,
        )



    # def read_covariance(self, frequency=None) -> CovarianceImage:
    #     """
    #     Read the complete six-term covariance matrix.

    #     A full polarimetric covariance image requires:
    #         HHHH, HHHV, HHVV, HVHV, HVVV, VVVV
    #     """

    #     frequency = frequency or self.default_frequency

    #     if frequency not in self.frequencies:
    #         raise ValueError(
    #             f"Unknown frequency '{frequency}'. "
    #             f"Available frequencies: {self.frequencies}"
    #         )

    #     required_terms = (
    #         "HHHH",
    #         "HHHV",
    #         "HHVV",
    #         "HVHV",
    #         "HVVV",
    #         "VVVV",
    #     )

    #     available_terms = set(self.covariance_terms[frequency])

    #     missing_terms = [
    #         term for term in required_terms
    #         if term not in available_terms
    #     ]

    #     if missing_terms:
    #         raise ValueError(
    #             "Incomplete covariance: "
    #             f"missing covariance terms {missing_terms}"
    #         )

    #     channels = {}

    #     for term in required_terms:
    #         channels[term] = self._grids[frequency][term][()]

    #     metadata = self._build_metadata()

    #     mask = np.isfinite(channels["HHHH"])

    #     images = {
    #         term: SARImage(
    #             data=data,
    #             mask=mask.copy(),
    #             metadata=metadata,
    #         )
    #         for term, data in channels.items()
    #     }

    #     return CovarianceImage(
    #         hhhh=images["HHHH"],
    #         hhhv=images["HHHV"],
    #         hhvv=images["HHVV"],
    #         hvhv=images["HVHV"],
    #         hvvv=images["HVVV"],
    #         vvvv=images["VVVV"],
    #     )

    def read_covariance(
        self,
        frequency: str | None = None,
    ) -> CovarianceImage:
        """
        Read a full symmetrized covariance image.

        The NISAR raw 4-channel covariance representation is first
        read as ten covariance terms, then converted into the six
        independent terms of the symmetrized 3 × 3 covariance matrix.
        """

        frequency = frequency or self.default_frequency

        if frequency not in self.frequencies:
            raise ValueError(
                f"Unknown frequency '{frequency}'. "
                f"Available frequencies: {self.frequencies}"
            )

        required_terms = (
            "HHHH",
            "HHHV",
            "HHVH",
            "HHVV",
            "HVHV",
            "HVVH",
            "HVVV",
            "VHVH",
            "VHVV",
            "VVVV",
        )

        available_terms = set(self.covariance_terms[frequency])

        missing_terms = [
            term
            for term in required_terms
            if term not in available_terms
        ]

        if missing_terms:
            raise ValueError(
                "Incomplete covariance: "
                f"missing covariance terms {missing_terms}"
            )

        # Read the raw ten-term NISAR C4 representation.
        raw_covariance = {
            term: self._grids[frequency][term][()]
            for term in required_terms
        }

        # Convert raw C4 → symmetrized G3.
        g3_terms = symmetrize_nisar_covariance(
            raw_covariance
        )

        metadata = self._build_metadata()

        mask = np.isfinite(g3_terms["HHHH"])

        images = {
            term: SARImage(
                data=data,
                mask=mask.copy(),
                metadata=metadata,
            )
            for term, data in g3_terms.items()
        }

        return CovarianceImage(
            hhhh=images["HHHH"],
            hhhv=images["HHHV"],
            hhvv=images["HHVV"],
            hvhv=images["HVHV"],
            hvvv=images["HVVV"],
            vvvv=images["VVVV"],
        )


    def read_covariance_window(
        self,
        window: Window,
        frequency: str | None = None,
        *,
        orientation_correction: bool = False,
    ) -> CovarianceImage:
        """
        Read a spatial window of a full-polarimetric covariance product.

        The raw ten-term NISAR covariance representation is read only
        for the requested window, optionally corrected for the
        product-specific polarization-orientation issue, and then
        converted into the six independent terms of the symmetrized
        3 × 3 covariance matrix.
        """

        frequency = frequency or self.default_frequency

        raw_covariance = self._read_covariance_window(
            frequency=frequency,
            rows=window.rows,
            cols=window.cols,
        )

        if orientation_correction:
            raw_covariance = correct_p05023_covariance(
                raw_covariance
            )

        g3_terms = symmetrize_nisar_covariance(
            raw_covariance
        )

        metadata = self._build_metadata()

        mask = np.isfinite(
            g3_terms["HHHH"]
        )

        images = {
            term: SARImage(
                data=data,
                mask=mask.copy(),
                metadata=metadata,
            )
            for term, data in g3_terms.items()
        }

        return CovarianceImage(
            hhhh=images["HHHH"],
            hhhv=images["HHHV"],
            hhvv=images["HHVV"],
            hvhv=images["HVHV"],
            hvvv=images["HVVV"],
            vvvv=images["VVVV"],
        )



    @property
    def frequencies(self):
        return self._frequencies


    @property
    def polarizations(self):
        return self._polarizations


    @property
    def default_frequency(self):
        return self._frequencies[0]


    @property
    def default_polarization(self):
        return self._polarizations[
            self.default_frequency
        ][0]

    @property
    def covariance_terms(self):
        """
        Available covariance terms for each frequency.
        """
        return self._covariance_terms
