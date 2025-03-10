from sqlmodel import Session, select

from db_models import Image


def find_unverified(session: Session):
    """Yield image entries that have not been verified yet. Skip invalid entries."""

    yield from session.exec(
        select(Image)
        .where(Image.modified_filepath != None)
        .where(Image.valid_image == True)
        .where(Image.reversible == None)
    )
