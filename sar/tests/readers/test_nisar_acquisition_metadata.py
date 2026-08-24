from sar.readers.nisar import NISARReader


def test_platform(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_acquisition_metadata()

    assert metadata.platform == "NISAR"

    reader.close()


def test_sensor(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_acquisition_metadata()

    assert metadata.sensor == "LSAR"

    reader.close()


def test_polarization(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_acquisition_metadata()

    assert metadata.polarization == "HHHH"

    reader.close()


def test_frequency_band(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_acquisition_metadata()

    assert metadata.frequency_band == "frequencyA"

    reader.close()


def test_default_values(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_acquisition_metadata()

    assert metadata.acquisition_date == ""
    assert metadata.orbit_direction == ""
    assert metadata.relative_orbit is None
    assert metadata.beam_mode == ""
    assert metadata.incidence_angle == ""

    reader.close()