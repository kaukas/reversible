from typing import Sequence
from sqlmodel import Session, select

from db_models import Image


def find_unverified(session: Session):
    for image in session.exec(select(Image).where(Image.reversible == None)):
        yield image

def save_images(session: Session, images: Sequence[Image]):
    session.add_all(images)
    session.commit()
