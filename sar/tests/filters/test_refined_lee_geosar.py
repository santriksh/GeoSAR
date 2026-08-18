from sar.filters.refined_lee_geosar import (
    _refined_lee_numpy,refined_lee
)
import numpy as np
from sar.sar_image import SARImage

def test_refined_lee_numpy_shape(
    sample_linear_image,
):

    result = _refined_lee_numpy(
        sample_linear_image,
    )

    assert result.shape == sample_linear_image.shape


from copy import deepcopy

def test_refined_lee_numpy_constant(
    sample_linear_image,
):

    image = deepcopy(
        sample_linear_image,
    )

    image.data = np.full(
        (20,20),
        7.5,
    )

    image.mask = np.ones(
        (20,20),
        dtype=bool,
    )

    # image.metadata.spatial.shape = (
    #     20,
    #     20,
    # )

    result = _refined_lee_numpy(
        image,
    )

    # np.testing.assert_allclose(
    #     result,
    #     image.data,
    #     atol=1e-12,
    # )
    assert np.max(
    np.abs(
        result-image.data
    )
) < 1e-12

def test_refined_lee_returns_sarimage(
    sample_linear_image,
):

    result = refined_lee(
        sample_linear_image,
    )

    assert isinstance(
        result,
        SARImage,
    )


def test_refined_lee_preserves_mask(
    sample_linear_image,
):

    result = refined_lee(
        sample_linear_image,
    )

    np.testing.assert_array_equal(
        result.mask,
        sample_linear_image.mask,
    )


