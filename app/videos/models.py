from uuid import uuid1
from app.config import get_settings
from app.users.models import User

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from extractors import extract_video_id

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
        host_id = extract_video_id(url)
        if host_id is None:
            raise Exception("Invalid youtube video url")

        user_id = User.check_exists(user_id)
        if user_id is None:
            raise Exception("Invalid user id")

        # user_obj = User.by_user_id(user_id)
        # user_obj.display_name

        q = Video.objects.filter(host_id=host_id, user_id=user_id)
        if q.count() != 0:
            raise Exception("Video already added")

        return Video.create(host_id=host_id, user_id=user_id, url=url)
