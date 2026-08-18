from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from sar.constants.refined_lee import (
    DIRECTION_MASKS,
    Direction,
)

"""
Directional statistics used by the Refined Lee filter.
"""
def compute_directional_sums(
    windows: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute directional sums for every window.

    Parameters
    ----------
    windows
        Shape (..., 7, 7)

    Returns
    -------
    ndarray
        Shape (..., 8)
    """

    if windows.shape[-2:] != (7, 7):
        raise ValueError(
            "Last two dimensions must be (7, 7)."
        )

    sums = []

    for direction in Direction:

        selected = windows[
            ...,
            DIRECTION_MASKS[direction],
        ]

        sums.append(
            #selected.sum(axis=-1)
            np.nansum(selected,axis=-1,)
        )

    return np.stack(
        sums,
        axis=-1,
    )


# def compute_directional_means(
#     windows,
# ):

#     sums = directional_sums(
#         windows,
#     )

#     counts = np.array(
#         [
#             np.sum(
#                 DIRECTION_MASKS[d]
#             )
#             for d in Direction
#         ],
#         dtype=float,
#     )

#     return sums / counts


# def compute_directional_variance(
#     windows,
# ):

#     windows_sq = windows**2

#     sum1 = directional_sums(
#         windows,
#     )
    
#     sum2 = directional_sums(
#         windows_sq,
#     )
    
#     means = ...
    
#     variance = (
#         sum2/counts
#         -
#         means**2
#     )

#     return sums / counts


def compute_directional_means(
    windows: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute directional means for every Refined Lee window.

    Parameters
    ----------
    windows
        Shape (..., 7, 7)

    Returns
    -------
    ndarray
        Shape (..., 8)
    """

    sums, counts = (
        compute_directional_accumulators(
            windows,
        )
    )

    return (
        sums
        /
        np.maximum(
            counts,
            1,
        )
    )

def compute_directional_variances(
    windows: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute directional variances for every
    Refined Lee window.

    Parameters
    ----------
    windows
        Shape (..., 7, 7)

    Returns
    -------
    ndarray
        Shape (..., 8)
    """

    sums, counts = (
        compute_directional_accumulators(
            windows,
        )
    )

    sums_sq, _ = (
        compute_directional_accumulators(
            windows ** 2,
        )
    )

    means = (
        sums
        /
        np.maximum(
            counts,
            1,
        )
    )

    variance = (
        sums_sq
        /
        np.maximum(
            counts,
            1,
        )
        -
        means**2
    )

    return np.maximum(
        variance,
        0.0,
    )
    


def compute_directional_accumulators(
    windows: NDArray[np.float64],
) -> tuple[
    NDArray[np.float64],
    NDArray[np.int32],
]:
    """
    Compute directional sums and valid counts.

    Parameters
    ----------
    windows
        Shape (..., 7, 7)

    Returns
    -------
    sums
        Shape (..., 8)

    counts
        Shape (..., 8)
    """
    sums = []

    counts = []

    for direction in Direction:

        selected = windows[
            ...,
            DIRECTION_MASKS[direction],
        ]
    
        sums.append(
            np.nansum(
                selected,
                axis=-1,
            )
        )
    
        counts.append(
            np.sum(
                np.isfinite(
                    selected,
                ),
                axis=-1,
            )
        )

    return (
    np.stack(
        sums,
        axis=-1,
    ),
    np.stack(
        counts,
        axis=-1,
    ),
)

    