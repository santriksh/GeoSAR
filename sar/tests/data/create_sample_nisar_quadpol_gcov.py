from pathlib import Path

import h5py
import numpy as np


OUTPUT = Path(__file__).parent / "sample_nisar_quadpol_gcov.h5"


def main():

    shape = (3, 3)

    hhhh = np.zeros(shape, dtype=np.float64)
    hhhv = np.zeros(shape, dtype=np.complex128)
    hhvv = np.zeros(shape, dtype=np.complex128)
    hvhv = np.zeros(shape, dtype=np.float64)
    hvvv = np.zeros(shape, dtype=np.complex128)
    vvvv = np.zeros(shape, dtype=np.float64)

    # --------------------------------------------------
    # Pixel (0,0): Pure surface scattering
    # Expected Pauli:
    # R=0, G=0, B=32
    # --------------------------------------------------

    hhhh[0, 0] = 16.0
    hhvv[0, 0] = 16.0 + 0.0j
    hvhv[0, 0] = 0.0
    vvvv[0, 0] = 16.0

    # --------------------------------------------------
    # Pixel (0,1): Pure double-bounce scattering
    # Expected Pauli:
    # R=32, G=0, B=0
    # --------------------------------------------------

    hhhh[0, 1] = 16.0
    hhvv[0, 1] = -16.0 + 0.0j
    hvhv[0, 1] = 0.0
    vvvv[0, 1] = 16.0

    # --------------------------------------------------
    # Pixel (0,2): Pure volume scattering
    # Expected Pauli:
    # R=0, G=32, B=0
    # --------------------------------------------------

    hhhh[0, 2] = 0.0
    hhvv[0, 2] = 0.0 + 0.0j
    hvhv[0, 2] = 16.0
    vvvv[0, 2] = 0.0

    with h5py.File(OUTPUT, "w") as f:

        # Minimal product structure
        science = f.create_group("science")
        lsar = science.create_group("LSAR")
        gcov = lsar.create_group("GCOV")
        grids = gcov.create_group("grids")
        frequency = grids.create_group("frequencyA")

        projection = frequency.create_group("projection")

        projection.attrs["epsg_code"] = 4326
        
        frequency.create_dataset(
            "xCoordinates",
            data=np.array(
                [0.0, 1.0, 2.0],
                dtype=np.float64,
            ),
        )

        frequency.create_dataset(
            "yCoordinates",
            data=np.array(
                [3.0, 2.0, 1.0],
                dtype=np.float64,
            ),
        )

        frequency.create_dataset(
            "HHHH",
            data=hhhh,
        )

        frequency.create_dataset(
            "HHHV",
            data=hhhv,
        )

        frequency.create_dataset(
            "HHVV",
            data=hhvv,
        )

        frequency.create_dataset(
            "HVHV",
            data=hvhv,
        )

        frequency.create_dataset(
            "HVVV",
            data=hvvv,
        )

        frequency.create_dataset(
            "VVVV",
            data=vvvv,
        )

    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()