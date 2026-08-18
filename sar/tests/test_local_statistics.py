from sar.sar_filters import _local_statistics
from sar.sar_image import SARImage
def test_local_statistics_returns_images(
    linear_image,
):

    mean, variance = _local_statistics(
        linear_image,
        window_size=5,
    )

    assert isinstance(mean, SARImage)
    assert isinstance(variance, SARImage)


    assert mean.data.shape == linear_image.data.shape
    assert variance.data.shape == linear_image.data.shape