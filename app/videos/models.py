from uuid import uuid1

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app.config import get_settings
from app.users.exceptions import InvalidUserIDException
from app.users.models import User
from .exceptions import (
    InvalidYoutubeVideoURLException, VideoAlreadyAddedException
)
from .extractors import extract_video_id

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid1)
    host_service = columns.Text(default="youtube")
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(host_id={self.host_id}, host_service={self.host_service})"

    def as_data(self):
        return {f"{self.host_service}_id": self.host_id}

    @staticmethod
    def add_video(url, user_id=None):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYoutubeVideoURLException("Invalid youtube video url")

        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid user id")

        # user_obj = User.by_user_id(user_id)
        # user_obj.display_name

        q = Video.objects.allow_filtering().filter(host_id=host_id, user_id=user_id)
        if q.count() != 0:
            raise VideoAlreadyAddedException("Video already added")

        return Video.create(host_id=host_id, user_id=user_id, url=url)
