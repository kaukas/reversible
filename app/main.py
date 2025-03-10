from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from os.path import join
from pathlib import Path
from shutil import copyfileobj
from sqlmodel import select
from typing import Sequence, cast
from uuid import uuid4

from app.core.db import create_db_and_tables
from db_models import Image

from app.core.validate_image import validate_and_modify_image
from app.core.config import settings
from app.deps import SessionDep
from app.models import ImagePublic, ImagesPublic


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    Path(settings.IMAGE_UPLOADED_PATH).mkdir(parents=True, exist_ok=True)
    Path(settings.IMAGE_MODIFIED_PATH).mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    # The demo server listens on 8001.
    allow_origins=["http://localhost:8000", "http://localhost:8001"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/images", response_model=ImagesPublic)
def list_images(session: SessionDep):
    return ImagesPublic(
        images=cast(Sequence[ImagePublic], session.exec(select(Image)).all())
    )


@app.post("/images", response_model=ImagePublic)
def create_image(
    session: SessionDep, image: UploadFile, background_tasks: BackgroundTasks
):
    if image.size == 0:
        raise HTTPException(422, "Image must not be empty")

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
    return ImagePublic(id=cast(int, image_entry.id), filename=image_entry.filename)
