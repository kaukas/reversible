from PIL.Image import Image
from math import floor
from random import sample
from typing import Iterable


class BitFlipper:
    """Inverts bits of RGB values of random pixels."""

    def modify(self, image: Image):
        """Invert up to a hundred pixels."""

        dims = image.size
        # An image might have <100 pixels.
        pixel_count = min(100, dims[0] * dims[1])
        to_flip = set(sample(range(dims[0] * dims[1]), k=pixel_count))
        self._flip(image, to_flip)
        return sorted(to_flip)

    def unmodify(self, image: Image, flipped_indices: Iterable[int]):
        """Un-invert the inverted pixels."""

        self._flip(image, flipped_indices)

    def _flip(self, image: Image, indices: Iterable[int]):
        """Do the inversion"""
        dims = image.size
        for i in indices:
            xy = (floor(i / dims[1]), i % dims[1])
            pixel = image.getpixel(xy)
            if not pixel:
                raise IndexError(f"Pixel value empty at {xy}")
            if isinstance(pixel, float) or isinstance(pixel, int):
                raise IndexError(f"Pixel value invalid at {xy}")
            pixel = (
                # Use 0xFF to discard the upper bytes of the integer.
                *[~band_val & 0xFF for band_val in pixel[:3]],
                # Append the alpha value if present.
                *(pixel[3:]),
            )
            image.putpixel(xy, pixel)
