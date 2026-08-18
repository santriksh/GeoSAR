import numpy as np
from sar.features.subwindow_variance_grid import build_subwindow_variance_grid
from sar.features.window_views import build_window_view
from sar.filters.refined_lee import _extract_subwindows

def test_variance_grid_shape():

    image = np.ones((20,20))

    windows = build_window_view(
        image,
    )

    grid = build_subwindow_variance_grid(
        windows,
    )

    assert grid.shape == (20,20,3,3)


def test_variance_grid_constant():

    image = np.full(
        (20,20),
        5.0,
    )

    windows = build_window_view(
        image,
    )

    grid = build_subwindow_variance_grid(
        windows,
    )

    np.testing.assert_allclose(
        grid,
        0.0,
        atol=1e-12,
    )


# def test_variance_grid_matches_reference():

#     rng = np.random.default_rng(42)

#     image = rng.random((30,30))

#     windows = build_window_view(
#         image,
#     )

#     grid = build_subwindow_variance_grid(
#         windows,
#     )

#     for _ in range(100):

#         row = rng.integers(3,27)
#         col = rng.integers(3,27)

#         window = windows[
#             row,
#             col,
#         ]

#         expected = _extract_subwindows(
#             window,
#         )

#         expected = np.array(
#             [
#                 np.var(
#                     patch
#                 )
#                 for patch in expected
#             ]
#         ).reshape(3,3)

#         np.testing.assert_allclose(
#             grid[
#                 row,
#                 col,
#             ],
#             expected,
#             atol=1e-12,
#         )