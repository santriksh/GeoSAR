from sar.readers.nisar import NISARReader


def test_processing_level(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_processing_metadata()

    assert metadata.processing_level == "L2"

    reader.close()


def test_product_type(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_processing_metadata()

    assert metadata.product_type == "GCOV"

    reader.close()


def test_value_scale(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_processing_metadata()

    assert metadata.value_scale == "Linear"

    reader.close()


def test_terrain_corrected(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_processing_metadata()

    assert metadata.terrain_corrected is True

    reader.close()

def test_speckle_filtered(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_processing_metadata()

    assert metadata.speckle_filtered is False

    reader.close()