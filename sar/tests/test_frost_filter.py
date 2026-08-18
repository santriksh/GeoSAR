import numpy as np
import pytest

from sar.sar_filters import frost_filter
from sar.tests.utils import clone_image

from copy import deepcopy

# def test_uniform_image(linear_image):

#     image = deepcopy(linear_image)

#     image.data[:] = 1.0
#     image.mask[:] = True

#     filtered = frost_filter(image)

#     np.testing.assert_allclose(
#         filtered.data,
#         image.data,
#         atol=1e-6,
#     )
def test_uniform_image(uniform_linear_image):

    filtered = frost_filter(uniform_linear_image)

    np.testing.assert_allclose(
        filtered.data,
        uniform_linear_image.data,
    )

def test_output_shape(linear_image):

    filtered = frost_filter(linear_image)

    assert filtered.shape == linear_image.shape


def test_variance_reduction(noisy_linear_image):

    filtered = frost_filter(noisy_linear_image)

    #assert filtered.data.var() < noisy_linear_image.data.var()
    assert np.nanvar(filtered.data) < noisy_linear_image.data.var()

def test_mean_preservation(noisy_linear_image):

    filtered = frost_filter(noisy_linear_image)

    #assert filtered.data.mean() == pytest.approx(noisy_linear_image.data.mean(),rel=0.02,)
    assert np.nanmean(filtered.data) == pytest.approx(noisy_linear_image.data.mean(),rel=0.02,)


def test_invalid_window_size(small_linear_image):

    #image = np.ones((5,5))
    image = clone_image(small_linear_image)

    with pytest.raises(ValueError):

        frost_filter(
            image,
            window_size=4,
        )


def test_invalid_damping(small_linear_image):

    #image = np.ones((5,5))
    image = clone_image(small_linear_image)
    
    with pytest.raises(ValueError):

        frost_filter(
            image,
            damping_factor=-1,
        )


def test_nan_handling(small_linear_image):

    image = clone_image(small_linear_image)

    image.data[1,1] = np.nan
    
    filtered = frost_filter(image)
    
    assert filtered.shape == image.shape


def test_deterministic(noisy_linear_image):

    from copy import deepcopy

    img1 = deepcopy(noisy_linear_image)
    img2 = deepcopy(noisy_linear_image)

    out1 = frost_filter(img1)
    out2 = frost_filter(img2)

    np.testing.assert_allclose(
        out1.data,
        out2.data,
    )
