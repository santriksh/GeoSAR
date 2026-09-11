from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    """
    Rectangular pixel window.

    Coordinates follow NumPy slicing conventions:
        row_start <= rows < row_stop
        col_start <= cols < col_stop
    """

    row_start: int
    row_stop: int
    col_start: int
    col_stop: int

    def __post_init__(self):
        values = (
            self.row_start,
            self.row_stop,
            self.col_start,
            self.col_stop,
        )

        if not all(isinstance(value, int) for value in values):
            raise TypeError(
                "Window coordinates must be integers."
            )

        if self.row_start < 0 or self.col_start < 0:
            raise ValueError(
                "Window start coordinates must be non-negative."
            )

        if self.row_stop <= self.row_start:
            raise ValueError(
                "row_stop must be greater than row_start."
            )

        if self.col_stop <= self.col_start:
            raise ValueError(
                "col_stop must be greater than col_start."
            )

    @property
    def height(self) -> int:
        """Number of rows in the window."""
        return self.row_stop - self.row_start

    @property
    def width(self) -> int:
        """Number of columns in the window."""
        return self.col_stop - self.col_start

    @property
    def shape(self) -> tuple[int, int]:
        """Window shape as (rows, columns)."""
        return self.height, self.width

    @property
    def rows(self) -> slice:
        """Return the NumPy row slice."""
        return slice(
            self.row_start,
            self.row_stop,
        )

    @property
    def cols(self) -> slice:
        """Return the NumPy column slice."""
        return slice(
            self.col_start,
            self.col_stop,
        )