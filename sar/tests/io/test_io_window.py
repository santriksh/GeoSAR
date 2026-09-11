import pytest

from sar.io.window import Window


def test_window_shape():

    window = Window(
        row_start=10,
        row_stop=30,
        col_start=20,
        col_stop=50,
    )

    assert window.height == 20
    assert window.width == 30
    assert window.shape == (20, 30)


def test_window_slices():

    window = Window(
        row_start=10,
        row_stop=30,
        col_start=20,
        col_stop=50,
    )

    assert window.rows == slice(10, 30)
    assert window.cols == slice(20, 50)


def test_window_rejects_negative_start():

    with pytest.raises(
        ValueError,
        match="non-negative",
    ):
        Window(
            row_start=-1,
            row_stop=10,
            col_start=0,
            col_stop=10,
        )


def test_window_rejects_invalid_row_range():

    with pytest.raises(
        ValueError,
        match="row_stop",
    ):
        Window(
            row_start=10,
            row_stop=10,
            col_start=0,
            col_stop=10,
        )


def test_window_rejects_invalid_column_range():

    with pytest.raises(
        ValueError,
        match="col_stop",
    ):
        Window(
            row_start=0,
            row_stop=10,
            col_start=10,
            col_stop=10,
        )


def test_window_rejects_non_integer_coordinates():

    with pytest.raises(
        TypeError,
        match="integers",
    ):
        Window(
            row_start=0.5,
            row_stop=10,
            col_start=0,
            col_stop=10,
        )