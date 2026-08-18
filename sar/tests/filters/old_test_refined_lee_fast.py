import numpy as np

from sar.filters.refined_lee_fast import (
    refined_lee_filter_image,
)


def test_output_shape():

    rng = np.random.default_rng(42)

    image = rng.random((40, 50))

    filtered = refined_lee_filter_image(
        image,
    )

    assert filtered.shape == image.shape


def test_constant_image():

    image = np.full(
        (40, 40),
        17.5,
    )

    filtered = refined_lee_filter_image(
        image,
    )

    np.testing.assert_allclose(
        filtered,
        image,
        atol=1e-12,
    )

def test_output_is_finite():

    rng = np.random.default_rng(123)

    image = rng.random((40,40))

    filtered = refined_lee_filter_image(
        image,
    )

    assert np.all(
        np.isfinite(filtered)
    )


def test_no_nan():

    rng = np.random.default_rng(123)

    image = rng.random((40,40))

    filtered = refined_lee_filter_image(
        image,
    )

    assert np.all(
        np.isfinite(filtered)
    )


from sar.filters.refined_lee import (
    refined_lee_filter,
)


def test_matches_reference():

    rng = np.random.default_rng(42)

    image = rng.random((25,25))

    padded = np.pad(
        image,
        3,
        mode="reflect",
    )

    expected = np.empty_like(image)

    for row in range(image.shape[0]):

        for col in range(image.shape[1]):

            window = padded[
                row:row+7,
                col:col+7,
            ]

            expected[row, col] = (
                refined_lee_filter(
                    window,
                )
            )

    actual = refined_lee_filter_image(
        image,
    )

    np.testing.assert_allclose(
        actual,
        expected,
        atol=1e-10,
    )