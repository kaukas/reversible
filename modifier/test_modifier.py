from PIL import Image

from modifier import BitFlipper


def test_flips_bits_of_pixels_in_an_image():
    image = Image.new("RGBA", (1, 3))
    image.putdata([(0, 0, 0, 0), (0b11, 0b1111, 0b111111, 0), (0xFF, 0xFF, 0xFF, 0)])
    BitFlipper().modify(image, 3)
    assert list(image.getdata()) == [
        (0xFF, 0xFF, 0xFF, 0),
        (0b11111100, 0b11110000, 0b11000000, 0),
        (0, 0, 0, 0),
    ]


def test_flips_bits_of_random_pixels():
    image = Image.new("RGBA", (3, 3))
    px_before = list(image.getdata())
    # Flip any two pixels.
    BitFlipper().modify(image, 2)
    px_after = list(image.getdata())
    changed = [i for i, (pb, pa) in enumerate(zip(px_before, px_after)) if pb != pa]
    assert len(changed) == 2
