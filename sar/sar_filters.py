from numbers import Real

import numpy as np

from sar.sar_geometry import _distance_matrix
from sar.sar_statistics import _weighted_window_mean, coefficient_of_variation

from .sar_image import SARImage
from .sar_radiometry import _create_result
from .sar_statistics import (
    local_mean,
    local_variance,
)

EPS = 1e-10

def mean_filter(
    image: SARImage,
    window_size: int = 5,
) -> SARImage:
    """
    Apply a moving average filter.

    Parameters
    ----------
    image : SARImage

    window_size : int

    Returns
    -------
    SARImage
    """
    mean = local_mean(
    image,
    window_size=window_size
)

    return _create_result(
        reference=image,
        data=mean.data,
        mask=mean.mask,
        operation="mean_filter",
        value_scale=image.value_scale
    )



def estimate_global_noise_variance(
    variance: SARImage,
) -> float:
    """
    Estimate the global speckle noise variance from
    a local variance image.

    Parameters
    ----------
    variance : SARImage
        Local variance image.

    Returns
    -------
    float
        Estimated global noise variance.
    """

    return float(
        np.nanmean(
            variance.data
        )
    )



def _lee_weight(
    local_variance,
    noise_variance,
):

    local_variance = np.asarray(
        local_variance,
        dtype=float,
    )

    noise_variance = np.asarray(
        noise_variance,
        dtype=float,
    )

    if np.any(noise_variance < 0):
        raise ValueError(
            "noise_variance must be non-negative."
        )

    EPSILON = 1e-10

    weight = np.divide(
        local_variance,
        local_variance + noise_variance,
        out=np.zeros_like(local_variance),
        where=(local_variance + noise_variance) > EPSILON,
    )

    return np.clip(
        weight,
        0.0,
        1.0,
    )


def lee_filter(
    image: SARImage,
    window_size: int = 5,
    noise_variance: float | SARImage | None = None,
) -> SARImage:
    """
    Apply the Lee speckle filter.

    Parameters
    ----------
    image : SARImage
        Input SAR image in Linear scale.

    window_size : int
        Moving window size.

    noise_variance : float, SARImage or None, optional
    Noise variance estimate.

      local variance image (default).
    - float: Use a constant noise variance for the
      entire image.
    - SARImage: Use a spatially varying local noise
      variance image.

    Returns
    -------
    SARImage
        Lee filtered image.
    """

    _validate_common_filter_inputs(image, window_size)

    mean, variance = _local_statistics(
    image,
    window_size,
)

    # Determine the noise variance to use

    if noise_variance is None:
    
        # Backward-compatible behaviour
        noise_variance_used = estimate_global_noise_variance(
            variance
        )
    
    elif isinstance(noise_variance, SARImage):
    
        if noise_variance.data.shape != image.data.shape:
            raise ValueError(
                "noise_variance image must have the same "
                "shape as the input image."
            )
    
        noise_variance_used = noise_variance.data
    
    elif isinstance(noise_variance, Real):
    
        noise_variance_used = float(noise_variance)
    
    else:
    
        raise TypeError(
            "noise_variance must be None, "
            "a real number, or a SARImage."
        )
    
    weight = _lee_weight(
        variance.data,
        noise_variance_used,
    )


    return _adaptive_filter_result(
        reference=image,
        mean=mean,
        variance=variance,
        weight=weight,
        operation="lee_filter",
    )

def _lee_weight_original(
    observed_variance: np.ndarray,
    noise_variance: float,
) -> np.ndarray:
    """
    Compute the original Lee (1980) adaptive weight.

    Parameters
    ----------
    observed_variance : np.ndarray
        Local variance of the observed image.

    noise_variance : float
        Estimated noise variance.

    Returns
    -------
    np.ndarray
        Adaptive weights in [0,1].
    """

    if noise_variance <= 0:
        raise ValueError(
            "noise_variance must be positive."
        )

    observed_variance = np.asarray(
        observed_variance,
        dtype=float
    )

    EPSILON = 1e-10

    signal_variance = np.maximum(
        observed_variance - noise_variance,
        0.0
    )

    weight = np.divide(
        signal_variance,
        observed_variance,
        out=np.zeros_like(
            observed_variance,
            dtype=float
        ),
        where=observed_variance > EPSILON
    )

    return np.clip(
        weight,
        0.0,
        1.0
    )
    
def _frost_weights(
    distance: np.ndarray,
    damping: float,
) -> np.ndarray:
    """
    Compute normalized Frost filter weights.

    Parameters
    ----------
    distance : np.ndarray
        Distance matrix.

    damping : float
        Frost damping coefficient.

    Returns
    -------
    np.ndarray
        Normalized weight matrix.
    """

    if damping < 0:
        raise ValueError(
            "damping must be non-negative."
        )

    weights = np.exp(
        -damping * distance
    )

    total = np.sum(weights)

    if total <= 0:
        raise ValueError(
            "Weight normalization failed."
        )

    return weights / total 


def _frost_kernel_table(
    distance: np.ndarray,
    max_damping: float = 10.0,
    step: float = 0.01,
) -> dict[int, np.ndarray]:
    """
    Precompute Frost kernels for a range of damping values.

    Parameters
    ----------
    distance : np.ndarray
        Distance matrix.

    max_damping : float, default=10.0
        Maximum damping value.

    step : float, default=0.01
        Quantization step.

    Returns
    -------
    dict[int, np.ndarray]
        Dictionary mapping an integer damping index
        to a normalized Frost kernel.
    """

    table = {}

    damping = 0.0

    while damping <= max_damping + 1e-12:

        key = round(damping / step)

        table[key] = _frost_weights(
            distance,
            damping,
        )

        damping += step

    return table


def frost_filter(
    image: SARImage,
    window_size: int = 5,
    damping_factor: float = 2.0,
    return_damping: bool = False,
) -> SARImage:
    """
    Apply the Frost speckle filter.

    Parameters
    ----------
    image : SARImage
        Input SAR image in Linear scale.

    window_size : int, default=5
        Size of the moving window.
        Must be a positive odd integer.

    damping_factor : float, default=2.0
        Controls the strength of smoothing.
        Larger values preserve edges more strongly.

    Returns
    -------
    SARImage
        Frost filtered image.
    """
    MAX_DAMPING = 10.0
    DAMPING_STEP = 0.01
    MAX_INDEX = int(MAX_DAMPING / DAMPING_STEP)
    
    # _validate_filter_inputs(
    #     image=image,
    #     window_size=window_size,
    #     damping_factor=damping_factor,
    #     )

    _validate_common_filter_inputs(image, window_size)
    _validate_frost_inputs(damping_factor)    

    distance = _distance_matrix(
        window_size
    )

    kernel_table = _frost_kernel_table(
    distance,
    max_damping=10.0,
    step=0.01,
)

    # mean = local_mean(
    #     image,
    #     window_size=window_size
    # )

    # variance = local_variance(
    #     image,
    #     window_size=window_size
    # )
    mean, variance = _local_statistics(
    image,
    window_size,
)

    padded_data, padded_mask = _pad_image(
    image,
    window_size,
)

    output = np.full(
        image.data.shape,
        np.nan,
        dtype=float
    )

    rows, cols = image.data.shape

    EPSILON = 1e-10

    damping_image = np.divide(
    damping_factor * variance.data,
    mean.data**2,
    out=np.zeros_like(mean.data),
    where=np.abs(mean.data) > EPSILON,
)

    for row in range(rows):

        for col in range(cols):

            if not image.mask[row, col]:
                continue

            window = _extract_window(
                padded_data,
                padded_mask,
                row,
                col,
                window_size,
            )
            
            local_damping = min(damping_image[row, col],MAX_DAMPING,)

            #key = int(round(local_damping / DAMPING_STEP))
            
            key = min(int(local_damping * 100 + 0.5),MAX_INDEX,)

            weights = kernel_table[key]

            output[row, col] = (
                _weighted_window_mean(
                    window,
                    weights
                )
            )

    mask = (
    image.mask
    &
    np.isfinite(output)
)

    result=_create_result(
        reference=image,
        data=output,
        mask=mask,
        operation="frost_filter",
        value_scale="Linear",
    )

    if return_damping:
        return result, damping_image

    return result

    

def _validate_common_filter_inputs(
    image: SARImage,
    window_size: int,
) -> None:
    """
    Validate inputs common to all SAR filters.
    """

    if image.value_scale != "Linear":
        raise ValueError(
            f"Expected image in Linear scale. "
            f"Found '{image.value_scale}'."
        )

    if window_size < 3:
        raise ValueError(
            "window_size must be at least 3."
        )

    if window_size % 2 == 0:
        raise ValueError(
            "window_size must be odd."
        )


def _validate_frost_inputs(
    damping_factor: float,
) -> None:

    if damping_factor <= 0:
        raise ValueError(
            "damping_factor must be positive."
        )


def _pad_image(
    image: SARImage,
    window_size: int,
    mode: str = "reflect",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Pad image data and mask.

    Parameters
    ----------
    image : SARImage
        Input image.

    window_size : int
        Size of the moving window.

    mode : str, default="reflect"
        Padding mode passed to numpy.pad().

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Padded data and padded mask.
    """

    pad = window_size // 2

    padded_data = np.pad(
        image.data,
        pad_width=pad,
        mode=mode,
    )

    padded_mask = np.pad(
        image.mask,
        pad_width=pad,
        mode=mode,
    )

    return padded_data, padded_mask


def _extract_window(
    padded_data: np.ndarray,
    padded_mask: np.ndarray,
    row: int,
    col: int,
    window_size: int,
) -> np.ndarray:
    """
    Extract a moving window from a padded image.

    Invalid pixels are replaced with NaN.

    Parameters
    ----------
    padded_data : np.ndarray
        Padded image data.

    padded_mask : np.ndarray
        Padded validity mask.

    row : int
        Row index in the original image.

    col : int
        Column index in the original image.

    window_size : int
        Size of the moving window.

    Returns
    -------
    np.ndarray
        Window with invalid pixels replaced by NaN.
    """

    window = padded_data[
        row:row + window_size,
        col:col + window_size
    ]

    mask = padded_mask[
        row:row + window_size,
        col:col + window_size
    ]

    return np.where(
        mask,
        window,
        np.nan
    )


def _local_statistics(
    image: SARImage,
    window_size: int,
) -> tuple[SARImage, SARImage]:
    """
    Compute local mean and local variance.

    Parameters
    ----------
    image : SARImage
        Input SAR image.

    window_size : int
        Size of the moving window.

    Returns
    -------
    tuple[SARImage, SARImage]
        (local_mean, local_variance)
    """
    mean = local_mean(
        image,
        window_size=window_size,
    )

    variance = local_variance(
        image,
        window_size=window_size,
    )

    return mean, variance



def _kuan_weight(
    local_mean,
    local_variance,
    noise_variance,
):
    """
    Compute adaptive Kuan filter weights.
    """
    EPS = 1e-10
    local_mean = np.asarray(local_mean, dtype=float)
    local_variance = np.asarray(local_variance, dtype=float)
    noise_variance = np.asarray(noise_variance, dtype=float)

    if np.any(noise_variance < 0):
        raise ValueError(
            "noise_variance must be non-negative."
        )

    cv2 = np.divide(
        local_variance,
        local_mean**2,
        out=np.zeros_like(local_variance),
        where=np.abs(local_mean) > EPS,
    )

    cn2 = np.divide(
        noise_variance,
        local_mean**2,
        out=np.zeros_like(local_variance),
        where=np.abs(local_mean) > EPS,
    )

    weight = np.divide(
        1.0 - (cn2 / (cv2 + EPS)),
        1.0 + cn2,
        out=np.zeros_like(cv2),
        where=cv2 > EPS,
    )

    return np.clip(weight, 0.0, 1.0)


def _adaptive_filter_result(
    reference: SARImage,
    mean: SARImage,
    variance: SARImage,
    weight: np.ndarray,
    operation: str,
) -> SARImage:
    """
    Construct the output of an adaptive SAR filter.

    Parameters
    ----------
    reference : SARImage
        Original input image.

    mean : SARImage
        Local mean image.

    variance : SARImage
        Local variance image.

    weight : ndarray
        Adaptive filter weights.

    operation : str
        Name of the filtering operation.

    Returns
    -------
    SARImage
        Filtered SAR image.
    """

    if weight.shape != reference.data.shape:
        raise ValueError(
            "weight must have the same shape as the input image."
        )

    data = (
        mean.data
        + weight * (reference.data - mean.data)
    )

    mask = (
        reference.mask
        & mean.mask
        & variance.mask
        & np.isfinite(data)
    )

    return _create_result(
        reference=reference,
        data=data,
        mask=mask,
        operation=operation,
        value_scale="Linear",
    )


def kuan_filter(
    image: SARImage,
    window_size: int = 5,
    noise_variance: float | SARImage | None = None,
) -> SARImage:
    """
    Apply the Lee speckle filter.

    Parameters
    ----------
    image : SARImage
        Input SAR image in Linear scale.

    window_size : int
        Moving window size.

    noise_variance : float, SARImage or None, optional
    Noise variance estimate.

      local variance image (default).
    - float: Use a constant noise variance for the
      entire image.
    - SARImage: Use a spatially varying local noise
      variance image.

    Returns
    -------
    SARImage
        Kuan filtered image.
    """

    _validate_common_filter_inputs(image, window_size)

    mean, variance = _local_statistics(
    image,
    window_size,
)

    # Determine the noise variance to use

    if noise_variance is None:
    
        # Backward-compatible behaviour
        noise_variance_used = estimate_global_noise_variance(
            variance
        )
    
    elif isinstance(noise_variance, SARImage):
    
        if noise_variance.data.shape != image.data.shape:
            raise ValueError(
                "noise_variance image must have the same "
                "shape as the input image."
            )
    
        noise_variance_used = noise_variance.data
    
    elif isinstance(noise_variance, Real):
    
        noise_variance_used = float(noise_variance)
    
    else:
    
        raise TypeError(
            "noise_variance must be None, "
            "a real number, or a SARImage."
        )
    
    weight = _kuan_weight(
    mean.data,
    variance.data,
    noise_variance_used,
)



    return _adaptive_filter_result(
    reference=image,
    mean=mean,
    variance=variance,
    weight=weight,
    operation="kuan_filter",
)


def _gamma_map_estimate(
    pixel: np.ndarray,
    mean: np.ndarray,
    alpha: np.ndarray,
    enl: float,
) -> np.ndarray:
    """
    Compute the Gamma-MAP estimate for textured pixels.

    Parameters
    ----------
    pixel : ndarray
        Observed SAR intensity.

    mean : ndarray
        Local mean.

    alpha : ndarray
        Gamma texture parameter.

    enl : float
        Equivalent Number of Looks.

    Returns
    -------
    ndarray
        MAP estimate.
    """

    term = (
        mean**2
        * (alpha - enl - 1.0) ** 2
        + 4.0
        * alpha
        * enl
        * mean
        * pixel
    )

    # Numerical robustness
    term = np.maximum(term, 0.0)

    estimate = np.divide(
    mean * (alpha - enl - 1.0)
    + np.sqrt(term),
    2.0 * alpha,
    out=pixel.copy(),
    where=alpha > EPS,
)

    return estimate


def _gamma_map_alpha(
    cv: np.ndarray,
    enl: float,
) -> np.ndarray:
    """
    Compute the Gamma-MAP texture parameter.
    """

    cu = 1.0 / np.sqrt(enl)

    denominator = cv**2 - cu**2

    alpha = np.divide(
        1.0 + cu**2,
        denominator,
        out=np.zeros_like(cv),
        where=denominator > EPS,
    )

    return alpha

def _gamma_map_masks(
    cv: np.ndarray,
    enl: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Classify pixels into homogeneous, textured and edge regions.

    Parameters
    ----------
    cv : ndarray
        Local coefficient of variation.

    enl : float
        Equivalent Number of Looks.

    Returns
    -------
    homogeneous : ndarray
        Homogeneous-region mask.

    textured : ndarray
        Textured-region mask.

    edge : ndarray
        Edge-region mask.
    """

    cu = 1.0 / np.sqrt(enl)
    cmax = np.sqrt(2.0) * cu

    homogeneous = cv <= cu

    textured = (
        (cv > cu)
        &
        (cv < cmax)
    )

    edge = cv >= cmax

    return homogeneous, textured, edge

def _validate_gamma_map_inputs(
    enl: float,
) -> None:
    """
    Validate Gamma-MAP specific parameters.

    Parameters
    ----------
    enl : float
        Equivalent Number of Looks.

    Raises
    ------
    ValueError
        If ENL is not positive.
    """

    if enl <= 0:
        raise ValueError(
            "enl must be positive."
        )
    
def gamma_map_filter(
    image: SARImage,
    window_size: int = 5,
    enl: float = 1.0,
) -> SARImage:
    """
    Apply the Gamma-MAP adaptive speckle filter.

    Parameters
    ----------
    image : SARImage
        Input image in Linear scale.

    window_size : int, default=5
        Size of the moving window.

    enl : float, default=1.0
        Equivalent Number of Looks of the SAR acquisition.

    Returns
    -------
    SARImage
        Gamma-MAP filtered image.
    """

    _validate_common_filter_inputs(
        image=image,
        window_size=window_size,
    )

    _validate_gamma_map_inputs(
        enl=enl,
    )

    mean = local_mean(
        image,
        window_size,
    )

    cv = coefficient_of_variation(
        image,
        window_size,
    )

    alpha = _gamma_map_alpha(
        cv=cv.data,
        enl=enl,
    )

    homogeneous, textured, _edge = _gamma_map_masks(
        cv=cv.data,
        enl=enl,
    )

    estimate = _gamma_map_estimate(
        pixel=image.data,
        mean=mean.data,
        alpha=alpha,
        enl=enl,
    )

    output = image.data.copy()

    output[homogeneous] = mean.data[homogeneous]

    output[textured] = estimate[textured]

    mask = (
        image.mask
        & mean.mask
        & cv.mask
        & np.isfinite(output)
    )

    return _create_result(
        reference=image,
        data=output,
        mask=mask,
        operation="gamma_map_filter",
    )