from pathlib import Path

import h5py
import numpy as np


OUTPUT = Path(__file__).parent / "sample_nisar_quadpol_gcov.h5"


def main():

    shape = (3, 3)

    # --------------------------------------------------
    # Raw NISAR C4 covariance terms
    #
    # The 4-channel scattering vector is:
    #
    #   [S_HH, S_HV, S_VH, S_VV]
    #
    # This produces 10 covariance terms:
    #
    #   HHHH, HHHV, HHVH, HHVV,
    #   HVHV, HVVH, HVVV,
    #   VHVH, VHVV, VVVV
    # --------------------------------------------------

    hhhh = np.zeros(shape, dtype=np.float64)
    hhhv = np.zeros(shape, dtype=np.complex128)
    hhvh = np.zeros(shape, dtype=np.complex128)
    hhvv = np.zeros(shape, dtype=np.complex128)

    hvhv = np.zeros(shape, dtype=np.float64)
    hvvh = np.zeros(shape, dtype=np.complex128)
    hvvv = np.zeros(shape, dtype=np.complex128)

    vhvh = np.zeros(shape, dtype=np.float64)
    vhvv = np.zeros(shape, dtype=np.complex128)

    vvvv = np.zeros(shape, dtype=np.float64)

    # --------------------------------------------------
    # Pixel (0,0): Pure surface scattering
    #
    # Existing Pauli expectation:
    #
    #   R = 0
    #   G = 0
    #   B = 32
    #
    # HHHH = 16
    # HHVV = +16
    # HVHV = 0
    # VVVV = 16
    # --------------------------------------------------

    hhhh[0, 0] = 16.0
    hhvv[0, 0] = 16.0 + 0.0j
    hvhv[0, 0] = 0.0
    vvvv[0, 0] = 16.0

    # --------------------------------------------------
    # Pixel (0,1): Pure double-bounce scattering
    #
    # Existing Pauli expectation:
    #
    #   R = 32
    #   G = 0
    #   B = 0
    #
    # HHHH = 16
    # HHVV = -16
    # HVHV = 0
    # VVVV = 16
    # --------------------------------------------------

    hhhh[0, 1] = 16.0
    hhvv[0, 1] = -16.0 + 0.0j
    hvhv[0, 1] = 0.0
    vvvv[0, 1] = 16.0

    # --------------------------------------------------
    # Pixel (0,2): Pure volume scattering
    #
    # Existing Pauli expectation:
    #
    #   R = 0
    #   G = 32
    #   B = 0
    #
    # HHHH = 0
    # HHVV = 0
    # HVHV = 16
    # VVVV = 0
    # --------------------------------------------------

    hhhh[0, 2] = 0.0
    hhvv[0, 2] = 0.0 + 0.0j
    hvhv[0, 2] = 16.0
    vvvv[0, 2] = 0.0

    # --------------------------------------------------
    # The four additional raw NISAR terms
    #
    # For these three Pauli test pixels, the cross terms
    # are zero, so we can keep them zero.
    #
    # This keeps the existing Pauli tests unchanged while
    # making the fixture structurally equivalent to a
    # 10-term raw NISAR C4 product.
    # --------------------------------------------------

    # --------------------------------------------------
    # Pixel (2,2): Synthetic complex covariance terms
    #
    # This pixel is used to test the P05023 polarization-
    # orientation correction.
    # --------------------------------------------------

    hhhh[2, 2] = 10.0
    hhhv[2, 2] = 1.0 + 2.0j
    hhvh[2, 2] = 3.0 - 1.0j
    hhvv[2, 2] = 4.0 + 5.0j

    hvhv[2, 2] = 5.0
    hvvh[2, 2] = 2.0 + 3.0j
    hvvv[2, 2] = 1.0 - 2.0j

    vhvh[2, 2] = 5.0
    vhvv[2, 2] = 3.0 + 4.0j

    vvvv[2, 2] = 12.0


    hhvh[:] = 0.0 + 0.0j
    hvvh[:] = 0.0 + 0.0j
    vhvh[:] = hvhv
    vhvv[:] = 0.0 + 0.0j

    # Synthetic complex terms for orientation-correction test.
    hhhv[2, 2] = 1.0 + 2.0j
    hhvh[2, 2] = 3.0 - 1.0j
    hhvv[2, 2] = 4.0 + 5.0j

    hvvh[2, 2] = 2.0 + 3.0j
    hvvv[2, 2] = 1.0 - 2.0j
    vhvv[2, 2] = 3.0 + 4.0j

    # Diagonal values for the synthetic test pixel.
    hhhh[2, 2] = 10.0
    hvhv[2, 2] = 5.0
    vhvh[2, 2] = 5.0
    vvvv[2, 2] = 12.0

    # --------------------------------------------------
    # Create minimal NISAR-like HDF5 structure
    # --------------------------------------------------

    with h5py.File(OUTPUT, "w") as f:

        # Product hierarchy
        science = f.create_group("science")
        lsar = science.create_group("LSAR")
        gcov = lsar.create_group("GCOV")
        grids = gcov.create_group("grids")
        frequency = grids.create_group("frequencyA")

        # --------------------------------------------------
        # Spatial metadata
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Raw covariance datasets
        # --------------------------------------------------

        frequency.create_dataset(
            "HHHH",
            data=hhhh,
        )

        frequency.create_dataset(
            "HHHV",
            data=hhhv,
        )

        frequency.create_dataset(
            "HHVH",
            data=hhvh,
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
            "HVVH",
            data=hvvh,
        )

        frequency.create_dataset(
            "HVVV",
            data=hvvv,
        )

        frequency.create_dataset(
            "VHVH",
            data=vhvh,
        )

        frequency.create_dataset(
            "VHVV",
            data=vhvv,
        )

        frequency.create_dataset(
            "VVVV",
            data=vvvv,
        )

        # --------------------------------------------------
        # NISAR product metadata
        # --------------------------------------------------

        frequency.create_dataset(
            "listOfCovarianceTerms",
            data=np.array(
                [
                    b"HHHH",
                    b"HHHV",
                    b"HHVH",
                    b"HHVV",
                    b"HVHV",
                    b"HVVH",
                    b"HVVV",
                    b"VHVH",
                    b"VHVV",
                    b"VVVV",
                ],
                dtype="S4",
            ),
        )

        frequency.create_dataset(
            "listOfPolarizations",
            data=np.array(
                [
                    b"HH",
                    b"HV",
                    b"VH",
                    b"VV",
                ],
                dtype="S2",
            ),
        )

    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
