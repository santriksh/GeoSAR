from sar.sar_filters import _local_statistics
from sar.sar_filters import _kuan_weight
from sar.sar_filters import _adaptive_filter_result
from sar.sar_image import SARImage

import numpy as np

def test_adaptive_filter_result_returns_sarimage(linear_image):

    mean, variance = _local_statistics(
        linear_image,
        window_size=5,
    )

    weight = np.ones_like(linear_image.data)

    result = _adaptive_filter_result(
        reference=linear_image,
        mean=mean,
        variance=variance,
        weight=weight,
        operation="test",
    )

    assert isinstance(result, SARImage)
    assert result.value_scale == "Linear"
    assert result.data.shape == linear_image.data.shape