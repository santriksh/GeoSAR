import numpy as np

from sar.features.window_views import build_window_view

from sar.filters.refined_lee_geosar import (
    _compute_mean_grid,
    _compute_noise_image,
    _compute_direction_image,
    _compute_selected_directional_statistics,
    _refined_lee_numpy,
    compute_signal_variance,
    compute_mmse_weight,
)

from sar.filters.refined_lee import (
    _extract_subwindows,
    window_statistics,
    _estimate_noise_variance,
    _gradient_direction,
    _directional_statistics,
    NeighborhoodStatistics,
    _estimate_signal_variance,
    _adaptive_weight,
    _mmse_estimate,
)

def compare_scalar_vector_pipeline(
    image,
    row,
    col,
):
    windows = build_window_view(
    image.data,
)

    window = windows[
        row,
        col,
    ]

    ##### Scalar pipeline ##########

    subwindows = _extract_subwindows(
    window,
)

    means, variances = window_statistics(
        subwindows,
    )
    
    scalar_noise = _estimate_noise_variance(
        means,
        variances,
    )
    
    scalar_direction = _gradient_direction(
        means,
    )
    
    (
        scalar_mean,
        scalar_variance,
    ) = _directional_statistics(
        window,
        scalar_direction,
    )
    
    scalar_statistics = NeighborhoodStatistics(
        mean=scalar_mean,
        variance=scalar_variance,
        noise_variance=scalar_noise,
    )
    
    scalar_signal = _estimate_signal_variance(
        scalar_statistics,
    )
    
    scalar_weight = _adaptive_weight(
        scalar_signal,
        scalar_variance,
    )
    
    scalar_filtered = _mmse_estimate(
        center_pixel=window[3,3],
        local_mean=scalar_mean,
        weight=scalar_weight,
    )

    ###### Vector Pipeline #######

    mean_grid = _compute_mean_grid(
    image,
)

    noise = _compute_noise_image(
        mean_grid,
        windows,
    )
    
    directions = _compute_direction_image(
        mean_grid,
    )
    
    (
        directional_mean,
        directional_variance,
    ) = _compute_selected_directional_statistics(
        windows,
        directions,
    )
    
    signal = compute_signal_variance(
        directional_mean,
        directional_variance,
        noise,
    )
    
    weight = compute_mmse_weight(
        signal,
        directional_variance,
    )
    
    filtered = _refined_lee_numpy(
        image,
    )

    print()
    print("=" * 80)
    print(f"PIXEL ({row},{col})")
    print("=" * 80)
    
    print(
        f"{'Quantity':25}"
        f"{'Scalar':>18}"
        f"{'Vector':>18}"
        f"{'Difference':>18}"
    )
    
    print("-" * 80)

    def show(name, s, v):

        print(
            f"{name:25}"
            f"{s:18.12f}"
            f"{v:18.12f}"
            f"{(s-v):18.12e}"
        )

    show(
    "Noise",
    scalar_noise,
    noise[row,col],
)

    print()
    
    print(
        f"{'Direction':25}"
        f"{scalar_direction:18}"
        f"{int(directions[row,col]):18}"
    )
    
    print()
    
    show(
        "Directional Mean",
        scalar_mean,
        directional_mean[row,col],
    )
    
    show(
        "Directional Variance",
        scalar_variance,
        directional_variance[row,col],
    )
    
    show(
        "Signal Variance",
        scalar_signal,
        signal[row,col],
    )
    
    show(
        "Weight",
        scalar_weight,
        weight[row,col],
    )
    
    show(
        "Filtered",
        scalar_filtered,
        filtered[row,col],
    )

    
def test_pipeline(
    sample_linear_image,
):

    compare_scalar_vector_pipeline(
        sample_linear_image,
        row=3,
        col=3,
    )    
