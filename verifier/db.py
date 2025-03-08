from typing import Sequence
from sqlmodel import Session, select

from db_models import Image


def find_unverified(session: Session):
    yield from session.exec(
        select(Image)
        .where(Image.modified_filepath != None)
        .where(Image.reversible == None)
    )


def save_images(session: Session, images: Sequence[Image]):
    session.add_all(images)
    session.commit()
