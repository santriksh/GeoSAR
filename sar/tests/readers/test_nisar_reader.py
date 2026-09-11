"""
Tests for the NISARReader.
"""

from pathlib import Path
import pytest
import h5py
import numpy as np
from sar.readers.nisar import NISARReader
from sar.covariance import CovarianceImage

def test_reader_initialization(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    assert reader.filename == sample_nisar_file

    reader.close()


def test_reader_close(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    reader.close()

    assert not reader.file.id.valid


def test_invalid_product(tmp_path):

    filename = tmp_path / "invalid.h5"

    with h5py.File(filename, "w"):
        pass

    with pytest.raises(
        ValueError,
        match="Invalid NISAR GCOV product",
    ):
        NISARReader(filename)



def test_missing_lsar_group(tmp_path):

    filename = tmp_path / "invalid.h5"

    with h5py.File(filename, "w") as f:

        f.create_group("science")

    with pytest.raises(ValueError):

        NISARReader(filename)



def test_available_frequencies(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    assert reader.frequencies == ["frequencyA"]

    reader.close()



def test_available_polarizations(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    assert reader.polarizations == {
        "frequencyA": ["HH"]
    }

    reader.close()


def test_default_frequency(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    assert reader.default_frequency == "frequencyA"

    reader.close()


def test_default_polarization(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    assert reader.default_polarization == "HH"

    reader.close()


def test_read_image_shape(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader._read_image()

    assert image.shape == (50, 50)

    reader.close()



def test_read_image_dtype(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader._read_image()

    assert image.dtype == np.float32

    reader.close()


def test_read_image_contains_nan(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader._read_image()

    assert np.isnan(image[0, 0])

    reader.close()


def test_read_image_valid_pixels(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader._read_image()

    assert np.isfinite(image[10, 10])

    reader.close()


def test_read_image_explicit_selection(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader._read_image(
        frequency="frequencyA",
        polarization="HH",
    )

    assert image.shape == (50, 50)

    reader.close()


def test_read_covariance_returns_covariance_image(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance()

    assert isinstance(
        covariance,
        CovarianceImage,
    )

    reader.close()


def test_read_covariance_reads_all_channels(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance()

    expected_channels = (
        "HHHH",
        "HHHV",
        "HHVV",
        "HVHV",
        "HVVV",
        "VVVV",
    )

    for channel in expected_channels:

        image = covariance[channel]

        assert image.shape == (3, 3)

    reader.close()


def test_read_covariance_reads_expected_values(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance()

    assert covariance["HHHH"].data[0, 0] == 16.0
    assert covariance["HHVV"].data[0, 0] == 16.0
    assert covariance["HVHV"].data[0, 0] == 0.0
    assert covariance["VVVV"].data[0, 0] == 16.0

    assert covariance["HHVV"].data[0, 1] == -16.0

    assert covariance["HVHV"].data[0, 2] == 8.0

    reader.close()


def test_read_covariance_preserves_complex_channels(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance()

    assert np.iscomplexobj(
        covariance["HHHV"].data
    )

    assert np.iscomplexobj(
        covariance["HHVV"].data
    )

    assert np.iscomplexobj(
        covariance["HVVV"].data
    )

    reader.close()


def test_read_covariance_preserves_spatial_metadata(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance()

    reference = covariance["HHHH"]

    for channel in (
        "HHHV",
        "HHVV",
        "HVHV",
        "HVVV",
        "VVVV",
    ):
        image = covariance[channel]

        assert image.shape == reference.shape
        assert image.crs == reference.crs
        assert image.transform == reference.transform
        assert image.bounds == reference.bounds
        assert image.resolution == reference.resolution

    reader.close()

def test_available_polarizations_realistic_nisar_product(tmp_path):

    filename = tmp_path / "realistic_nisar.h5"

    with h5py.File(filename, "w") as f:

        science = f.create_group("science")
        lsar = science.create_group("LSAR")
        gcov = lsar.create_group("GCOV")
        grids = gcov.create_group("grids")
        frequency = grids.create_group("frequencyA")

        # Actual covariance dataset
        frequency.create_dataset(
            "HHHH",
            data=np.ones((5, 5), dtype=np.float32),
        )

        # NISAR metadata
        frequency.create_dataset(
            "listOfPolarizations",
            data=np.array([b"HH"]),
        )

        frequency.create_dataset(
            "listOfCovarianceTerms",
            data=np.array([b"HHHH"]),
        )

        frequency.create_dataset(
            "mask",
            data=np.zeros((5, 5), dtype=np.uint8),
        )

        frequency.create_dataset(
            "numberOfLooks",
            data=np.ones((5, 5), dtype=np.float32),
        )

        frequency.create_dataset(
            "numberOfSubSwaths",
            data=np.ones((5, 5), dtype=np.uint8),
        )

        frequency.create_dataset(
            "rtcGammaToSigmaFactor",
            data=np.ones((5, 5), dtype=np.float32),
        )

        frequency.create_dataset(
            "xCoordinates",
            data=np.arange(5, dtype=np.float64),
        )

        frequency.create_dataset(
            "yCoordinates",
            data=np.arange(5, dtype=np.float64),
        )

        projection = frequency.create_group("projection")
        projection.attrs["epsg_code"] = 4326

    reader = NISARReader(filename)

    assert reader.polarizations == {
        "frequencyA": ["HH"]
    }

    reader.close()


def test_available_covariance_terms_realistic_nisar_product(tmp_path):

    filename = tmp_path / "realistic_nisar.h5"

    with h5py.File(filename, "w") as f:

        science = f.create_group("science")
        lsar = science.create_group("LSAR")
        gcov = lsar.create_group("GCOV")
        grids = gcov.create_group("grids")
        frequency = grids.create_group("frequencyA")

        frequency.create_dataset(
            "HHHH",
            data=np.ones((5, 5), dtype=np.float32),
        )

        frequency.create_dataset(
            "listOfPolarizations",
            data=np.array([b"HH"]),
        )

        frequency.create_dataset(
            "listOfCovarianceTerms",
            data=np.array([b"HHHH"]),
        )

        frequency.create_dataset(
            "mask",
            data=np.zeros((5, 5), dtype=np.uint8),
        )

        frequency.create_dataset(
            "numberOfLooks",
            data=np.ones((5, 5), dtype=np.float32),
        )

        frequency.create_dataset(
            "numberOfSubSwaths",
            data=np.ones((5, 5), dtype=np.uint8),
        )

        frequency.create_dataset(
            "rtcGammaToSigmaFactor",
            data=np.ones((5, 5), dtype=np.float32),
        )

        frequency.create_dataset(
            "xCoordinates",
            data=np.arange(5, dtype=np.float64),
        )

        frequency.create_dataset(
            "yCoordinates",
            data=np.arange(5, dtype=np.float64),
        )

        projection = frequency.create_group("projection")
        projection.attrs["epsg_code"] = 4326

    reader = NISARReader(filename)

    assert reader.covariance_terms == {
        "frequencyA": ["HHHH"]
    }

    reader.close()


def test_read_covariance_rejects_incomplete_covariance(
    realistic_nisar_file,
):

    reader = NISARReader(realistic_nisar_file)

    with pytest.raises(
        ValueError,
        match="complete covariance",
    ):
        reader.read_covariance()

    reader.close()


def test_covariance_terms_are_incomplete_for_single_pol_product(
    realistic_nisar_file,
):

    reader = NISARReader(realistic_nisar_file)

    assert reader.covariance_terms["frequencyA"] == [
        "HHHH"
    ]

    required_terms = {
        "HHHH",
        "HHHV",
        "HHVV",
        "HVHV",
        "HVVV",
        "VVVV",
    }

    assert set(reader.covariance_terms["frequencyA"]) != required_terms

    reader.close()


def test_read_covariance_symmetrizes_cross_pol_terms(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance()

    # At synthetic pixel (2,2):
    #
    # HHHV = 1 + 2j
    # HHVH = 3 - 1j
    #
    # Symmetrized HHHV:
    #
    # ((1 + 2j) + (3 - 1j)) / 2
    # = 2 + 0.5j

    assert np.allclose(
        covariance["HHHV"].data[2, 2],
        2.0 + 0.5j,
    )

    reader.close()


def test_read_covariance_window_returns_window(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance_window(
        rows=slice(0, 2),
        cols=slice(0, 2),
    )

    assert isinstance(
        covariance,
        CovarianceImage,
    )

    assert covariance["HHHH"].shape == (2, 2)
    assert covariance["HHVV"].shape == (2, 2)
    assert covariance["HVHV"].shape == (2, 2)
    assert covariance["VVVV"].shape == (2, 2)

    reader.close()


    def test_read_covariance_applies_nisar_symmetrization(
        sample_nisar_quadpol_file,
    ):
        reader = NISARReader(
            sample_nisar_quadpol_file,
        )

        covariance = reader.read_covariance()

        # Synthetic fixture:
        #
        # HVHV = 16
        # VHVH = 16
        # HVVH = 0
        #
        # Therefore:
        #
        # HVHV_G3 = (16 + 16 + 2*0) / 4 = 8

        assert np.isclose(
            covariance["HVHV"].data[0, 2],
            8.0,
        )

        # HHHV_G3 = (HHHV + HHVH) / 2
        assert np.isclose(
            covariance["HHHV"].data[0, 2],
            0.0,
        )

        # HVVV_G3 = (HVVV + VHVV) / 2
        assert np.isclose(
            covariance["HVVV"].data[0, 2],
            0.0,
        )

        reader.close()


def test_read_covariance_applies_nisar_symmetrization(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance()

    # Synthetic fixture:
    #
    # HVHV = 16
    # VHVH = 16
    # HVVH = 0
    #
    # Therefore:
    #
    # HVHV_G3 = (16 + 16 + 2*0) / 4 = 8

    assert np.isclose(
        covariance["HVHV"].data[0, 2],
        8.0,
    )

    # HHHV_G3 = (HHHV + HHVH) / 2
    assert np.isclose(
        covariance["HHHV"].data[0, 2],
        0.0,
    )

    # HVVV_G3 = (HVVV + VHVV) / 2
    assert np.isclose(
        covariance["HVVV"].data[0, 2],
        0.0,
    )

    reader.close()


def test_read_covariance_window_applies_orientation_correction(
        sample_nisar_quadpol_file,
    ):
        reader = NISARReader(
            sample_nisar_quadpol_file,
        )

        rows = slice(2, 3)
        cols = slice(2, 3)

        uncorrected = reader.read_covariance_window(
            rows=rows,
            cols=cols,
            frequency="frequencyA",
            orientation_correction=False,
        )

        corrected = reader.read_covariance_window(
            rows=rows,
            cols=cols,
            frequency="frequencyA",
            orientation_correction=True,
        )

        angle = np.deg2rad(59.0)

        expected_hhhv = (
            (1.0 + 2.0j) * np.exp(-1j * angle)
            + (3.0 - 1.0j) * np.exp(0.0j)
        ) / 2.0

        expected_hhvv = (
            (4.0 + 5.0j) * np.exp(-1j * angle)
        )

        expected_hvvv = (
            (1.0 - 2.0j)
            + (3.0 + 4.0j) * np.exp(-1j * angle)
        ) / 2.0

        assert np.allclose(
            corrected["HHHV"].data[0, 0],
            expected_hhhv,
        )

        assert np.allclose(
            corrected["HHVV"].data[0, 0],
            expected_hhvv,
        )

        assert np.allclose(
            corrected["HVVV"].data[0, 0],
            expected_hvvv,
        )

        # The correction must actually change the affected terms.
        assert not np.allclose(
            corrected["HHVV"].data,
            uncorrected["HHVV"].data,
        )

        reader.close()


def test_read_covariance_window_to_pauli_rgb(
    sample_nisar_quadpol_file,
):
    reader = NISARReader(
        sample_nisar_quadpol_file,
    )

    covariance = reader.read_covariance_window(
        rows=slice(2, 3),
        cols=slice(2, 3),
        frequency="frequencyA",
        orientation_correction=True,
    )

    red, green, blue = covariance.pauli_rgb()

    # Corrected G3 terms at synthetic pixel (2,2).
    hhhh = 10.0
    hvhv = 5.0
    vvvv = 12.0

    hhvv = covariance["HHVV"].data[0, 0]

    expected_red = (
        0.5
        * (
            hhhh
            + vvvv
            - 2.0 * np.real(hhvv)
        )
    )
    angle = np.deg2rad(59.0)
    expected_hvhv_g3 = (
        5.0
        + 5.0
        + 2.0 * np.real(
            (2.0 + 3.0j) * np.exp(1j * angle)
        )
    ) / 4.0

    expected_green = 2.0 * expected_hvhv_g3

    #expected_green = 2.0 * hvhv

    expected_blue = (
        0.5
        * (
            hhhh
            + vvvv
            + 2.0 * np.real(hhvv)
        )
    )

    assert np.isclose(
        red.data[0, 0],
        expected_red,
    )

    assert np.isclose(
        green.data[0, 0],
        expected_green,
    )

    assert np.isclose(
        blue.data[0, 0],
        expected_blue,
    )

    reader.close()
