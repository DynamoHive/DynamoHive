router = APIRouter()

events = []

@router.post("/events")
def create_event(event_type: str, user_id: int, post_id: int = None):

    event = {
        "type": event_type,
        "user_id": user_id,
        "post_id": post_id
    }

    events.append(event)

    # pipeline'a gönder
    add_event(event)

    return {"status": "event recorded", "event": event}


@router.get("/events")
def list_events():
    return events
