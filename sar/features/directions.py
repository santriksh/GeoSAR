

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def dominant_gradient(
    gradients: NDArray[np.float64],
) -> NDArray[np.int64]:
    """
    Return the index of the dominant
    composite gradient.

    Parameters
    ----------
    gradients
        Shape (...,4)

    Returns
    -------
    ndarray
        Shape (...)
    """

    return np.argmax(
    gradients,
    axis=-1,
)