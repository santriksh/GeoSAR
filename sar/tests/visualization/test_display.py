from sar.visualization.display import display

def test_display_runs(
    sample_linear_image,
):

    display(
        sample_linear_image,
    )


def test_display_db_image(
    db_image,
):

    display(
        db_image,
    )

def test_display_without_stretch(
    sample_linear_image,
):

    display(
        sample_linear_image,
        stretch=False,
    )


def test_display_without_conversion(
    sample_linear_image,
):

    display(
        sample_linear_image,
        convert_linear_to_db=False,
    )


def test_display_with_title(
    sample_linear_image,
):

    display(
        sample_linear_image,
        title="Test",
    )