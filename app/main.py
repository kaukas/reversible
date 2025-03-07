from os.path import join
from shutil import copyfileobj
from uuid import uuid4
from fastapi import BackgroundTasks, FastAPI, UploadFile
from sqlmodel import select

from db_models import Image

from app.core.validate_image import validate_and_modify_image
from app.core.config import settings
from app.deps import SessionDep
from app.models import ImagePublic, ImagesPublic


app = FastAPI()


@app.get("/images", response_model=ImagesPublic)
def list_images(session: SessionDep):
    return ImagesPublic(images=session.exec(select(Image)).all())


@app.post("/images", response_model=ImagePublic)
def create_image(
    session: SessionDep, image: UploadFile, background_tasks: BackgroundTasks
):
    original_filepath = join(settings.IMAGE_UPLOADED_PATH, str(uuid4()))
    with open(original_filepath, "xb") as dest_file:
        copyfileobj(image.file, dest_file)

    image_entry = Image(
        filename=image.filename,
        original_filepath=original_filepath,
    )
    session.add(image_entry)
    session.commit()
    background_tasks.add_task(validate_and_modify_image, session, image_entry)
    return ImagePublic(id=image_entry.id, filename=image_entry.filename)
