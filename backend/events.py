from fastapi import APIRouter
from backend.data_pipeline import event_queue

router = APIRouter()

@router.post("/events")
def collect_event(event: dict):

    event_queue.put(event)

    return {"status": "event received"}
