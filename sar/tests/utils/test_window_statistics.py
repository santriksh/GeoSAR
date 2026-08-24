import numpy as np
from sar.sar_statistics import window_statistics

def test_window_statistics_ignores_nan():

    windows = np.array(
        [
            [
                [1.0, 2.0],
                [np.nan, 3.0],
            ]
        ]
    )

    means, variances = window_statistics(
        windows,
    )

    assert np.isclose(
        means[0],
        2.0,
    )

    assert np.isfinite(
        variances[0]
    )