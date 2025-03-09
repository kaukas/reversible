from PIL import Image as PILImage
from json import dumps
from os.path import join
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest import fixture, mark
from uuid import uuid4

from db_models import Image
from modifier import modify

from verifier.main import settings
from verifier.reverser import reversible


@fixture
def standard_dirs(fs: FakeFilesystem):
    fs.makedirs(settings.IMAGE_UPLOADED_PATH)
    fs.makedirs(settings.IMAGE_MODIFIED_PATH)


@mark.usefixtures("standard_dirs")
def test_reverses_image_modifications_and_verifies_all_pixels_match():
    modified_filepath = join(settings.IMAGE_MODIFIED_PATH, str(uuid4()))
    image_entry = Image(
        original_filepath=join(settings.IMAGE_UPLOADED_PATH, str(uuid4())),
        modified_filepath=modified_filepath,
    )

    pil_image = PILImage.new("RGBA", (10, 10))
    pil_image.save(image_entry.original_filepath, "png")

    changes = modify(pil_image)
    image_entry.modification_params = dumps(changes)

    pil_image.save(modified_filepath, "png")

    assert reversible(image_entry)

    # A manual change to the modified image. After un-modification it will remain
    # different from the original.
    pil_image.putpixel((0, 0), (1, 1, 1, 50))
    pil_image.save(modified_filepath, "png")

    assert not reversible(image_entry)
