import numpy as np

def correct_p05023_covariance(
    covariance: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    """
    Apply the P05023 polarization-orientation phase correction.

    The correction applies phase rotations to selected complex
    covariance terms:

        +59 degrees:
            HVVH

        -59 degrees:
            HHHV
            HHVV
            VHVV

    All other covariance terms are left unchanged.

    A new dictionary is returned. The input covariance dictionary
    and its arrays are not modified.
    """

    angle = np.deg2rad(59.0)

    positive_rotation = np.exp(1j * angle)
    negative_rotation = np.exp(-1j * angle)

    corrected = {
        term: array.copy()
        for term, array in covariance.items()
    }

    corrected["HVVH"] = covariance["HVVH"] * positive_rotation

    for term in ("HHHV", "HHVV", "VHVV"):
        corrected[term] = covariance[term] * negative_rotation

    return corrected

def symmetrize_nisar_covariance(
    data: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    """
    Convert the raw NISAR 4-channel covariance representation
    into the six independent elements of a symmetrized 3x3
    covariance matrix.

    Parameters
    ----------
    data:
        Dictionary containing the required raw NISAR covariance
        terms:
        HHHH, HHHV, HHVH, HHVV, HVHV, HVVH, HVVV, VHVV, VVVV.

    Returns
    -------
    dict[str, np.ndarray]
        Six independent covariance terms:
        HHHH, HHHV, HHVV, HVHV, HVVV, VVVV.

    Notes
    -----
    The symmetrization is performed at the scattering-vector level:

        s_HV_sym = (s_HV + s_VH) / 2

    The resulting covariance matrix is therefore:

        G3 = A C4 A^H

    where A performs the HV/VH averaging.
    """
    required = {
        "HHHH",
        "HHHV",
        "HHVH",
        "HHVV",
        "HVHV",
        "HVVH",
        "HVVV",
        "VHVV",
        "VHVH",
        "VVVV",
    }

    missing = required - data.keys()

    if missing:
        raise ValueError(
            f"Missing required NISAR covariance terms: "
            f"{sorted(missing)}"
        )

    return {
        "HHHH": data["HHHH"],
        "HHHV": (
            data["HHHV"] + data["HHVH"]
        ) / 2.0,
        "HHVV": data["HHVV"],
        "HVHV": (
            data["HVHV"]
            + data["VHVH"]
            + 2.0 * np.real(data["HVVH"])
        ) / 4.0,
        "HVVV": (
            data["HVVV"] + data["VHVV"]
        ) / 2.0,
        "VVVV": data["VVVV"],
    }
