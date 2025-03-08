from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session, create_engine

from verifier.db import find_unverified
from verifier.reverser import reversible


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    SQLALCHEMY_DATABASE_URI: str
    IMAGE_UPLOADED_PATH: str
    IMAGE_MODIFIED_PATH: str


settings = Settings()  # type: ignore

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def verify(session: Session | None = None):
    if session is None:
        with Session(engine) as session:
            _verify_with_session(session)
    else:
        _verify_with_session(session)


def _verify_with_session(session: Session):
    for image_entry in find_unverified(session):
        image_entry.reversible = reversible(image_entry)
        session.add(image_entry)
    session.commit()
