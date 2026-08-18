import pytest
import numpy as np
from sar.sar_filters import gamma_map_filter
from sar.tests.utils import make_test_image


def test_output_shape(noisy_linear_image):
    filtered = gamma_map_filter(
        noisy_linear_image,
    )

    assert filtered.data.shape == noisy_linear_image.data.shape




def test_uniform_image(uniform_linear_image):
    filtered = gamma_map_filter(
        uniform_linear_image,
    )
    
    np.testing.assert_allclose(
        filtered.data,
        uniform_linear_image.data,
    )
    
    assert filtered.metadata.acquisition == uniform_linear_image.metadata.acquisition

    assert filtered.metadata.processing == uniform_linear_image.metadata.processing

    assert filtered.metadata.custom == uniform_linear_image.metadata.custom
    assert (
    filtered.metadata.provenance.operation
    == "gamma_map_filter"
)
    
    assert filtered.crs == uniform_linear_image.crs
    assert filtered.bounds == uniform_linear_image.bounds
    assert filtered.value_scale == "Linear"


def test_invalid_enl(noisy_linear_image):

    with pytest.raises(
        ValueError,
        match="enl must be positive",
    ):
        gamma_map_filter(
            noisy_linear_image,
            enl=0,
        )

def test_requires_linear_image(sample_image):

    with pytest.raises(
        ValueError,
        match="Expected image in Linear scale",
    ):
        gamma_map_filter(
            sample_image,
        )

def test_reduces_variance(noisy_linear_image):

    filtered = gamma_map_filter(
        noisy_linear_image,
        enl=4.0,
    )

    assert (
        filtered.data.var()
        <
        noisy_linear_image.data.var()
    )


def test_preserves_strong_reflector(linear_image):

    image = make_test_image(
        linear_image,
        data=np.array([
            [10,10,10],
            [10,80,10],
            [10,10,10],
        ], dtype=float)
    )

    filtered = gamma_map_filter(
        image,
        window_size=3,
        enl=4.0,
    )

    assert filtered.data[1,1] > 70
