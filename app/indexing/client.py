from algoliasearch.search_client import SearchClient

from app.config import get_settings
from app.playlists.models import Playlist
from app.videos.models import Video
from .schemas import VideoIndexSchema, PlaylistIndexSchema

settings = get_settings()


def get_index(name=settings.algolia_index_name):
    client = SearchClient.create(settings.algolia_app_id, settings.algolia_api_key)
    index = client.init_index(name)
    return index


def get_dataset():
    playlist_q = [dict(obj) for obj in Video.objects.all()]
    playlists_dataset = [PlaylistIndexSchema(**obj).dict() for obj in playlist_q]

    video_q = [dict(x) for x in Video.objects.all()]
    videos_dataset = [VideoIndexSchema(**obj).dict() for obj in video_q]

    return playlists_dataset + videos_dataset


def update_index():
    index = get_index()
    dataset = get_dataset()
    idx_response = index.save_objects(dataset).wait()
    try:
        count = len(list(idx_response[0]["objectIDs"]))
    except:
        count = 0

    return count


def search_index():
    pass
    index = get_index()
    return index.search(query)
