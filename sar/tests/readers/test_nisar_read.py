from sar.sar_image import SARImage
from sar.readers.nisar import NISARReader
import numpy as np

def test_read_returns_sarimage(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader.read()

    assert isinstance(image, SARImage)

    reader.close()


def test_read_image_shape(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader.read()

    assert image.shape == (50, 50)

    reader.close()


def test_read_mask(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader.read()

    assert image.mask.shape == (50, 50)

    assert image.mask.dtype == bool

    reader.close()


def test_read_mask_contains_invalid_pixels(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader.read()

    assert not image.mask[0, 0]

    assert image.mask[10, 10]

    reader.close()


def test_read_metadata(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader.read()

    assert image.metadata.acquisition.platform == "NISAR"

    reader.close()


def test_read_statistics(sample_nisar_file):

    reader = NISARReader(sample_nisar_file)

    image = reader.read()

    stats = image.statistics()

    assert stats["valid_pixels"] > 0

    reader.close()