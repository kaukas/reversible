from PIL import Image as PILImage
from json import dumps
from os.path import join
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest import fixture, mark
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select
from typing import cast
from uuid import uuid4

from db_models import Image
from main import settings, verify
from modifier import modify


@fixture
def standard_dirs(fs: FakeFilesystem):
    fs.makedirs(settings.IMAGE_UPLOADED_PATH)
    fs.makedirs(settings.IMAGE_MODIFIED_PATH)


@fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def create_image(**kwargs):
    image_entry = Image(
        original_filepath=join(settings.IMAGE_UPLOADED_PATH, str(uuid4())),
        modified_filepath=join(settings.IMAGE_MODIFIED_PATH, str(uuid4())),
        valid_image=True,
        **kwargs,
    )

    pil_image = PILImage.new("RGBA", (10, 10))
    pil_image.save(image_entry.original_filepath, "png")
    return image_entry


@mark.usefixtures("standard_dirs")
def test_sets_reversibility_of_previously_unchecked_image_records(session: Session):
    image_entry = create_image()
    pil_image = PILImage.open(image_entry.original_filepath)
    image_entry.modification_params = dumps(modify(pil_image))
    pil_image.save(cast(str, image_entry.modified_filepath), "png")

    src_images = [
        # These two will be ignored.
        create_image(reversible=False),
        create_image(reversible=True),
        # This one will be verified.
        image_entry,
    ]
    session.add_all(src_images)

    verify(session)

    assert session.exec(
        select(Image.reversible).order_by(cast(str, Image.id))
    ).all() == [False, True, True]
