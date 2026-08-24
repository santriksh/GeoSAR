from sar.sar_metadata import SARMetadata
from sar.readers.nisar import NISARReader


def test_build_metadata_returns_sarmetadata(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_metadata()

    assert isinstance(metadata, SARMetadata)

    reader.close()


def test_build_metadata_spatial(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_metadata()

    assert metadata.spatial.shape == (50, 50)

    reader.close()


def test_build_metadata_acquisition(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_metadata()

    assert metadata.acquisition.platform == "NISAR"

    reader.close()


def test_build_metadata_processing(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_metadata()

    assert metadata.processing.processing_level == "L2"

    reader.close()


def test_build_metadata_provenance(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_metadata()

    assert metadata.provenance.operation == "load_nisar"

    reader.close()


def test_build_metadata_custom(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_metadata()

    assert metadata.custom.values == {}

    reader.close()