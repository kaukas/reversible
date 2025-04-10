from PIL import Image as PILImage
from fastapi.testclient import TestClient
from io import BytesIO
from os.path import dirname
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest import fixture, mark
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select

from db_models import Image

from .main import app
from app.core.config import settings
from app.deps import get_session


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


@fixture(name="client")
def client_fixture(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_lists_images(session: Session, client: TestClient):
    session.add_all(
        [
            Image(filename="cat.png", original_filepath="/tmp/cat.png"),
            Image(
                filename="dog.png",
                original_filepath="",
                valid_image=True,
                reversible=False,
            ),
        ]
    )
    session.commit()

    response = client.get("/images")
    assert response.status_code == 200
    assert response.json() == {
        "images": [
            {"id": 1, "filename": "cat.png", "valid_image": None, "reversible": None},
            {"id": 2, "filename": "dog.png", "valid_image": True, "reversible": False},
        ]
    }


@mark.usefixtures("standard_dirs")
def test_uploads_an_image(session: Session, client: TestClient, fs: FakeFilesystem):
    assert client.get("/images").json() == {"images": []}

    pil_image = PILImage.new("RGBA", (10, 10))
    buffer = BytesIO()
    pil_image.save(buffer, "png")

    response = client.post("/images", files={"image": ("cat.png", buffer)})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "filename": "cat.png",
        "valid_image": None,
        "reversible": None,
    }

    all_images = session.exec(select(Image)).all()
    assert len(all_images) == 1
    image_entry = all_images[0]
    assert image_entry.filename == "cat.png"
    assert image_entry.valid_image == True
    assert dirname(image_entry.original_filepath) == settings.IMAGE_UPLOADED_PATH
    assert fs.exists(image_entry.original_filepath)


def test_requires_an_image(client: TestClient):
    # No image.
    assert client.post("/images").status_code == 422

    # Empty image.
    response = client.post("/images", files={"image": ("cat.png", BytesIO())})
    assert response.status_code == 422


@mark.usefixtures("standard_dirs")
def test_supports_RGB_images(session: Session, client: TestClient):
    pil_image = PILImage.new("RGB", (10, 10))
    buffer = BytesIO()
    pil_image.save(buffer, "png")

    response = client.post("/images", files={"image": ("cat.png", buffer)})
    assert response.status_code == 200
    assert session.exec(select(Image.valid_image)).all() == [True]


@mark.usefixtures("standard_dirs")
def test_does_not_support_non_RGB_or_RGBA_images(session: Session, client: TestClient):
    def file_of_mode(mode: str):
        pil_image = PILImage.new(mode, (10, 10))
        buffer = BytesIO()
        pil_image.save(buffer, "png")
        return {"image": ("cat.png", buffer)}

    for mode in ["1", "L", "P"]:
        client.post("/images", files=file_of_mode(mode))
    assert set(session.exec(select(Image.valid_image)).all()) == set([False])


@mark.usefixtures("standard_dirs")
def test_does_not_support_non_png_images(session: Session, client: TestClient):
    def file_of_ext(ext: str):
        pil_image = PILImage.new("RGB", (10, 10))
        buffer = BytesIO()
        pil_image.save(buffer, ext)
        return {"image": (f"cat.{ext}", buffer)}

    for ext in ["jpeg", "bmp"]:
        client.post("/images", files=file_of_ext(ext))
    assert set(session.exec(select(Image.valid_image)).all()) == set([False])


@mark.usefixtures("standard_dirs")
def test_modifies_the_uploaded_image(
    session: Session, client: TestClient, fs: FakeFilesystem
):
    pil_image = PILImage.new("RGBA", (10, 10))
    buffer = BytesIO()
    pil_image.save(buffer, "png")

    response = client.post("/images", files={"image": ("cat.png", buffer)})
    assert response.status_code == 200
    image_entry = session.exec(select(Image)).one()

    mod_filepath = image_entry.modified_filepath
    assert isinstance(mod_filepath, str)
    assert dirname(mod_filepath) == settings.IMAGE_MODIFIED_PATH
    assert fs.exists(image_entry.modified_filepath)
    assert image_entry.modification_params

    assert image_entry.valid_image == True


@mark.usefixtures("standard_dirs")
def test_marks_invalid_image(session: Session, client: TestClient):
    buffer = BytesIO(b"not an image at all")

    response = client.post("/images", files={"image": ("cat.png", buffer)})
    assert response.status_code == 200
    assert session.exec(select(Image.valid_image)).one() == False
