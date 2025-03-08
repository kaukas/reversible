from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "test", "staging", "production"] = "local"

    PROJECT_NAME: str
    SQLALCHEMY_DATABASE_URI: str

    IMAGE_UPLOADED_PATH: str
    IMAGE_MODIFIED_PATH: str


settings = Settings()  # type: ignore
