import uuid

from pydantic import (
    BaseModel,
    validator,
    root_validator
)

from app.users.exceptions import InvalidUserIDException
from .exceptions import (
    InvalidYoutubeVideoURLException,
    VideoAlreadyAddedException
)
from .extractors import extract_video_id
from .models import Video


class VideoCreateSchema(BaseModel):
    url: str  # User generated
    title: str
    user_id: uuid.UUID  # request.session_id

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid Youtube URL")

        return url

    @root_validator
    def validate_data(cls, values):
        url = values.get("url")
        title = values.get("title")

        if url is None:
            raise ValueError("A valid url is required")

        user_id = values.get("user_id")
        video_obj = None
        extra_data = {}
        if title is not None:
            extra_data["title"] = title

        extra_data = {
            "title": title
        }
        try:
            video_obj = Video.add_video(url, user_id=user_id, **extra_data)
        except InvalidYoutubeVideoURLException:
            raise ValueError(f"{url} is not a valid Youtube URL.")
        except VideoAlreadyAddedException:
            raise ValueError(f"{url} has already been added to your account.")
        except InvalidUserIDException:
            raise ValueError("There's a problem with your account, please try again.")

        if video_obj is None:
            raise ValueError("There's a problem with your account, please try again.")
        if not isinstance(video_obj, Video):
            raise ValueError("There's a problem with your account, please try again.")
        # if title is not None:
        #     video_obj.title = title
        #     video_obj.save()

        return video_obj.as_data()