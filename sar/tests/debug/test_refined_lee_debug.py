from sar.sar_statistics import local_mean
from sar.features.window_views import build_window_view
from sar.features.subwindow_grid import build_subwindow_mean_grid
from sar.features.subwindow_variance_grid import build_subwindow_variance_grid
from sar.filters.refined_lee_geosar import compute_signed_composite_gradients
from sar.filters.refined_lee import _compute_signed_composite_gradients
from sar.filters.refined_lee import _extract_subwindows
import numpy as np
from sar.tests.fixtures import sample_metadata
from copy import deepcopy
from sar.filters.refined_lee_geosar import _compute_mean_grid
ROW = 10
COL = 10

rng = np.random.default_rng(42)

image = rng.random((21,21))

def test_debug_refined_lee(
    sample_linear_image,
):

    windows = build_window_view(image)
    
    window = windows[ROW, COL]
    #########
    # rng = np.random.default_rng(42)
    
    # data = rng.random((21,21)).astype(np.float64)
    
    # mask = np.ones_like(
    #     data,
    #     dtype=bool,
    # )
    
    # metadata = deepcopy(
    #     sample_metadata   # or however you created it
    # )
    
    # metadata.processing.value_scale = "linear"
    
    # sar_image = SARImage(
    #     data=data,
    #     mask=mask,
    #     metadata=metadata,
    # )
    ########
    
    mean_image = local_mean(
        sample_linear_image,
        window_size=3,
    ).data
    
    mean_grid = build_subwindow_mean_grid(
        mean_image,
    )
    
    vector_means = mean_grid[
        ROW,
        COL,
    ].reshape(-1)
    
    
    reference_means = np.array(
        [
            np.mean(patch)
            for patch in _extract_subwindows(window)
        ]
    )
    
    print("\nSubwindow Means")
    
    print(vector_means)
    
    print(reference_means)
    
    np.testing.assert_allclose(
        vector_means,
        reference_means,
        atol=1e-12,
    )

    variance_grid = build_subwindow_variance_grid(
    windows,
)

    vector_variances = variance_grid[
        ROW,
        COL,
    ].reshape(-1)

    reference_variances = np.array(
    [
        np.var(patch)
        for patch in _extract_subwindows(window)
    ]
)

    vector_signed = (
    compute_signed_composite_gradients(
        mean_grid[
            ROW,
            COL,
        ]
    )
)
    reference_signed = (
    _compute_signed_composite_gradients(
        reference_means,
    )
)


def test_integration_step_1(
    sample_linear_image,
):

    manual_mean_image = local_mean(
        sample_linear_image,
        window_size=3,
    ).data

    manual_mean_grid = build_subwindow_mean_grid(
        manual_mean_image,
    )

    wrapper_mean_grid = _compute_mean_grid(
        sample_linear_image,
    )

    print("=" * 60)
    print("INTEGRATION STEP 1")
    print("=" * 60)
    
    print("Manual")
    print(
        manual_mean_grid[10,10]
    )
    
    print()
    
    print("Wrapper")
    print(
        wrapper_mean_grid[10,10]
    )
    
    print()

    np.testing.assert_allclose(
        manual_mean_grid,
        wrapper_mean_grid,
        atol=1e-12,
    )

from sar.features.window_views import build_window_view
from sar.features.directional_statistics import (
    compute_directional_means,
    compute_directional_variances,
)
from sar.filters.refined_lee import (
    _directional_statistics,
)
def test_all_direction_statistics_match(
    sample_linear_image,
):

    ROW = 10
    COL = 10
    
    windows = build_window_view(
        sample_linear_image.data,
    )
    
    window = windows[
        ROW,
        COL,
    ]

    vector_means = compute_directional_means(
    windows,
)[ROW, COL]

    vector_variances = compute_directional_variances(
        windows,
    )[ROW, COL]

    print("\n")
    print("=" * 70)
    print("DIRECTIONAL STATISTICS COMPARISON")
    print("=" * 70)

    for direction in range(8):
    
        scalar_mean, scalar_variance = (
            _directional_statistics(
                window,
                direction,
            )
        )
    
        print()
    
        print(f"Direction {direction}")
    
        print(
            f"Mean      : "
            f"{scalar_mean:.12f}"
        )
    
        print(
            f"Vector    : "
            f"{vector_means[direction]:.12f}"
        )
    
        print(
            f"Difference: "
            f"{scalar_mean - vector_means[direction]:.12e}"
        )
    
        print()
    
        print(
            f"Variance  : "
            f"{scalar_variance:.12f}"
        )
    
        print(
            f"Vector    : "
            f"{vector_variances[direction]:.12f}"
        )
    
        print(
            f"Difference: "
            f"{scalar_variance - vector_variances[direction]:.12e}"
        )
    
        np.testing.assert_allclose(
            scalar_mean,
            vector_means[direction],
            atol=1e-6,
        )
    
        np.testing.assert_allclose(
            scalar_variance,
            vector_variances[direction],
            atol=1e-6,
        )


    
