from collections.abc import Generator
from typing import Annotated
from sqlmodel import Session
from fastapi import Depends

from app.core.db import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
