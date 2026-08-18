from .closing import binary_closing
from .connected_components import (
    label_connected_components,
)
from .objects import (
    remove_small_objects,
)
from .opening import binary_opening

__all__ = [
    "binary_closing",
    "binary_opening",
    "label_connected_components",
    "remove_small_objects",
]