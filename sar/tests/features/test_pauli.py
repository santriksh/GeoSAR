import numpy as np

from sar.features.pauli import pauli_rgb_from_covariance

def test_pauli_rgb_pure_surface():
    hhhh = np.array([[16.0]])
    hhvv = np.array([[16.0 + 0.0j]])
    hvhv = np.array([[0.0]])
    vvvv = np.array([[16.0]])

    red, green, blue = pauli_rgb_from_covariance(
        hhhh,
        hhvv,
        hvhv,
        vvvv,
    )

    assert np.allclose(red, 0.0)
    assert np.allclose(green, 0.0)
    assert np.allclose(blue, 32.0)


def test_pauli_rgb_pure_double_bounce():
    hhhh = np.array([[16.0]])
    hhvv = np.array([[-16.0 + 0.0j]])
    hvhv = np.array([[0.0]])
    vvvv = np.array([[16.0]])

    red, green, blue = pauli_rgb_from_covariance(
        hhhh,
        hhvv,
        hvhv,
        vvvv,
    )

    assert np.allclose(red, 32.0)
    assert np.allclose(green, 0.0)
    assert np.allclose(blue, 0.0)


def test_pauli_rgb_pure_volume():
    hhhh = np.array([[0.0]])
    hhvv = np.array([[0.0 + 0.0j]])
    hvhv = np.array([[16.0]])
    vvvv = np.array([[0.0]])

    red, green, blue = pauli_rgb_from_covariance(
        hhhh,
        hhvv,
        hvhv,
        vvvv,
    )

    assert np.allclose(red, 0.0)
    assert np.allclose(green, 32.0)
    assert np.allclose(blue, 0.0)


def test_pauli_rgb_uses_real_part_of_hhvv():
    hhhh = np.array([[10.0]])
    hhvv = np.array([[2.0 + 3.0j]])
    hvhv = np.array([[4.0]])
    vvvv = np.array([[6.0]])

    red, green, blue = pauli_rgb_from_covariance(
        hhhh,
        hhvv,
        hvhv,
        vvvv,
    )

    assert np.allclose(red, 6.0)
    assert np.allclose(green, 8.0)
    assert np.allclose(blue, 10.0)


def test_pauli_rgb_power_conservation():
    rng = np.random.default_rng(42)

    hhhh = rng.random((5, 5))
    hvhv = rng.random((5, 5))
    vvvv = rng.random((5, 5))

    hhvv = (
        rng.random((5, 5))
        + 1j * rng.random((5, 5))
    )

    red, green, blue = pauli_rgb_from_covariance(
        hhhh,
        hhvv,
        hvhv,
        vvvv,
    )

    expected_span = (
        hhhh
        + vvvv
        + 2.0 * hvhv
    )

    assert np.allclose(
        red + green + blue,
        expected_span,
    )



def test_pauli_rgb_preserves_shape():
    shape = (7, 9)

    hhhh = np.ones(shape)
    hhvv = np.ones(shape, dtype=np.complex128)
    hvhv = np.ones(shape)
    vvvv = np.ones(shape)

    red, green, blue = pauli_rgb_from_covariance(
        hhhh,
        hhvv,
        hvhv,
        vvvv,
    )

    assert red.shape == shape
    assert green.shape == shape
    assert blue.shape == shape