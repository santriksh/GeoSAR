
import numpy as np
from numpy.typing import NDArray

from sar.models.statistics import NeighborhoodStatistics

EPS = 1e-12
_NUM_HOMOGENEOUS_WINDOWS = 5

_SUBWINDOW_OFFSETS = (
    (-2, -2), (-2, 0), (-2, 2),
    ( 0, -2), ( 0, 0), ( 0, 2),
    ( 2, -2), ( 2, 0), ( 2, 2),
)

# REFINED_LEE_WINDOW_SIZE = 7

# REFINED_LEE_CENTER = REFINED_LEE_WINDOW_SIZE // 2

#from sar.constants import refined_lee
from sar.constants.refined_lee import (
    DIRECTION_MASKS,
    REFINED_LEE_CENTER,
    REFINED_LEE_WINDOW_SHAPE,
    SUBWINDOW_OFFSETS,
    Direction,
)
from sar.sar_statistics import window_statistics

# class Direction(IntEnum):
#     """
#     Directional kernels used by the Refined Lee filter.
#     """

#     NORTH = 0
#     EAST = 1
#     NORTH_EAST = 2
#     NORTH_WEST = 3

#     SOUTH = 4
#     WEST = 5
#     SOUTH_WEST = 6
#     SOUTH_EAST = 7

# _DIRECTION_KERNELS = {
# Direction.NORTH: (
#     (-3, 0), (-2, 0), (-1, 0),
#     ( 0, 0),
#     ( 1, 0), ( 2, 0), ( 3, 0),
# ),

# Direction.EAST: (
#     (0, -3), (0, -2), (0, -1),
#     (0,  0),
#     (0,  1), (0,  2), (0,  3),
# ),

# Direction.NORTH_EAST: (
#     (-3, 3), (-2, 2), (-1, 1),
#     ( 0, 0),
#     ( 1,-1), ( 2,-2), ( 3,-3),
# ),

# Direction.NORTH_WEST: (
#     (-3,-3), (-2,-2), (-1,-1),
#     ( 0, 0),
#     ( 1, 1), ( 2, 2), ( 3, 3),
# ),

# # opposite directions reuse the same pixels

# Direction.SOUTH: (
#     (-3, 0), (-2, 0), (-1, 0),
#     ( 0, 0),
#     ( 1, 0), ( 2, 0), ( 3, 0),
# ),

# Direction.WEST: (
#     (0, -3), (0, -2), (0, -1),
#     (0,  0),
#     (0,  1), (0,  2), (0,  3),
# ),

# Direction.SOUTH_WEST: (
#     (-3, 3), (-2, 2), (-1, 1),
#     ( 0, 0),
#     ( 1,-1), ( 2,-2), ( 3,-3),
# ),

# Direction.SOUTH_EAST: (
#     (-3,-3), (-2,-2), (-1,-1),
#     ( 0, 0),
#     ( 1, 1), ( 2, 2), ( 3, 3),
# ),
# }


# def _extract_directional_pixels(
#     window: np.ndarray,
#     direction: Direction,
# ) -> np.ndarray:
#     """
#     Extract the seven pixels lying along the specified
#     directional kernel.

#     Parameters
#     ----------
#     window : ndarray of shape (7, 7)

#     direction : Direction

#     Returns
#     -------
#     ndarray of shape (7,)
#     """
#     if window.shape != (7, 7):
#         raise ValueError(
#             "window must have shape (7, 7)."
#         )

#     offsets = _DIRECTION_KERNELS[direction]

#     return np.array(
#         [
#             window[3 + dr, 3 + dc]
#             for dr, dc in offsets
#         ],
#         dtype=float,
#     )

def _extract_directional_pixels(
    window: np.ndarray,
    direction: Direction,
) -> np.ndarray:
    """
    Extract the pixels belonging to the specified
    directional neighbourhood.

    Parameters
    ----------
    window : ndarray of shape (7, 7)

    direction : Direction

    Returns
    -------
    ndarray of shape (28,)
    """
    if window.shape != REFINED_LEE_WINDOW_SHAPE:
        raise ValueError(
            f"window must have shape {REFINED_LEE_WINDOW_SHAPE}."
        )

    return window[DIRECTION_MASKS[direction]].astype(float)

    
def _extract_subwindows(
    window: np.ndarray,
) -> np.ndarray:
    """
    Extract the nine overlapping 3×3 subwindows from a 7×7 window.

    Parameters
    ----------
    window : ndarray of shape (7, 7)

    Returns
    -------
    ndarray of shape (9, 3, 3)
    """

    if window.shape != (7, 7):
        raise ValueError(
            "window must have shape (7, 7)."
        )

    subwindows = []

    centre = 3

    for row_offset, col_offset in _SUBWINDOW_OFFSETS:

        row = centre + row_offset
        col = centre + col_offset

        subwindows.append(
            window[
                row - 1 : row + 2,
                col - 1 : col + 2,
            ]
        )

    return np.stack(subwindows)


def _estimate_noise_variance(
    means: np.ndarray,
    variances: np.ndarray,
) -> float:
    """
    Estimate the local speckle noise variance from the
    nine 3×3 subwindows.

    Parameters
    ----------
    means : ndarray of shape (9,)
        Mean intensity of each subwindow.

    variances : ndarray of shape (9,)
        Variance of each subwindow.

    Returns
    -------
    float
        Estimated normalized speckle variance.
    """

    if means.shape != (9,):
        raise ValueError(
            "means must have shape (9,)."
        )

    if variances.shape != (9,):
        raise ValueError(
            "variances must have shape (9,)."
        )

    normalized_variance = variances / np.maximum(
        means**2,
        EPS,
    )

    return np.mean(
        np.sort(normalized_variance)[:_NUM_HOMOGENEOUS_WINDOWS]
    )


# def _compute_composite_gradients(means: np.ndarray) -> np.ndarray:
#     """
#     Compute the four composite gradient magnitudes used by the
#     Refined Lee filter.

#     The nine subwindow means are arranged as::

#         M1  M2  M3
#         M4  M5  M6
#         M7  M8  M9

#     The gradients are computed as::

#         g0 = |(M2 - M8) + (M3 - M7)|
#         g1 = |(M6 - M4) + (M9 - M1)|
#         g2 = |(M3 - M7) + (M6 - M4)|
#         g3 = |(M1 - M9) + (M2 - M8)|

#     Parameters
#     ----------
#     means : ndarray of shape (9,)
#         Mean intensity of the nine 3×3 subwindows.

#     Returns
#     -------
#     ndarray of shape (4,)
#         Composite gradient magnitudes.
#     """
#     means = np.asarray(means, dtype=float)

#     if means.shape != (9,):
#         raise ValueError("means must have shape (9,).")

#     grid = means.reshape(3, 3)

#     gradients = np.array(
#         [
#             np.abs((grid[0, 1] - grid[2, 1]) +
#                    (grid[0, 2] - grid[2, 0])),

#             np.abs((grid[1, 2] - grid[1, 0]) +
#                    (grid[2, 2] - grid[0, 0])),

#             np.abs((grid[0, 2] - grid[2, 0]) +
#                    (grid[1, 2] - grid[1, 0])),

#             np.abs((grid[0, 0] - grid[2, 2]) +
#                    (grid[0, 1] - grid[2, 1])),
#         ],
#         dtype=float,
#     )

#     return gradients

def _compute_composite_gradients(
    means: np.ndarray,
) -> np.ndarray:
    """
    Compute the four composite gradient magnitudes used by
    the Refined Lee filter.
    """
    return np.abs(
        _compute_signed_composite_gradients(means)
    )


def _mean_grid(means: np.ndarray) -> np.ndarray:
    """
    Reshape the nine subwindow means into a 3×3 grid.

    Parameters
    ----------
    means : ndarray of shape (9,)

    Returns
    -------
    ndarray of shape (3, 3)
    """
    means = np.asarray(means, dtype=float)

    if means.shape != (9,):
        raise ValueError("means must have shape (9,).")

    return means.reshape(3, 3)

def _gradient_direction(means: np.ndarray) -> Direction:
    """
    Determine the dominant Refined Lee edge direction.

    Parameters
    ----------
    means : ndarray of shape (9,)
        Mean intensity of the nine 3×3 subwindows.

    Returns
    -------
    int
        Direction index in the range [0, 7].
    """
    signed = _compute_signed_composite_gradients(means)

    dominant = np.argmax(np.abs(signed))
    
    return dominant if signed[Direction(dominant)] >= 0 else Direction(dominant + 4)
    # grid = _mean_grid(means)

    # # Composite gradient magnitudes
    # gradients = _compute_composite_gradients(means)

    # dominant = int(np.argmax(gradients))

    # # Signed composite differences
    # signed = np.array(
    #     [
    #         (grid[0, 1] - grid[2, 1]) +
    #         (grid[0, 2] - grid[2, 0]),

    #         (grid[1, 2] - grid[1, 0]) +
    #         (grid[2, 2] - grid[0, 0]),

    #         (grid[0, 2] - grid[2, 0]) +
    #         (grid[1, 2] - grid[1, 0]),

    #         (grid[0, 0] - grid[2, 2]) +
    #         (grid[0, 1] - grid[2, 1]),
    #     ]
    # )

    # if signed[dominant] >= 0:
    #     return dominant

    # return dominant + 4


def _compute_signed_composite_gradients(
    means: np.ndarray,
) -> np.ndarray:
    """
    Compute the four signed composite gradients used by the
    Refined Lee filter.

    The nine subwindow means are arranged as::

        M1  M2  M3
        M4  M5  M6
        M7  M8  M9

    The signed composite gradients are::

        g0 = (M2 - M8) + (M3 - M7)
        g1 = (M6 - M4) + (M9 - M1)
        g2 = (M3 - M7) + (M6 - M4)
        g3 = (M1 - M9) + (M2 - M8)

    Parameters
    ----------
    means : ndarray of shape (9,)
        Mean intensity of the nine 3×3 subwindows.

    Returns
    -------
    ndarray of shape (4,)
        Signed composite gradients.
    """
    grid = _mean_grid(means)

    return np.array(
        [
            (grid[0, 1] - grid[2, 1]) +
            (grid[0, 2] - grid[2, 0]),

            (grid[1, 2] - grid[1, 0]) +
            (grid[2, 2] - grid[0, 0]),

            (grid[0, 2] - grid[2, 0]) +
            (grid[1, 2] - grid[1, 0]),

            (grid[0, 0] - grid[2, 2]) +
            (grid[0, 1] - grid[2, 1]),
        ],
        dtype=float,
    )


def _directional_statistics(
    window: np.ndarray,
    direction: Direction,
) -> tuple[float, float]:
    """
    Compute the directional mean and variance for a 7×7 window.

    Parameters
    ----------
    window : ndarray of shape (7, 7)
        Local neighbourhood centred on the target pixel.

    direction : Direction
        Direction along which statistics are computed.

    Returns
    -------
    mean : float
        Mean of the directional pixels.

    variance : float
        Variance of the directional pixels.
    """
    pixels = _extract_directional_pixels(
        window,
        direction,
    )
    # print("%%%%%%%%%%%%%%%%%")
    # print(len(pixels))
    # print(np.unique(pixels, return_counts=True))
    # print("%%%%%%%%%%%%%%%%%")
    return (
        float(np.mean(pixels)),
        float(np.var(pixels)),
    )


def _estimate_signal_variance(
    statistics: NeighborhoodStatistics,
) -> float:
    """
    Estimate the underlying signal variance.

    Parameters
    ----------
    observed_mean : float
        Mean of the observed neighbourhood.

    observed_variance : float
        Variance of the observed neighbourhood.

    noise_variance : float
        Estimated speckle noise variance.

    Returns
    -------
    float
        Non-negative estimate of the signal variance.

    Notes
    -----
    The observed variance contains contributions from both the
    underlying backscatter and multiplicative speckle noise.
    This function removes the expected noise contribution using
    the Lee MMSE model.

    References
    ----------
    Lee, J. S. (1981)
    Lee & Pottier (2009)
    ESA SNAP RefinedLee.java
    """

    signal_variance = (
        statistics.variance
        - statistics.mean**2 * statistics.noise_variance
    ) / (1.0 + statistics.noise_variance)

    return max(signal_variance, 0.0)



def _adaptive_weight(
    signal_variance: float,
    observed_variance: float,
) -> float:
    """
    Compute the adaptive MMSE weight.

    Parameters
    ----------
    signal_variance : float
        Estimated variance of the underlying signal.

    observed_variance : float
        Variance of the observed neighbourhood.

    Returns
    -------
    float
        Adaptive MMSE weight.
    """

    if observed_variance <= EPS:
        return 0.0

    return signal_variance / observed_variance


def _mmse_estimate(
    center_pixel: float,
    local_mean: float,
    weight: float,
) -> float:
    """
    Compute the minimum mean square error (MMSE) estimate.

    Parameters
    ----------
    center_pixel : float
        Observed value of the centre pixel.

    local_mean : float
        Mean of the selected neighbourhood.

    weight : float
        Adaptive MMSE weight.

    Returns
    -------
    float
        Filtered pixel estimate.
    """
    return local_mean + weight * (center_pixel - local_mean)


def refined_lee_filter(
    window: NDArray[np.float64],
) -> float:
    """
    Apply the Refined Lee filter to a 7×7 neighbourhood.

    Parameters
    ----------
    window : NDArray[np.float64]
        A 7×7 SAR intensity window.

    Returns
    -------
    float
        Filtered value of the centre pixel.
    """

    _validate_refined_lee_window(window)

    # Estimate local noise statistics
    subwindows = _extract_subwindows(window)

    means, variances = window_statistics(subwindows)

    # print(means.reshape(3, 3))
    # print(variances.reshape(3, 3))

    noise_variance = _estimate_noise_variance(
        means,
        variances,
    )


    # Determine dominant edge direction
    direction = _gradient_direction(means)


    # Compute statistics for the selected directional neighbourhood
    directional_mean, directional_variance = _directional_statistics(
            window,
            direction,)
    

    statistics = NeighborhoodStatistics(
        mean=directional_mean,
        variance=directional_variance,
        noise_variance=noise_variance,
    )

    # MMSE estimation
    # signal_variance = _estimate_signal_variance(
    #     statistics.mean,
    #     statistics.variance,
    #     statistics.noise_variance,
    # )

    signal_variance = _estimate_signal_variance(statistics)


    weight = _adaptive_weight(
        signal_variance,
        statistics.variance,
    )
   
    return _mmse_estimate(
        center_pixel=window[
        REFINED_LEE_CENTER,
        REFINED_LEE_CENTER,
        ],
        local_mean=statistics.mean,
        weight=weight,
    )


def _validate_refined_lee_window(
    window: NDArray[np.float64],
) -> None:
    """
    Validate that the input is a Refined Lee window.

    Parameters
    ----------
    window : NDArray[np.float64]
        Input window.

    Raises
    ------
    ValueError
        If the window is not square or is not of shape
        (REFINED_LEE_WINDOW_SIZE, REFINED_LEE_WINDOW_SIZE).
    """

    # expected_shape = (
    #     REFINED_LEE_WINDOW_SIZE,
    #     REFINED_LEE_WINDOW_SIZE,
    # )
    expected_shape = REFINED_LEE_WINDOW_SHAPE

    if window.shape != expected_shape:
        raise ValueError(
            f"Expected window shape {expected_shape}, "
            f"got {window.shape}."
        )


def _compute_subwindow_statistics(
    window: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute mean and variance of the nine overlapping
    3×3 windows inside a 7×7 Refined Lee window.

    Returns
    -------
    means : ndarray shape (9,)
    variances : ndarray shape (9,)
    """

    means = np.empty(9, dtype=np.float64)
    variances = np.empty(9, dtype=np.float64)

    for index, (row, col) in enumerate(SUBWINDOW_OFFSETS):

        block = window[
            row : row + 3,
            col : col + 3,
        ]

        means[index] = block.mean()
        variances[index] = block.var()

    return means, variances

def refined_lee_filter_fast(
    window: NDArray[np.float64],
) -> float:
    """
    Apply the Refined Lee filter to a 7×7 neighbourhood.

    Parameters
    ----------
    window : NDArray[np.float64]
        A 7×7 SAR intensity window.

    Returns
    -------
    float
        Filtered value of the centre pixel.
    """

    _validate_refined_lee_window(window)

    # Estimate local noise statistics
    # subwindows = _extract_subwindows(window)

    # means, variances = window_statistics(subwindows)
    means, variances = _compute_subwindow_statistics(
    window,
    )

    # print(means.reshape(3, 3))
    # print(variances.reshape(3, 3))

    noise_variance = _estimate_noise_variance(
        means,
        variances,
    )


    # Determine dominant edge direction
    direction = _gradient_direction(means)


    # Compute statistics for the selected directional neighbourhood
    directional_mean, directional_variance = _directional_statistics(
            window,
            direction,)
    

    statistics = NeighborhoodStatistics(
        mean=directional_mean,
        variance=directional_variance,
        noise_variance=noise_variance,
    )

    # MMSE estimation
    # signal_variance = _estimate_signal_variance(
    #     statistics.mean,
    #     statistics.variance,
    #     statistics.noise_variance,
    # )

    signal_variance = _estimate_signal_variance(statistics)


    weight = _adaptive_weight(
        signal_variance,
        statistics.variance,
    )
   
    return _mmse_estimate(
        center_pixel=window[
        REFINED_LEE_CENTER,
        REFINED_LEE_CENTER,
        ],
        local_mean=statistics.mean,
        weight=weight,
    )
    