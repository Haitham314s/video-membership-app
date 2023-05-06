import uuid
from typing import Optional

from pydantic import BaseModel, Field, validator, root_validator


class VideoIndexSchema(BaseModel):
    objectID: str = Field(alias="host_id")
    objectType: str = "Video"
    title: Optional[str]
    path: str = Field(alias="host_id")

    @validator("path")
    def set_path(cls, v, values, **kwargs):
        return f"/videos/{v}"


class PlaylistIndexSchema(BaseModel):
    objectID: uuid.UUID = Field(alias="db_id")
    objectType: str = "Playlist"
    title: Optional[str]
    path: uuid.UUID = Field(default="/")

    @root_validator
    def set_defaults(cls, values):
        objectID = values.get("objectID")
        values["objectID"] = str(objectID)
        values["path"] = f"/playlists/{objectID}"
        return values
