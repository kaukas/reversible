from ...modifier import BitFlipper

from app.deps import SessionDep
from app.models import Image

def validate_and_modify_image(session: SessionDep, image_entry: Image):
    image_entry.modified_filepath = join(settings.IMAGE_MODIFIED_PATH, str(uuid4()))
    image_entry.valid_image = True
    session.add(image_entry)
    session.commit()
