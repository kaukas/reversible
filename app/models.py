from sqlmodel import SQLModel
from typing import Sequence

### Models that are returned by the API.


class ImagePublic(SQLModel):
    id: int
    filename: str | None = None
    valid_image: bool | None = None
    reversible: bool | None = None


class ImagesPublic(SQLModel):
    images: Sequence[ImagePublic]
