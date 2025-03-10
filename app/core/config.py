from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URI: str

    IMAGE_UPLOADED_PATH: str
    IMAGE_MODIFIED_PATH: str


settings = Settings()  # type: ignore
