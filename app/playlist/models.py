from datetime import datetime
from uuid import uuid1

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app.config import get_settings

from datetime import timezone

settings = get_settings()


class Playlist(Model):
    __keyspace__ = settings.keyspace
    db_id = columns.UUID(primary_key=True, default=uuid1)
    user_id = columns.UUID()
    updated = columns.DateTime(default=datetime.now(timezone.utc))
    host_ids = columns.List(value_type=columns.Text)
    title = columns.Text()
   