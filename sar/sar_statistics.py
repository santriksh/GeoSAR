

from __future__ import annotations

import numpy as np
from scipy.ndimage import uniform_filter

from .sar_geometry import _create_result, copy_image
from .sar_image import SARImage

#from .sar_statistics import local_mean   # if local_mean is in another module



def local_mean(
    image: SARImage,
    window_size: int = 5,
) -> SARImage:

    """
    Compute the NaN-aware local mean within a moving window.

    Only valid pixels contribute to the mean.

    Parameters
    ----------
    image : SARImage

    window_size : int
    Size of the square moving window.
    Must be an odd positive integer.

    Returns
    -------
    SARImage
    Local mean image.
    """

    valid = (~np.isnan(image.data)).astype(np.float32)

    if window_size % 2 == 0:
        raise ValueError("window_size must be an odd number.")

    if window_size < 1:
        raise ValueError(
        "window_size must be positive."
    )

    filled = np.nan_to_num(
        image.data,
        nan=0
    )
    
    sum_values = (
        uniform_filter(
            filled,
            size=window_size
        )
        *
        window_size**2
    )
    
    count = (
        uniform_filter(
            valid,
            size=window_size
        )
        *
        window_size**2
    )

    data = np.divide(
    sum_values,
    count,
    out=np.full_like(sum_values, np.nan),
    where=count > 0)
    
    #data = sum_values / count
    
    #data[count == 0] = np.nan

    mask = np.isfinite(data)

    

    return _create_result(
    reference=image,
    data=data,
    mask=mask,
    operation="local_mean",
    value_scale=image.value_scale,
)


def local_variance(
    image: SARImage,
    window_size: int = 5,
) -> SARImage:
    """
    Compute the local variance within a moving window.

    Parameters
    ----------
    image : SARImage
        Input SAR image.

    window_size : int
        Size of the square moving window.
        Must be an odd positive integer.

    Returns
    -------
    SARImage
        Local variance image.
    """

    # -----------------------------
    # Validate input
    # -----------------------------
    if window_size < 1:
        raise ValueError(
            "window_size must be positive."
        )

    if window_size % 2 == 0:
        raise ValueError(
            "window_size must be odd."
        )

    # -----------------------------
    # Local mean
    # -----------------------------
    mean = local_mean(
        image,
        window_size=window_size
    )

    # -----------------------------
    # Square image
    # -----------------------------
    squared = copy_image(image)

    squared.data = image.data ** 2

    # -----------------------------
    # Mean of squared image
    # -----------------------------
    mean_square = local_mean(
        squared,
        window_size=window_size
    )

    # -----------------------------
    # Variance
    # -----------------------------
    data = (
        mean_square.data
        -
        mean.data ** 2
    )

    # Numerical precision
    data = np.maximum(
        data,
        0.0
    )

    mask = np.isfinite(data)

    return _create_result(
        reference=image,
        data=data,
        mask=mask,
        operation="local_variance",
        value_scale=image.value_scale
    )


def local_std(
    image: SARImage,
    window_size: int = 5,
) -> SARImage:
    """
    Compute the local standard deviation within a moving window.

    Parameters
    ----------
    image : SARImage
        Input SAR image.

    window_size : int
        Size of the moving window.

    Returns
    -------
    SARImage
        Local standard deviation image.
    """

    variance = local_variance(
        image,
        window_size=window_size
    )

    data = np.sqrt(
        variance.data
    )

    mask = np.isfinite(data)

    return _create_result(
        reference=image,
        data=data,
        mask=mask,
        operation="local_std",
        value_scale=image.value_scale
    )


def coefficient_of_variation(
    image: SARImage,
    window_size: int = 5,
) -> SARImage:
    """
    Compute the local coefficient of variation.

    Parameters
    ----------
    image : SARImage
        Input image in Linear scale.

    window_size : int
        Size of the moving window.

    Returns
    -------
    SARImage
        Coefficient of variation image.
    """
    if window_size < 1:
        raise ValueError(
            "window_size must be positive."
        )

    if window_size % 2 == 0:
        raise ValueError(
            "window_size must be odd."
        )

    if image.value_scale != "Linear":
        raise ValueError(
            "Coefficient of variation requires a Linear image. "
            f"Found '{image.value_scale}'. "
            "Convert using db_to_linear() first."
        )
        
    mean = local_mean(
    image,
    window_size
)

    std = local_std(
    image,
    window_size
)

    #data = std.data / mean.data

    _EPS = 1e-10

    data = np.divide(
    std.data,
    mean.data,
    out=np.full_like(std.data, np.nan),
    where=mean.data > _EPS
)

    #mask = (mean.mask & std.mask & np.isfinite(data))
    mask = (
    image.mask &
    mean.mask &
    std.mask &
    np.isfinite(data)
)

    return _create_result(
    reference=image,
    data=data,
    mask=mask,
    operation="coefficient_of_variation",
    value_scale="Unitless"
)


def equivalent_number_of_looks(
    image: SARImage,
    window_size: int = 5,
) -> SARImage:

    if image.value_scale != "Linear":
        raise ValueError(
            "ENL requires a Linear image. "
            "Convert using db_to_linear() first."
        )


    mean = local_mean(
    image,
    window_size=window_size
    )

    variance = local_variance(
        image,
        window_size=window_size
    )
    
    EPSILON = 1e-10
    
    data = np.divide(
        mean.data ** 2,
        variance.data,
        out=np.full_like(mean.data, np.nan),
        where=variance.data > EPSILON
    )
    
    mask = (
    image.mask &
    mean.mask &
    variance.mask &
    np.isfinite(data)
)
    
    return _create_result(
        reference=image,
        data=data,
        mask=mask,
        operation="equivalent_number_of_looks",
        value_scale="Unitless"
    )


def _local_smallest_mean(
    data: np.ndarray,
    mask: np.ndarray,
    block_size: int,
    n_smallest: int,
) -> np.ndarray:
    """
    Compute the mean of the n smallest valid values
    within a moving window.

    Parameters
    ----------
    data : np.ndarray
        Input image.

    mask : np.ndarray
        Boolean mask of valid pixels.

    block_size : int
        Size of the moving window.

    n_smallest : int
        Number of smallest values to average.

    Returns
    -------
    np.ndarray
        Image containing the local mean of the
        n smallest values.
    """

    if block_size % 2 == 0:
        raise ValueError(
            "block_size must be odd."
        )

    if block_size < 1:
        raise ValueError(
            "block_size must be positive."
        )

    if n_smallest < 1:
        raise ValueError(
            "n_smallest must be positive."
        )

    if n_smallest > block_size * block_size:
        raise ValueError(
            "n_smallest cannot exceed "
            "the number of pixels "
            "in the moving window."
        )

    pad = block_size // 2

    padded_data = np.pad(
        data,
        pad,
        mode="reflect"
    )

    padded_mask = np.pad(
        mask,
        pad,
        mode="reflect"
    )

    output = np.full(
        data.shape,
        np.nan,
        dtype=data.dtype
    )

    rows, cols = data.shape

    for row in range(rows):

        for col in range(cols):

            # Skip invalid center pixel
            if not mask[row, col]:
                continue

            window = padded_data[
                row:row + block_size,
                col:col + block_size
            ]

            window_mask = padded_mask[
                row:row + block_size,
                col:col + block_size
            ]

            #values = window[window_mask]
            #values = window[window_mask & np.isfinite(window)]
            valid = (window_mask & np.isfinite(window))

            values = window[valid]

            if values.size < n_smallest:
                continue

            # smallest = np.partition(
            #     values,
            #     n_smallest - 1
            # )[:n_smallest]

            # output[row, col] = np.mean(
            #     smallest
            # )
            try:
                output[row, col] = _mean_smallest(values,n_smallest)
            except ValueError:
                continue

    return output


def _mean_smallest(
    values: np.ndarray,
    n_smallest: int,
) -> float:
    """
    Compute the mean of the n smallest finite values.

    Parameters
    ----------
    values : np.ndarray
        One-dimensional array.

    n_smallest : int
        Number of smallest values to average.

    Returns
    -------
    float
        Mean of the n smallest finite values.

    Raises
    ------
    ValueError
        If there are insufficient finite values.
    """
    values = np.asarray(values)
    if values.ndim != 1:
        raise ValueError(
            "values must be a 1-D array."
        )

    if n_smallest < 1:
        raise ValueError(
            "n_smallest must be positive."
        )

    values = values[np.isfinite(values)]

    if values.size < n_smallest:
        raise ValueError(
            "Not enough finite values."
        )

    smallest = np.partition(
        values,
        n_smallest - 1
    )[:n_smallest]

    return float(
        np.mean(smallest)
    )


def local_noise_variance(
    image: SARImage,
    window_size: int = 5,
    block_size: int = 7,
    n_smallest: int = 5,
) -> SARImage:
    """
    Estimate the local speckle noise variance.

    The noise variance is estimated by computing the
    local variance image and averaging the n smallest
    variances within a moving window.

    Parameters
    ----------
    image : SARImage
        Input SAR image.

    window_size : int, default=5
        Window used to compute the local variance.

    block_size : int, default=7
        Window used for local noise estimation.

    n_smallest : int, default=5
        Number of smallest variances to average.

    Returns
    -------
    SARImage
        Estimated local noise variance image.
    """

    variance = local_variance(
        image,
        window_size=window_size
    )

    noise = _local_smallest_mean(
        variance.data,
        variance.mask,
        block_size,
        n_smallest,
    )

    return _create_result(
        reference=image,
        data=noise,
        mask=np.isfinite(noise),
        operation="local_noise_variance",
        value_scale=image.value_scale,
    )


# def _weighted_window_mean(
#     values: np.ndarray,
#     weights: np.ndarray,
# ) -> float:
#     """
#     Compute the weighted mean of a window.

#     NaN values are ignored and the remaining weights
#     are renormalized.

#     Parameters
#     ----------
#     values : np.ndarray
#         Window values.

#     weights : np.ndarray
#         Weight matrix.

#     Returns
#     -------
#     float
#         Weighted mean.
#     """

#     values = np.asarray(values, dtype=float)
#     weights = np.asarray(weights, dtype=float)

#     if values.shape != weights.shape:
#         raise ValueError(
#             "values and weights must have the same shape."
#         )

#     valid = np.isfinite(values)

#     if not np.any(valid):
#         return np.nan

#     values = values[valid]
#     weights = weights[valid]

#     weight_sum = np.sum(weights)

#     if weight_sum <= 0:
#         return np.nan

#     weights = weights / weight_sum

#     return float(
#         np.sum(values * weights)
#     )

def _weighted_window_mean(
    values: np.ndarray,
    weights: np.ndarray,
) -> float:
    """
    Compute the weighted mean of a window.

    NaN values are ignored and the remaining
    weights are renormalized.
    """

    if values.shape != weights.shape:
        raise ValueError(
            "values and weights must have the same shape."
        )

    # ----------------------------
    # Fast path
    # ----------------------------

    if np.all(np.isfinite(values)):
        return float(
            np.sum(values * weights)
        )

    # ----------------------------
    # Slow path
    # ----------------------------

    valid = np.isfinite(values)

    if not np.any(valid):
        return np.nan

    values = values[valid]
    weights = weights[valid]

    weight_sum = np.sum(weights)

    if weight_sum <= 0:
        return np.nan

    return float(
        np.sum(
            values * (weights / weight_sum)
        )
    )



def window_statistics(
    windows: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the mean and variance for a stack of windows.

    Parameters
    ----------
    windows : ndarray
        Array of shape (N, H, W), where N is the number of windows.

    Returns
    -------
    means : ndarray
        Mean of each window.

    variances : ndarray
        Variance of each window.
    """

    if windows.ndim != 3:
        raise ValueError(
            "windows must be a 3D array."
        )

    if windows.shape[0] == 0:
        raise ValueError(
            "windows must contain at least one window."
        )

    means = np.nanmean(
        windows,
        axis=(1, 2),
    )

    variances = np.nanvar(
        windows,
        axis=(1, 2),
    )

    return means, variances




    
    


