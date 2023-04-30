from fastapi import APIRouter, Request

from main import app
from .models import WatchEvent
from .schemas import WatchEventSchema

router = APIRouter()


@app.post("/api/events/watch", response_model=WatchEventSchema)
def watch_event_view(request: Request, watch_event: WatchEventSchema):
    cleaned_data = watch_event.dict()
    data = cleaned_data.copy()
    data.update({"user_id": request.user.username})
    print(f"Data: {data}")
    if request.user.is_authenticated:
        WatchEvent.objects.create(**data)

    return watch_event
