from pytest import fixture
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine, select, asc

from db_models import Image

from verifier.db import find_unverified


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
        Image(
            original_filepath="a",
            modified_filepath="m",
            valid_image=True,
            reversible=None,
        ),
        Image(
            original_filepath="b",
            modified_filepath="n",
            valid_image=True,
            reversible=False,  # ignored
        ),
        Image(
            original_filepath="c",
            modified_filepath="o",
            valid_image=True,
            reversible=True,  # ignored
        ),
    ]
    session.add_all(src_images)

    found_images = find_unverified(session)
    assert [i.id for i in found_images] == [src_images[0].id]


def test_skips_images_that_have_not_been_modified_yet(session: Session):
    src_images = [
        Image(original_filepath="a", reversible=None, valid_image=True),  # not modified
        Image(
            original_filepath="b",
            reversible=None,
            valid_image=True,
            modified_filepath="m",
        ),
    ]
    session.add_all(src_images)

    assert [i.id for i in find_unverified(session)] == [src_images[1].id]


def test_skips_invalid_images(session: Session):
    src_images = [
        Image(
            original_filepath="a",
            reversible=None,
            modified_filepath="m",
            valid_image=False,  # invalid
        ),
        Image(
            original_filepath="b",
            reversible=None,
            modified_filepath="m",
            valid_image=True,
        ),
    ]
    session.add_all(src_images)

    assert [i.id for i in find_unverified(session)] == [src_images[1].id]
