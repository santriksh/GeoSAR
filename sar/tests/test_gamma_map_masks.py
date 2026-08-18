import numpy as np

from sar.sar_filters import _gamma_map_masks


def test_homogeneous_mask():

    cv = np.array([[0.2]])

    homogeneous, textured, edge = _gamma_map_masks(
        cv=cv,
        enl=4.0,
    )

    assert homogeneous[0, 0]
    assert not textured[0, 0]
    assert not edge[0, 0]


def test_textured_mask():

    cv = np.array([[0.6]])

    homogeneous, textured, edge = _gamma_map_masks(
        cv=cv,
        enl=4.0,
    )

    assert textured[0, 0]
    assert not homogeneous[0, 0]
    assert not edge[0, 0]


def test_edge_mask():

    cv = np.array([[1.2]])

    homogeneous, textured, edge = _gamma_map_masks(
        cv=cv,
        enl=4.0,
    )

    assert edge[0, 0]
    assert not homogeneous[0, 0]
    assert not textured[0, 0]

def test_masks_partition():

    cv = np.array([[0.2, 0.6, 1.2]])

    homogeneous, textured, edge = _gamma_map_masks(
        cv=cv,
        enl=4.0,
    )

    classification = (
        homogeneous.astype(int)
        + textured.astype(int)
        + edge.astype(int)
    )

    np.testing.assert_array_equal(
        classification,
        np.ones_like(classification),
    )