from uuid import uuid1
from app.config import get_settings

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid1)
    host_service = columns.Text(default="youtubes")
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(email={self.email}, user_id={self.user_id})"

    @staticmethod
    def add_video(url, user_id=None):
        pass
