from PIL import Image

from modifier.bit_flipper import BitFlipper


def test_flips_bits_of_pixels_in_an_RGBA_image():
    # Pixel RGBA values, before and after. Alpha band unchanged.
    pixels = (
        ((0, 0, 0, 0), (0xFF, 0xFF, 0xFF, 0)),
        ((0b11, 0b1111, 0b111111, 0), (0b11111100, 0b11110000, 0b11000000, 0)),
        ((0xFF, 0xFF, 0xFF, 0), (0, 0, 0, 0)),
    )
    image = Image.new("RGBA", (1, 3))
    image.putdata([p[0] for p in pixels])
    BitFlipper().modify(image)
    assert list(image.getdata()) == [p[1] for p in pixels]


def test_flips_bits_of_pixels_in_an_RGB_image():
    # Pixel RGB values, before and after.
    pixels = (
        ((0, 0, 0), (0xFF, 0xFF, 0xFF)),
        ((0b11, 0b1111, 0b111111), (0b11111100, 0b11110000, 0b11000000)),
        ((0xFF, 0xFF, 0xFF), (0, 0, 0)),
    )
    image = Image.new("RGB", (1, 3))
    image.putdata([p[0] for p in pixels])
    BitFlipper().modify(image)
    assert list(image.getdata()) == [p[1] for p in pixels]


def test_flips_bits_of_random_pixels_and_reports_their_indices():
    image = Image.new("RGBA", (30, 30))
    px_before = list(image.getdata())
    # Flip any 100 pixels.
    indices = BitFlipper().modify(image)
    assert len(indices) == 100

    px_after = list(image.getdata())
    changed = [i for i, (pb, pa) in enumerate(zip(px_before, px_after)) if pb != pa]
    assert len(changed) == 100


def test_flips_the_modified_pixels_back():
    original_image = Image.new("RGBA", (1, 3))
    image = original_image.copy()
    flipper = BitFlipper()
    indices = flipper.modify(image)
    flipper.unmodify(image, indices)
    assert list(image.getdata()) == list(original_image.getdata())
