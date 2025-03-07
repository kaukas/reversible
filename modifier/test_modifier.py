from PIL import Image

from modifier import BitFlipper


def test_flips_bits_of_pixels_in_an_image():
    # Pixel RGBA values, before and after. Bits flipped in color bands only.
    pixels = (
        ((0, 0, 0, 0), (0xFF, 0xFF, 0xFF, 0)),
        ((0b11, 0b1111, 0b111111, 0), (0b11111100, 0b11110000, 0b11000000, 0)),
        ((0xFF, 0xFF, 0xFF, 0), (0, 0, 0, 0)),
    )
    image = Image.new("RGBA", (1, 3))
    image.putdata([p[0] for p in pixels])
    BitFlipper().modify(image, 3)
    assert list(image.getdata()) == [p[1] for p in pixels]


def test_flips_bits_of_random_pixels_and_reports_their_indices():
    image = Image.new("RGBA", (3, 3))
    px_before = list(image.getdata())
    # Flip any two pixels.
    indices = BitFlipper().modify(image, 2)
    assert len(indices) == 2

    px_after = list(image.getdata())
    changed = [i for i, (pb, pa) in enumerate(zip(px_before, px_after)) if pb != pa]
    assert len(changed) == 2


def test_flips_the_modified_pixels_back():
    original_image = Image.new("RGBA", (1, 3))
    image = original_image.copy()
    flipper = BitFlipper()
    indices = flipper.modify(image, 3)
    flipper.unmodify(image, indices)
    assert list(image.getdata()) == list(original_image.getdata())
