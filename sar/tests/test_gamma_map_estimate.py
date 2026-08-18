import numpy as np

from sar.sar_filters import _gamma_map_estimate


# def test_homogeneous_region_returns_mean():
#     pixel = np.array([[12.0]])
#     mean = np.array([[10.0]])
#     cv = np.array([[0.2]])      # Low variation
#     enl = 4.0

#     result = _gamma_map_estimate(
#         pixel=pixel,
#         mean=mean,
#         cv=cv,
#         enl=enl,
#     )

#     np.testing.assert_allclose(result, mean)


# def test_edge_region_returns_original_pixel():
#     pixel = np.array([[25.0]])
#     mean = np.array([[10.0]])
#     cv = np.array([[1.0]])      # High variation
#     enl = 4.0

#     result = _gamma_map_estimate(
#         pixel=pixel,
#         mean=mean,
#         cv=cv,
#         enl=enl,
#     )

#     np.testing.assert_allclose(result, pixel)


# def test_textured_region_placeholder_returns_mean():
#     pixel = np.array([[18.0]])
#     mean = np.array([[10.0]])

#     # Between Cu and Cmax
#     cv = np.array([[0.6]])
#     enl = 4.0

#     result = _gamma_map_estimate(
#         pixel=pixel,
#         mean=mean,
#         cv=cv,
#         enl=enl,
#     )

#    np.testing.assert_allclose(result, mean)


def test_gamma_map_estimate_shape():
    pixel = np.array([[12.0, 15.0]])
    mean = np.array([[10.0, 10.0]])
    alpha = np.array([[5.0, 6.0]])

    estimate = _gamma_map_estimate(
        pixel,
        mean,
        alpha,
        enl=4.0,
    )

    assert estimate.shape == pixel.shape

def test_gamma_map_estimate_finite():
    pixel = np.array([[12.0]])
    mean = np.array([[10.0]])
    alpha = np.array([[5.0]])

    estimate = _gamma_map_estimate(
        pixel,
        mean,
        alpha,
        enl=4.0,
    )

    assert np.isfinite(estimate).all()

    assert np.all(estimate >= 0)
    
    pixel = mean
    
    pixel = np.array([[10.]])
    mean  = np.array([[10.]])
    alpha = np.array([[8.]])

    estimate = _gamma_map_estimate(
    pixel,
    mean,
    alpha,
    enl=4.0,
)
    
   