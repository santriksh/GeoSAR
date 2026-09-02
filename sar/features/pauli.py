import numpy as np
from numpy.typing import NDArray


def pauli_rgb_from_covariance(
    hhhh: NDArray[np.float64],
    hhvv: NDArray[np.complex128],
    hvhv: NDArray[np.float64],
    vvvv: NDArray[np.float64],
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
]:
    """
    Compute Pauli RGB intensities from covariance elements.

    Parameters
    ----------
    hhhh
        HH power, i.e. <HH * HH*>.

    hhvv
        HH-VV cross-covariance, i.e. <HH * VV*>.

    hvhv
        HV power, i.e. <HV * HV*>.

    vvvv
        VV power, i.e. <VV * VV*>.

    Returns
    -------
    red, green, blue
        Pauli RGB intensity images.

        Red   -> Double-bounce scattering
        Green -> Volume scattering
        Blue  -> Surface scattering
    """

    red = 0.5 * (
        hhhh
        + vvvv
        - 2.0 * np.real(hhvv)
    )

    green = 2.0 * hvhv

    blue = 0.5 * (
        hhhh
        + vvvv
        + 2.0 * np.real(hhvv)
    )

    return red, green, blue