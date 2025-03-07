from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import SQLModel, Session, create_engine, select


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    SQLALCHEMY_DATABASE_URI: str


settings = Settings()  # type: ignore

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
