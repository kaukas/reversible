from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Filename of the user uploaded file.
    filename: str | None = Field(default=None)
    # Including the folder.
    original_filepath: str
    # Including the folder.
    modified_filepath: str | None = Field(default=None)
    # A JSONified string of changes.
    modification_params: str | None = Field(default=None)
    # If the image was recognized by PIL and was of the right format and mode.
    valid_image: bool | None = Field(default=None)
    # If the modification is reversible.
    reversible: bool | None = Field(default=None)
