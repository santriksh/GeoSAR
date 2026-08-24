from sar.readers.nisar import NISARReader


def test_provenance_operation(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_provenance_metadata()

    assert metadata.operation == "load_nisar"

    reader.close()


def test_provenance_inputs(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_provenance_metadata()

    assert metadata.inputs == [str(sample_nisar_file)]

    reader.close()


def test_provenance_created_by(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._build_provenance_metadata()

    assert metadata.created_by == "GeoSAR"

    reader.close()


