from fastapi import APIRouter

router = APIRouter()

events = []

@router.post("/events")
def track_event(event_type: str, user_id: int = None):
    event = {
        "type": event_type,
        "user_id": user_id
    }
    events.append(event)
    return {"status": "event recorded", "event": event}

@router.get("/events")
def list_events():
    return {"events": events}
