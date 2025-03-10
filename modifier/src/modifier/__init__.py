from PIL.Image import Image
from typing import Any

from modifier.bit_flipper import BitFlipper


def modify(image: Image):
    return BitFlipper().modify(image)


def unmodify(image: Image, changes: Any):
    BitFlipper().unmodify(image, changes)
