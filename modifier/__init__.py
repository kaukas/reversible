from math import floor
from random import sample
from typing import Iterable
from PIL.Image import Image


class BitFlipper:
    def modify(self, image: Image, pixel_count: int = 100):
        dims = image.size
        to_flip = set(sample(range(dims[0] * dims[1]), k=pixel_count))
        self._flip(image, to_flip)
        return sorted(to_flip)

    def unmodify(self, image: Image, flipped_indices: Iterable[int]):
        self._flip(image, flipped_indices)

    def _flip(self, image: Image, indices: Iterable[int]):
        dims = image.size
        for i in indices:
            xy = (floor(i / dims[1]), i % dims[1])
            rgba = image.getpixel(xy)
            if not rgba:
                raise IndexError(f"RGBA value empty at {xy}")
            if isinstance(rgba, float) or isinstance(rgba, int):
                raise IndexError(f"RGBA value invalid at {xy}")
            image.putpixel(
                xy, (~rgba[0] & 0xFF, ~rgba[1] & 0xFF, ~rgba[2] & 0xFF, rgba[3])
            )
