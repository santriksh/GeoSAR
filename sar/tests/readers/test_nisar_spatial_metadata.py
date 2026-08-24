from affine import Affine

from sar.readers.nisar import NISARReader

def test_spatial_metadata_shape(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_spatial_metadata()

    assert metadata.shape == (50, 50)

    reader.close()


def test_spatial_metadata_resolution(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_spatial_metadata()

    assert metadata.resolution == (20.0, 20.0)

    reader.close()


def test_spatial_metadata_crs(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_spatial_metadata()

    assert metadata.crs.to_epsg() == 32611

    reader.close()


def test_spatial_metadata_transform(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_spatial_metadata()

    assert metadata.transform == Affine(
        20.0,
        0.0,
        500000.0,
        0.0,
        -20.0,
        4100000.0,
    )

    reader.close()


def test_spatial_metadata_bounds(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    metadata = reader._read_spatial_metadata()

    assert metadata.bounds.left == 500000.0
    assert metadata.bounds.top == 4100000.0
    assert metadata.bounds.right == 501000.0
    assert metadata.bounds.bottom == 4099000.0

    reader.close()