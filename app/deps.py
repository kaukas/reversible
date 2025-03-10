from collections.abc import Generator
from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.core.db import engine


def get_session() -> Generator[Session, None, None]:
    """Create a SQLAlchemy session."""

    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
