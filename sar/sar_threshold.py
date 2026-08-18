import numpy as np

from .sar_image import SARImage


def _validate_threshold_image(
    image: SARImage,
) -> None:
    """
    Validate an image before threshold estimation.

    Parameters
    ----------
    image : SARImage

    Raises
    ------
    ValueError
        If the image contains no valid pixels.
    """

    if np.sum(image.mask) == 0:
        raise ValueError(
            "Image contains no valid pixels."
        )


def _compute_histogram(
    image: SARImage,
    bins: int = 256,
    #percentile_range=None,
    percentile_range: tuple[float, float] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute histogram from valid pixels.

    Parameters
    ----------
    image : SARImage

    bins : int

    Returns
    -------
    histogram : ndarray

    bin_centers : ndarray
    """

    values = image.data[image.mask]

    values = values[np.isfinite(values)]

    if percentile_range is not None:

        lower = np.percentile(
            values,
            percentile_range[0]
        )
    
        upper = np.percentile(
            values,
            percentile_range[1]
        )
    
        values = values[
            (values >= lower)
            &
            (values <= upper)
        ]
    
    hist, edges = np.histogram(values,bins=bins,)
    
    centers = (edges[:-1] + edges[1:]) / 2
    
    return hist, centers, edges


def otsu_threshold(
    image: SARImage,
    bins: int = 256,
    percentile_range: tuple[float, float] | None = (0, 99.9),
) -> float:
    """
    Compute Otsu's threshold.

    Parameters
    ----------
    image : SARImage
        Input image.

    bins : int
        Number of histogram bins.

    Returns
    -------
    float
        Otsu threshold.
    """

    _validate_threshold_image(image)

    hist, centers, _ = _compute_histogram(
    image,
    bins=bins,
    percentile_range=percentile_range,
)

    hist = hist.astype(float)

    hist /= hist.sum()

    assert np.isclose(hist.sum(),1.0,)

    omega = np.cumsum(hist)

    mu = np.cumsum(hist * centers)

    mu_total = mu[-1]

    numerator = (mu_total * omega - mu) ** 2

    denominator = (omega * (1 - omega))

    sigma_b = np.divide(numerator,denominator,out=np.zeros_like(numerator),where=denominator > 0,)

    index = np.argmax(sigma_b)
    
    return float(centers[index])