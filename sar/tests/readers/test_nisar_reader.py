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
        "frequencyA": ["HHHH"]
    }

    reader.close()


def test_default_frequency(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    assert reader.default_frequency == "frequencyA"

    reader.close()


def test_default_polarization(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    assert reader.default_polarization == "HHHH"

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
        polarization="HHHH",
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

    assert covariance["HVHV"].data[0, 2] == 16.0

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
