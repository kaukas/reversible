from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Filename of the user uploaded file.
    filename: str | None = None
    original_filepath: str
    modified_filepath: str | None = None
    modification_params: str | None = None
    # If the image was recognized by PIL.
    valid_image: bool | None = None
    # If the modification is reversible.
    reversible: bool | None = None
