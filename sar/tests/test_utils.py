import numpy as np

from .utils import make_test_image


# def test_make_test_image(sample_image):

#     data = np.ones((20, 30), dtype=np.float32)

#     image = make_test_image(
#         template=sample_image,
#         data=data,
#     )

#     assert image.data.shape == (20, 30)
#     assert image.mask.shape == (20, 30)
#     assert image.value_scale == "Linear"
#     assert image.metadata.spatial.shape == (20, 30)

def test_make_test_image_replaces_data(sample_image):

    data = np.ones((20, 30), dtype=np.float32)

    image = make_test_image(
        template=sample_image,
        data=data,
    )

    assert image.data.shape == (20, 30)
    assert np.array_equal(image.data, data)


def test_make_test_image_updates_shape(sample_image):

    data = np.ones((25, 40), dtype=np.float32)

    image = make_test_image(
        template=sample_image,
        data=data,
    )

    assert image.metadata.spatial.shape == (25, 40)

def test_make_test_image_updates_value_scale(sample_image):

    image = make_test_image(
        template=sample_image,
        value_scale="Linear",
    )

    assert image.value_scale == "Linear"

def test_make_test_image_preserves_metadata(sample_image):

    image = make_test_image(template=sample_image)

    assert image.crs == sample_image.crs
    assert image.transform == sample_image.transform
    assert image.metadata.acquisition == sample_image.metadata.acquisition
    assert image.metadata.provenance == sample_image.metadata.provenance

