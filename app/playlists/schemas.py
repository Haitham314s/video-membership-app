import uuid

from pydantic import BaseModel


class PlaylistCreateSchema(BaseModel):
    title: str
    user_id: uuid.UUID
