from json import loads
from PIL import Image as PILImage
from db_models import Image
from modifier import unmodify

class ModifiedFileMissing(Exception):
    """Modified Filepath empty. The image was likely not modified."""


def reversible(image: Image):
    if not image.modified_filepath or not image.modification_params:
        # TODO: test
        raise ModifiedFileMissing()

    original_pil_image = PILImage.open(image.original_filepath)
    modified_pil_image = PILImage.open(image.modified_filepath)
    unmodify(modified_pil_image, loads(image.modification_params))
    return list(original_pil_image.getdata()) == list(modified_pil_image.getdata())
