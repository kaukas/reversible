from typing import Any
from PIL.Image import Image

from modifier.bit_flipper import BitFlipper


def modify(image: Image):
    return BitFlipper().modify(image)


def unmodify(image: Image, changes: Any):
    BitFlipper().unmodify(image, changes)
