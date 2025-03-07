from typing import Sequence
from sqlmodel import SQLModel


class ImagePublic(SQLModel):
    id: int
    filename: str | None = None
    valid_image: bool | None = None
    reversible: bool | None = None


class ImagesPublic(SQLModel):
    images: Sequence[ImagePublic]
