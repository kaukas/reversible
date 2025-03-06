from sqlmodel import Session, create_engine, select

from app.core.config import settings
import app.models

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def init_db(session: Session) -> None:
    pass
