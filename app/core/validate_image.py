from json import dumps
from os.path import join
from uuid import uuid4
from PIL import Image as PILImage, UnidentifiedImageError

from db_models import Image
from modifier import modify

from app.core.config import settings
from app.deps import SessionDep


def validate_and_modify_image(session: SessionDep, image_entry: Image):
    try:
        pil_image = PILImage.open(image_entry.original_filepath)
    except UnidentifiedImageError as e:
        image_entry.valid_image = False
    else:
        image_entry.valid_image = True
        changes = modify(pil_image)
        if changes:
            image_entry.modification_params = dumps(changes)

        modified_filepath = join(settings.IMAGE_MODIFIED_PATH, str(uuid4()))
        pil_image.save(modified_filepath, pil_image.format)

        image_entry.modified_filepath = modified_filepath

    session.add(image_entry)
    session.commit()
