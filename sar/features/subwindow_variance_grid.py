from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
import numpy as np
from numpy.typing import NDArray


def build_subwindow_variance_grid(
    windows: NDArray[np.float64],
) -> NDArray[np.float64]:
    """
    Compute the variance of each 3×3 subwindow.

    Parameters
    ----------
    windows
        Shape (...,7,7)

    Returns
    -------
    ndarray
        Shape (...,3,3)
    """

    if windows.shape[-2:] != (7,7):
        raise ValueError(
            "Last two dimensions must be (7,7)."
        )

#     print(
#     "NaNs in windows:",
#     np.isnan(windows).sum()
# )
    logger.debug(
    "NaNs in windows: %d",
    np.isnan(windows).sum(),
)

    # print(
    #     "NaNs in first patch:",
    #     np.isnan(
    #         windows[0,0]
    #     ).sum()
    # )
    logger.debug(
    "NaNs in first patch: %d",
    np.isnan(windows[0]).sum(),
)

    variances = np.empty(
        windows.shape[:-2] + (3,3),
        dtype=np.float64,
    )

    for row in range(3):

        for col in range(3):
            row_start = row * 2
            col_start = col * 2

            patch = windows[
                ...,
                row_start:row_start+3,
                col_start:col_start+3,
            ]

            variances[
                ...,
                row,
                col,
            ] = np.nanvar(
                patch,
                axis=(-2,-1),
            )

    return variances