from sqlmodel import SQLModel, Session, create_engine, select

from app.core.config import settings
import app.models

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
