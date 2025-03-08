from PIL import Image

from modifier import modify, unmodify

def test_modifies_an_image():
    image = Image.new("RGBA", (1, 3))
    original_data = list(image.getdata())
    modify(image)
    modified_data = list(image.getdata())
    assert original_data != modified_data

def test_returns_modifications_data():
    assert modify(Image.new("RGBA", (1, 3))) != None

def test_unmodifies_an_image():
    image = Image.new("RGBA", (1, 3))
    original_data = list(image.getdata())
    changes = modify(image)
    unmodify(image, changes)
    modified_data = list(image.getdata())
    assert original_data == modified_data
