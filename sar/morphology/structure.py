"""
Structuring element utilities.
"""

from __future__ import annotations

from scipy.ndimage import generate_binary_structure


def binary_structure(
    connectivity: int = 2,
):
    """
    Create a binary structuring element.

    Parameters
    ----------
    connectivity

        1 -> 4-connected

        2 -> 8-connected

    Returns
    -------
    ndarray
    """

    if connectivity not in (1, 2):
        raise ValueError(
            "connectivity must be either 1 or 2."
        )

    return generate_binary_structure(
        rank=2,
        connectivity=connectivity,
    )