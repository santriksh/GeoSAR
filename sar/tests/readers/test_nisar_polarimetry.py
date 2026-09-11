import numpy as np


def test_symmetrized_g3_from_c4():
    """
    Verify the 4-pol C4 -> symmetrized 3-pol G3 transformation.
    """

    # -----------------------------------------------------
    # Construct a deterministic Hermitian C4.
    #
    # Polarization ordering:
    # HH, HV, VH, VV
    # -----------------------------------------------------

    C4 = np.array(
        [
            [10.0, 1.0 + 2.0j, 3.0 - 1.0j, 4.0 + 0.5j],
            [1.0 - 2.0j, 5.0, 0.5 + 1.0j, 2.0 - 0.5j],
            [3.0 + 1.0j, 0.5 - 1.0j, 6.0, 1.5 + 0.2j],
            [4.0 - 0.5j, 2.0 + 0.5j, 1.5 - 0.2j, 8.0],
        ],
        dtype=np.complex128,
    )

    # -----------------------------------------------------
    # Symmetrization matrix
    # -----------------------------------------------------

    A = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.5, 0.5, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=np.complex128,
    )

    # -----------------------------------------------------
    # Reference result from the matrix transformation
    # -----------------------------------------------------

    expected = A @ C4 @ A.conj().T

    # -----------------------------------------------------
    # Six independent G3 elements from the NISAR terms
    # -----------------------------------------------------

    hhhh = C4[0, 0]
    hhhv = C4[0, 1]
    hhvh = C4[0, 2]
    hhvv = C4[0, 3]

    hvhv = C4[1, 1]
    hvvh = C4[1, 2]
    hvvv = C4[1, 3]

    vhvh = C4[2, 2]
    vhvv = C4[2, 3]

    vvvv = C4[3, 3]

    actual = np.array(
        [
            [
                hhhh,
                (hhhv + hhvh) / 2.0,
                hhvv,
            ],
            [
                np.conj(hhhv + hhvh) / 2.0,
                (hvhv + vhvh + 2.0 * np.real(hvvh)) / 4.0,
                (hvvv + vhvv) / 2.0,
            ],
            [
                np.conj(hhvv),
                np.conj(hvvv + vhvv) / 2.0,
                vvvv,
            ],
        ],
        dtype=np.complex128,
    )

    np.testing.assert_allclose(
    actual,
    expected,
    rtol=1e-12,
    atol=1e-12,
)


import numpy as np

from sar.polarimetry import symmetrize_nisar_covariance


def test_symmetrize_nisar_covariance():
    """Test raw NISAR 10-term covariance -> six G3 terms."""

    hhhh = np.array([[10.0]])
    hhhv = np.array([[1.0 + 2.0j]])
    hhvh = np.array([[3.0 - 1.0j]])
    hhvv = np.array([[4.0 + 0.5j]])

    hvhv = np.array([[5.0]])
    hvvh = np.array([[0.5 + 1.0j]])
    hvvv = np.array([[2.0 - 0.5j]])

    vhvh = np.array([[6.0]])
    vhvv = np.array([[1.5 + 0.2j]])

    vvvv = np.array([[8.0]])

    raw = {
        "HHHH": hhhh,
        "HHHV": hhhv,
        "HHVH": hhvh,
        "HHVV": hhvv,
        "HVHV": hvhv,
        "HVVH": hvvh,
        "HVVV": hvvv,
        "VHVH": vhvh,
        "VHVV": vhvv,
        "VVVV": vvvv,
    }

    result = symmetrize_nisar_covariance(raw)

    # --------------------------------------------------
    # Expected symmetrized G3 terms
    # --------------------------------------------------

    expected_hhhv = (
        hhhv + hhvh
    ) / 2.0

    expected_hvhv = (
        hvhv
        + vhvh
        + 2.0 * np.real(hvvh)
    ) / 4.0

    expected_hvvv = (
        hvvv + vhvv
    ) / 2.0

    assert np.allclose(
        result["HHHH"],
        hhhh,
    )

    assert np.allclose(
        result["HHHV"],
        expected_hhhv,
    )

    assert np.allclose(
        result["HHVV"],
        hhvv,
    )

    assert np.allclose(
        result["HVHV"],
        expected_hvhv,
    )

    assert np.allclose(
        result["HVVV"],
        expected_hvvv,
    )

    assert np.allclose(
        result["VVVV"],
        vvvv,
    )

    # Explicit numerical checks for readability.
    assert np.allclose(
        result["HHHV"],
        [[2.0 + 0.5j]],
    )

    assert np.allclose(
        result["HVHV"],
        [[3.0]],
    )

    assert np.allclose(
        result["HVVV"],
        [[1.75 - 0.15j]],
    )


def test_symmetrize_nisar_covariance_is_hermitian():
    """Test that symmetrized NISAR G3 is Hermitian."""

    shape = (3, 4)

    rng = np.random.default_rng(42)

    hhhh = rng.random(shape)
    hhhv = rng.random(shape) + 1j * rng.random(shape)
    hhvh = rng.random(shape) + 1j * rng.random(shape)
    hhvv = rng.random(shape) + 1j * rng.random(shape)

    hvhv = rng.random(shape)
    hvvh = rng.random(shape) + 1j * rng.random(shape)
    hvvv = rng.random(shape) + 1j * rng.random(shape)

    vhvh = rng.random(shape)
    vhvv = rng.random(shape) + 1j * rng.random(shape)

    vvvv = rng.random(shape)

    raw = {
        "HHHH": hhhh,
        "HHHV": hhhv,
        "HHVH": hhvh,
        "HHVV": hhvv,
        "HVHV": hvhv,
        "HVVH": hvvh,
        "HVVV": hvvv,
        "VHVH": vhvh,
        "VHVV": vhvv,
        "VVVV": vvvv,
    }

    result = symmetrize_nisar_covariance(raw)

    # --------------------------------------------------
    # Reconstruct the full 3 x 3 Hermitian G3 matrix
    # from its six independent terms.
    # --------------------------------------------------

    g3 = np.empty(
        shape + (3, 3),
        dtype=np.complex128,
    )

    g3[..., 0, 0] = result["HHHH"]
    g3[..., 0, 1] = result["HHHV"]
    g3[..., 0, 2] = result["HHVV"]

    g3[..., 1, 0] = np.conjugate(
        result["HHHV"]
    )
    g3[..., 1, 1] = result["HVHV"]
    g3[..., 1, 2] = result["HVVV"]

    g3[..., 2, 0] = np.conjugate(
        result["HHVV"]
    )
    g3[..., 2, 1] = np.conjugate(
        result["HVVV"]
    )
    g3[..., 2, 2] = result["VVVV"]

    # --------------------------------------------------
    # Hermitian property:
    #
    # G3 = G3^H
    # --------------------------------------------------

    assert np.allclose(
        g3,
        np.conjugate(
            np.swapaxes(g3, -1, -2)
        ),
    )


def test_symmetrized_g3_integrates_with_covariance_image():
    """Test that symmetrized G3 integrates with CovarianceImage."""

    from sar.covariance import CovarianceImage
    from sar.sar_image import SARImage
    from sar.sar_metadata import (
        SARMetadata,
        SpatialMetadata,
        AcquisitionMetadata,
        ProcessingMetadata,
        ProvenanceMetadata,
        CustomMetadata,
    )

    shape = (1, 1)

    # --------------------------------------------------
    # Minimal metadata required by SARImage.
    # --------------------------------------------------

    metadata = SARMetadata(
        spatial=SpatialMetadata(
            crs="EPSG:32611",
            transform=None,
            bounds=None,
            resolution=(20.0, 20.0),
            shape=shape,
        ),
        acquisition=AcquisitionMetadata(),
        processing=ProcessingMetadata(),
        provenance=ProvenanceMetadata(),
        custom=CustomMetadata(),
    )

    mask = np.ones(
        shape,
        dtype=bool,
    )

    # --------------------------------------------------
    # Raw NISAR covariance terms.
    # --------------------------------------------------

    hhhh = np.array([[10.0]])
    hhhv = np.array([[1.0 + 2.0j]])
    hhvh = np.array([[3.0 - 1.0j]])
    hhvv = np.array([[4.0 + 0.5j]])

    hvhv = np.array([[5.0]])
    hvvh = np.array([[0.5 + 1.0j]])
    hvvv = np.array([[2.0 - 0.5j]])

    vhvh = np.array([[6.0]])
    vhvv = np.array([[1.5 + 0.2j]])

    vvvv = np.array([[8.0]])

    raw = {
        "HHHH": hhhh,
        "HHHV": hhhv,
        "HHVH": hhvh,
        "HHVV": hhvv,
        "HVHV": hvhv,
        "HVVH": hvvh,
        "HVVV": hvvv,
        "VHVH": vhvh,
        "VHVV": vhvv,
        "VVVV": vvvv,
    }

    # --------------------------------------------------
    # Raw C4 -> symmetrized G3.
    # --------------------------------------------------

    g3_terms = symmetrize_nisar_covariance(raw)

    # --------------------------------------------------
    # Convert G3 terms to SARImage objects.
    # --------------------------------------------------

    images = {
        term: SARImage(
            data=data,
            mask=mask.copy(),
            metadata=metadata,
        )
        for term, data in g3_terms.items()
    }

    covariance = CovarianceImage(
        hhhh=images["HHHH"],
        hhhv=images["HHHV"],
        hhvv=images["HHVV"],
        hvhv=images["HVHV"],
        hvvv=images["HVVV"],
        vvvv=images["VVVV"],
    )

    # --------------------------------------------------
    # Verify CovarianceImage construction.
    # --------------------------------------------------

    assert covariance.hhhh.shape == shape
    assert covariance.hhhv.shape == shape
    assert covariance.hhvv.shape == shape
    assert covariance.hvhv.shape == shape
    assert covariance.hvvv.shape == shape
    assert covariance.vvvv.shape == shape

    # --------------------------------------------------
    # Verify the symmetrized values.
    # --------------------------------------------------

    assert np.allclose(
        covariance["HHHV"].data,
        [[2.0 + 0.5j]],
    )

    assert np.allclose(
        covariance["HVHV"].data,
        [[3.0]],
    )

    assert np.allclose(
        covariance["HVVV"].data,
        [[1.75 - 0.15j]],
    )

    # --------------------------------------------------
    # Verify matrix_at() produces the expected G3 matrix.
    # --------------------------------------------------

    matrix = covariance.matrix_at(
        row=0,
        col=0,
    )

    assert matrix.shape == (3, 3)

    assert np.allclose(
        matrix,
        np.array(
            [
                [
                    10.0,
                    2.0 + 0.5j,
                    4.0 + 0.5j,
                ],
                [
                    2.0 - 0.5j,
                    3.0,
                    1.75 - 0.15j,
                ],
                [
                    4.0 - 0.5j,
                    1.75 + 0.15j,
                    8.0,
                ],
            ],
            dtype=np.complex128,
        ),
    )


def test_read_covariance_window():
    """Test windowed reading of raw NISAR covariance terms."""

    from pathlib import Path

    from sar.readers.nisar import NISARReader

    path = (
        Path(__file__).parents[1]
        / "data"
        / "sample_nisar_quadpol_gcov.h5"
    )

    rows = slice(0, 2)
    cols = slice(0, 2)

    reader = NISARReader(path)

    result = reader._read_covariance_window(
        frequency="frequencyA",
        rows=rows,
        cols=cols,
    )

    expected_terms = {
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
    }

    assert set(result) == expected_terms

    for term, array in result.items():
        assert array.shape == (2, 2)


def test_nisar_reader_to_symmetrized_g3():
    """Test NISAR reader C4 window -> symmetrized G3."""

    from pathlib import Path

    from sar.polarimetry import (
        symmetrize_nisar_covariance,
    )
    from sar.readers.nisar import NISARReader

    path = (
        Path(__file__).parents[1]
        / "data"
        / "sample_nisar_quadpol_gcov.h5"
    )

    reader = NISARReader(path)

    try:

        # --------------------------------------------------
        # Read a 2 x 2 window from the raw NISAR C4 product.
        # --------------------------------------------------

        raw = reader._read_covariance_window(
            frequency="frequencyA",
            rows=slice(0, 2),
            cols=slice(0, 2),
        )

        # --------------------------------------------------
        # Convert raw 10-term C4 representation into
        # six independent symmetrized G3 terms.
        # --------------------------------------------------

        g3_terms = symmetrize_nisar_covariance(
            raw
        )

        # --------------------------------------------------
        # Reconstruct the complete 3 x 3 G3 matrix.
        # --------------------------------------------------

        g3 = np.empty(
            g3_terms["HHHH"].shape + (3, 3),
            dtype=np.complex128,
        )

        g3[..., 0, 0] = g3_terms["HHHH"]
        g3[..., 0, 1] = g3_terms["HHHV"]
        g3[..., 0, 2] = g3_terms["HHVV"]

        g3[..., 1, 0] = np.conjugate(
            g3_terms["HHHV"]
        )
        g3[..., 1, 1] = g3_terms["HVHV"]
        g3[..., 1, 2] = g3_terms["HVVV"]

        g3[..., 2, 0] = np.conjugate(
            g3_terms["HHVV"]
        )
        g3[..., 2, 1] = np.conjugate(
            g3_terms["HVVV"]
        )
        g3[..., 2, 2] = g3_terms["VVVV"]

        # --------------------------------------------------
        # Shape check.
        # --------------------------------------------------

        assert g3.shape == (
            2,
            2,
            3,
            3,
        )

        # --------------------------------------------------
        # Hermitian property.
        # --------------------------------------------------

        assert np.allclose(
            g3,
            np.conjugate(
                np.swapaxes(
                    g3,
                    -1,
                    -2,
                )
            ),
        )

        # --------------------------------------------------
        # Known synthetic fixture values.
        #
        # Pixel (0,0): pure surface
        # G3 diagonal = [16, 0, 16]
        #
        # Pixel (0,1): pure double bounce
        # G3 diagonal = [16, 0, 16]
        #
        # Pixel (1,0), (1,1): zero-valued fixture pixels.
        # --------------------------------------------------

        assert np.isclose(
            g3[0, 0, 0, 0],
            16.0,
        )

        assert np.isclose(
            g3[0, 0, 1, 1],
            0.0,
        )

        assert np.isclose(
            g3[0, 0, 2, 2],
            16.0,
        )

        assert np.isclose(
            g3[0, 1, 0, 0],
            16.0,
        )

        assert np.isclose(
            g3[0, 1, 2, 2],
            16.0,
        )

    finally:
        reader.close()



def test_p05023_orientation_correction():
    """Test the P05023 covariance phase correction."""

    from sar.polarimetry import correct_p05023_covariance

    raw = {
        "HHHH": np.array([[10.0]]),
        "HHHV": np.array([[1.0 + 2.0j]]),
        "HHVH": np.array([[3.0 - 1.0j]]),
        "HHVV": np.array([[4.0 + 0.5j]]),
        "HVHV": np.array([[5.0]]),
        "HVVH": np.array([[0.5 + 1.0j]]),
        "HVVV": np.array([[2.0 - 0.5j]]),
        "VHVH": np.array([[6.0]]),
        "VHVV": np.array([[1.5 + 0.2j]]),
        "VVVV": np.array([[8.0]]),
    }

    corrected = correct_p05023_covariance(raw)

    angle = np.deg2rad(59.0)

    positive_rotation = np.exp(1j * angle)
    negative_rotation = np.exp(-1j * angle)

    # Terms requiring +59° correction.
    np.testing.assert_allclose(
        corrected["HVVH"],
        raw["HVVH"] * positive_rotation,
    )

    # Terms requiring -59° correction.
    for term in ("HHHV", "HHVV", "VHVV"):
        np.testing.assert_allclose(
            corrected[term],
            raw[term] * negative_rotation,
        )

    # Terms that must remain unchanged.
    unchanged_terms = (
        "HHHH",
        "HHVH",
        "HVHV",
        "HVVV",
        "VHVH",
        "VVVV",
    )

    for term in unchanged_terms:
        np.testing.assert_array_equal(
            corrected[term],
            raw[term]
        )

    # Verify that the input was not modified.
    np.testing.assert_array_equal(
        raw["HVVH"],
        np.array([[0.5 + 1.0j]]),
    )
