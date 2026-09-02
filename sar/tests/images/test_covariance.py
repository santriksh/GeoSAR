import numpy as np
import pytest
from sar.covariance import CovarianceImage
from sar.sar_image import SARImage

def test_covariance_image_construction(sample_linear_image):

    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    assert covariance.hhhh is sample_linear_image
    assert covariance.hhhv is sample_linear_image
    assert covariance.hhvv is sample_linear_image
    assert covariance.hvhv is sample_linear_image
    assert covariance.hvvv is sample_linear_image
    assert covariance.vvvv is sample_linear_image


def test_covariance_image_is_immutable(sample_linear_image):

    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    with pytest.raises(AttributeError):
        covariance.hhhh = sample_linear_image



def test_covariance_image_rejects_mismatched_shapes(
    sample_linear_image,
):

    data = np.ones((10, 10), dtype=np.float32)

    mismatched = SARImage(
        data=data,
        mask=np.ones_like(data, dtype=bool),
        metadata=sample_linear_image.metadata,
    )

    with pytest.raises(
        ValueError,
        match="same shape",
    ):
        CovarianceImage(
            hhhh=sample_linear_image,
            hhhv=sample_linear_image,
            hhvv=sample_linear_image,
            hvhv=sample_linear_image,
            hvvv=sample_linear_image,
            vvvv=mismatched,
        )
######################

def test_covariance_image_channel_access(sample_linear_image):

    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    assert covariance["HHHH"] is covariance.hhhh
    assert covariance["HHHV"] is covariance.hhhv
    assert covariance["HHVV"] is covariance.hhvv
    assert covariance["HVHV"] is covariance.hvhv
    assert covariance["HVVV"] is covariance.hvvv
    assert covariance["VVVV"] is covariance.vvvv


def test_covariance_image_channel_access_is_case_insensitive(
    sample_linear_image,
):

    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    assert covariance["hhhh"] is covariance.hhhh
    assert covariance["HhHv"] is covariance.hhhv


def test_covariance_image_hermitian_access(
    sample_linear_image,
):

    def make_image(value):
        data = np.full(
            sample_linear_image.shape,
            value,
            dtype=np.complex128,
        )

        return SARImage(
            data=data,
            mask=sample_linear_image.mask.copy(),
            metadata=sample_linear_image.metadata,
        )

    hhhv = make_image(2.0 + 3.0j)
    hhvv = make_image(4.0 + 5.0j)
    hvvv = make_image(6.0 + 7.0j)

    covariance = CovarianceImage(
        hhhh=make_image(1.0),
        hhhv=hhhv,
        hhvv=hhvv,
        hvhv=make_image(8.0),
        hvvv=hvvv,
        vvvv=make_image(9.0),
    )

    assert np.allclose(
        covariance["HVHH"].data,
        np.conjugate(hhhv.data),
    )

    assert np.allclose(
        covariance["VVHH"].data,
        np.conjugate(hhvv.data),
    )

    assert np.allclose(
        covariance["VVHV"].data,
        np.conjugate(hvvv.data),
    )


def test_covariance_image_rejects_unknown_channel(
    sample_linear_image,
):

    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    with pytest.raises(KeyError):

        covariance["INVALID"]



def test_covariance_image_hermitian_preserves_metadata_and_mask(
    sample_linear_image,
):
    data = np.full(
        sample_linear_image.shape,
        2.0 + 3.0j,
        dtype=np.complex128,
    )

    hhhv = SARImage(
        data=data,
        mask=sample_linear_image.mask.copy(),
        metadata=sample_linear_image.metadata,
    )

    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=hhhv,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    result = covariance["HVHH"]

    assert np.allclose(
        result.data,
        np.conjugate(hhhv.data),
    )

    assert np.array_equal(
        result.mask,
        hhhv.mask,
    )

    assert result.metadata is hhhv.metadata


def test_covariance_image_matrix_at(
    sample_linear_image,
):
    def make_image(value):
        data = np.full(
            sample_linear_image.shape,
            value,
            dtype=np.complex128,
        )

        return SARImage(
            data=data,
            mask=sample_linear_image.mask.copy(),
            metadata=sample_linear_image.metadata,
        )

    hhhh = make_image(1.0)
    hhhv = make_image(2.0 + 3.0j)
    hhvv = make_image(4.0 + 5.0j)
    hvhv = make_image(6.0)
    hvvv = make_image(7.0 + 8.0j)
    vvvv = make_image(9.0)

    covariance = CovarianceImage(
        hhhh=hhhh,
        hhhv=hhhv,
        hhvv=hhvv,
        hvhv=hvhv,
        hvvv=hvvv,
        vvvv=vvvv,
    )

    matrix = covariance.matrix_at(5, 7)

    expected = np.array(
        [
            [1.0, 2.0 + 3.0j, 4.0 + 5.0j],
            [2.0 - 3.0j, 6.0, 7.0 + 8.0j],
            [4.0 - 5.0j, 7.0 - 8.0j, 9.0],
        ],
        dtype=np.complex128,
    )

    assert matrix.shape == (3, 3)

    assert np.allclose(
        matrix,
        expected,
    )


def test_covariance_image_matrix_at_uses_requested_pixel(
    sample_linear_image,
):
    shape = sample_linear_image.shape

    hhhh_data = np.arange(
        shape[0] * shape[1],
        dtype=np.float64,
    ).reshape(shape)

    hhhh = SARImage(
        data=hhhh_data,
        mask=sample_linear_image.mask.copy(),
        metadata=sample_linear_image.metadata,
    )

    covariance = CovarianceImage(
        hhhh=hhhh,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    row = 3
    col = 7

    matrix = covariance.matrix_at(
        row,
        col,
    )

    assert matrix[0, 0] == hhhh_data[row, col]



def test_covariance_image_matrix_at_rejects_invalid_pixel(
    sample_linear_image,
):
    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    with pytest.raises(IndexError):
        covariance.matrix_at(
            -1,
            0,
        )

    with pytest.raises(IndexError):
        covariance.matrix_at(
            sample_linear_image.height,
            0,
        )

    with pytest.raises(IndexError):
        covariance.matrix_at(
            0,
            sample_linear_image.width,
        )



def test_covariance_matrix_is_hermitian(
    sample_linear_image,
):
    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    matrix = covariance.matrix_at(5, 7)

    assert np.allclose(
        matrix,
        matrix.conj().T,
    )


def test_covariance_image_pauli_rgb_surface(
    sample_linear_image,
):
    def make_image(value, dtype=np.float64):
        data = np.full(
            sample_linear_image.shape,
            value,
            dtype=dtype,
        )

        return SARImage(
            data=data,
            mask=sample_linear_image.mask.copy(),
            metadata=sample_linear_image.metadata,
        )

    covariance = CovarianceImage(
        hhhh=make_image(16.0),
        hhhv=make_image(0.0 + 0.0j, np.complex128),
        hhvv=make_image(16.0 + 0.0j, np.complex128),
        hvhv=make_image(0.0),
        hvvv=make_image(0.0 + 0.0j, np.complex128),
        vvvv=make_image(16.0),
    )

    red, green, blue = covariance.pauli_rgb()

    assert np.allclose(red.data, 0.0)
    assert np.allclose(green.data, 0.0)
    assert np.allclose(blue.data, 32.0)


def test_covariance_image_pauli_rgb_double_bounce(
    sample_linear_image,
):
    def make_image(value, dtype=np.float64):
        data = np.full(
            sample_linear_image.shape,
            value,
            dtype=dtype,
        )

        return SARImage(
            data=data,
            mask=sample_linear_image.mask.copy(),
            metadata=sample_linear_image.metadata,
        )

    covariance = CovarianceImage(
        hhhh=make_image(16.0),
        hhhv=make_image(0.0 + 0.0j, np.complex128),
        hhvv=make_image(-16.0 + 0.0j, np.complex128),
        hvhv=make_image(0.0),
        hvvv=make_image(0.0 + 0.0j, np.complex128),
        vvvv=make_image(16.0),
    )

    red, green, blue = covariance.pauli_rgb()

    assert np.allclose(red.data, 32.0)
    assert np.allclose(green.data, 0.0)
    assert np.allclose(blue.data, 0.0)



def test_covariance_image_pauli_rgb_volume(
    sample_linear_image,
):
    def make_image(value, dtype=np.float64):
        data = np.full(
            sample_linear_image.shape,
            value,
            dtype=dtype,
        )

        return SARImage(
            data=data,
            mask=sample_linear_image.mask.copy(),
            metadata=sample_linear_image.metadata,
        )

    covariance = CovarianceImage(
        hhhh=make_image(0.0),
        hhhv=make_image(0.0 + 0.0j, np.complex128),
        hhvv=make_image(0.0 + 0.0j, np.complex128),
        hvhv=make_image(16.0),
        hvvv=make_image(0.0 + 0.0j, np.complex128),
        vvvv=make_image(0.0),
    )

    red, green, blue = covariance.pauli_rgb()

    assert np.allclose(red.data, 0.0)
    assert np.allclose(green.data, 32.0)
    assert np.allclose(blue.data, 0.0)


def test_covariance_image_pauli_rgb_returns_sar_images(
    sample_linear_image,
):
    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    red, green, blue = covariance.pauli_rgb()

    assert isinstance(red, SARImage)
    assert isinstance(green, SARImage)
    assert isinstance(blue, SARImage)


def test_covariance_image_pauli_rgb_preserves_metadata_and_mask(
    sample_linear_image,
):
    covariance = CovarianceImage(
        hhhh=sample_linear_image,
        hhhv=sample_linear_image,
        hhvv=sample_linear_image,
        hvhv=sample_linear_image,
        hvvv=sample_linear_image,
        vvvv=sample_linear_image,
    )

    red, green, blue = covariance.pauli_rgb()

    for result in (red, green, blue):

        assert result.metadata is sample_linear_image.metadata

        assert np.array_equal(
            result.mask,
            sample_linear_image.mask,
        )