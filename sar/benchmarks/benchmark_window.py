from time import perf_counter

import numpy as np

from sar.processing import apply_window_filter


def benchmark_filter(
    image: np.ndarray,
    filter_function,
    *,
    window_size: int,
):
    """
    Benchmark a window filter.
    """

    start = perf_counter()

    output = apply_window_filter(
        image=image,
        filter_function=filter_function,
        window_size=window_size,
    )

    elapsed = perf_counter() - start

    print("=" * 50)
    print(f"Image size : {image.shape}")
    print(f"Window     : {window_size}")
    print(f"Elapsed    : {elapsed:.2f} seconds")
    print("=" * 50)

    return output