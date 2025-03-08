from pytest import fixture
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select

from db_models import Image

from verifier.db import find_unverified, save_images


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


def test_yields_unverified_image_entries_from_db(session: Session):
    src_images = [
        Image(original_filepath="a", modified_filepath="m", reversible=None),
        Image(original_filepath="b", modified_filepath="n", reversible=False),
        Image(original_filepath="c", modified_filepath="o", reversible=True),
    ]
    session.add_all(src_images)

    found_images = find_unverified(session)
    assert [i.id for i in found_images] == [src_images[0].id]


def test_skips_images_that_have_not_been_modified_yet(session: Session):
    src_images = [
        Image(original_filepath="a", reversible=None),
        Image(original_filepath="b", reversible=None, modified_filepath="m"),
    ]
    session.add_all(src_images)

    assert [i.id for i in find_unverified(session)] == [src_images[1].id]


def test_persists_modified_image_entries(session: Session):
    src_images = [
        Image(original_filepath="a"),
        Image(original_filepath="b"),
        Image(original_filepath="c"),
    ]
    session.add_all(src_images)
    session.commit()
    # Forget the images in the session.
    session.expunge_all()

    src_images[0].reversible = True
    src_images[1].reversible = True
    src_images[2].reversible = False
    save_images(session, src_images)

    assert session.exec(select(Image.reversible).order_by(Image.id)).all() == [
        True,
        True,
        False,
    ]
