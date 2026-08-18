import numpy as np
from sar.sar_filters import _gamma_map_alpha

def test_alpha_shape():
    cv = np.array([[0.7, 0.8]])

    alpha = _gamma_map_alpha(
        cv=cv,
        enl=4.0,
    )

    assert alpha.shape == cv.shape


def test_alpha_positive():
    cv = np.array([[0.8]])

    alpha = _gamma_map_alpha(
        cv=cv,
        enl=4.0,
    )

    assert alpha[0, 0] > 0