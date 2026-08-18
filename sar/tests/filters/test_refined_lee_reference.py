import numpy as np
import pytest

from sar.filters.refined_lee_geosar import (
    _refined_lee_numpy,
)

from sar.filters.refined_lee import (
    refined_lee_filter,
)

from sar.features.window_views import (
    build_window_view,
)
from sar.filters.refined_lee_geosar import refined_lee
from sar.sar_image import SARImage

def _reference_refined_lee(
    image: np.ndarray,
) -> np.ndarray:
    """
    Run the original Refined Lee implementation
    pixel-by-pixel.
    """

    windows = build_window_view(
        image,
    )

    rows, cols = image.shape

    result = np.empty_like(
        image,
        dtype=float,
    )

    for row in range(rows):

        for col in range(cols):

            result[row, col] = refined_lee_filter(
                windows[row, col]
            )

    return result


# def test_matches_reference(
#     sample_linear_image,
# ):
#     """
#     Vectorized implementation should match the
#     original pixel-wise implementation.
#     """

#     expected = _reference_refined_lee(
#         sample_linear_image.data,
#     )

#     actual = _refined_lee_numpy(
#         sample_linear_image,
#     )

#     # np.testing.assert_allclose(
#     #     actual,
#     #     expected,
#     #     atol=1e-10,
#     #     rtol=1e-10,
#     # )
#     difference = np.abs(
#     actual - expected
#     )
    
#     rows, cols = np.where(
#         difference > 1e-10
#     )
    
#     print("Number of mismatches:", len(rows))
    
#     print("First mismatch:")
    
#     print(
#         rows[0],
#         cols[0],
#     )
    
#     print()
    
#     r = rows[0]
#     c = cols[0]
    
#     print("Expected:", expected[r,c])
    
#     print("Actual:", actual[r,c])
    
#     print("Difference:", difference[r,c])

#     print()

#     print("Centre Pixel")
    
#     print(
#         expected[10,10]
#     )
    
#     print(
#         actual[10,10]
#     )
    
#     print(
#         actual[10,10]-expected[10,10]
#     )

#     print(sample_linear_image.mask.all())
#     print(np.isnan(sample_linear_image.data).any())
#     print(sample_linear_image.data.dtype)
#     print("JJJJJJJJJJJJJJ")
#     result = _refined_lee_numpy(
#     sample_linear_image,
# )

#     print("Manual :", vector_filtered)
    
#     print("Wrapper:", result[10,10])
    
#     print("Reference:", expected[10,10])
    
#     assert False

def test_matches_reference(
    sample_linear_image,
):

    expected = _reference_refined_lee(
        sample_linear_image.data,
    )

    actual = refined_lee(
        sample_linear_image,
    ).data

    np.testing.assert_allclose(
        actual,
        expected,
        atol=1e-6,
        rtol=1e-6,
    )