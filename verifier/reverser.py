from PIL import Image as PILImage
from json import loads
from typing import cast

from db_models import Image
from modifier import unmodify


def reversible(image: Image):
    """
    Reverse modifications of an image and check if the result matches the original.
    """
    original_pil_image = PILImage.open(image.original_filepath)
    modified_pil_image = PILImage.open(cast(str, image.modified_filepath))
    unmodify(
        modified_pil_image,
        loads(image.modification_params) if image.modification_params else None,
    )
    return list(original_pil_image.getdata()) == list(modified_pil_image.getdata())
