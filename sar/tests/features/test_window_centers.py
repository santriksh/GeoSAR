import numpy as np

from sar.features.window import extract_window_centers

from sar.features.window_views import build_window_view
def test_window_centers():

    image = np.arange(
        100,
        dtype=float,
    ).reshape(10,10)

    windows = build_window_view(
        image,
    )

    centres = extract_window_centers(
        windows,
    )

    np.testing.assert_array_equal(
        centres,
        image,
    )