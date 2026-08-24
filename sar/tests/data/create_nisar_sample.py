"""
Create a minimal synthetic NISAR GCOV product for unit testing.

This script generates a lightweight HDF5 file that mimics the
parts of the official NISAR product used by GeoSAR.
"""

from pathlib import Path

import h5py
import numpy as np


OUTPUT = Path(__file__).parent / "sample_nisar_gcov.h5"


def create_sample():

    rng = np.random.default_rng(42)

    image = rng.gamma(
        shape=4.0,
        scale=1.0,
        size=(50, 50),
    ).astype(np.float32)

    # Simulate NoData
    image[:5, :5] = np.nan

    x = np.arange(
        500000,
        501000,
        20,
        dtype=np.float64,
    )

    y = np.arange(
        4100000,
        4099000,
        -20,
        dtype=np.float64,
    )

    with h5py.File(OUTPUT, "w") as f:

        science = f.create_group("science")
        lsar = science.create_group("LSAR")
        gcov = lsar.create_group("GCOV")
        grids = gcov.create_group("grids")
        frequency = grids.create_group("frequencyA")

        ds = frequency.create_dataset(
            "HHHH",
            data=image,
            dtype=np.float32,
        )

        ds.attrs["description"] = (
            b"Covariance between HH and HH"
        )
        ds.attrs["long_name"] = (
            b"Geocoded polarimetric covariance term HHHH"
        )
        ds.attrs["_FillValue"] = np.nan
        ds.attrs["units"] = b"1"
        ds.attrs["grid_mapping"] = b"projection"

        frequency.create_dataset(
            "xCoordinates",
            data=x,
        )

        frequency.create_dataset(
            "yCoordinates",
            data=y,
        )

        projection = frequency.create_dataset(
            "projection",
            data=np.uint32(0),
        )

        projection.attrs["description"] = (
            b"Product map grid projection"
        )
        projection.attrs["epsg_code"] = 32611
        projection.attrs["grid_mapping_name"] = (
            "transverse_mercator"
        )
        projection.attrs["false_easting"] = 500000.0
        projection.attrs["false_northing"] = 0.0
        projection.attrs["semi_major_axis"] = 6378137.0
        projection.attrs["inverse_flattening"] = (
            298.257223563
        )
        projection.attrs[
            "scale_factor_at_central_meridian"
        ] = 0.9996
        projection.attrs[
            "latitude_of_projection_origin"
        ] = 0.0
        projection.attrs[
            "longitude_of_central_meridian"
        ] = -117.0
        projection.attrs["utm_zone_number"] = 11

    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    create_sample()