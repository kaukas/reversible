from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Filename of the user uploaded file.
    filename: str | None = Field(default=None)
    original_filepath: str
    modified_filepath: str | None = Field(default=None)
    modification_params: str | None = Field(default=None)
    # If the image was recognized by PIL.
    valid_image: bool | None = Field(default=None)
    # If the modification is reversible.
    reversible: bool | None = Field(default=None)
