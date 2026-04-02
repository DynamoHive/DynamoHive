from fastapi import APIRouter
from backend.data_pipeline import event_queue
from backend.knowledge_graph import add_knowledge

router = APIRouter()


@router.post("/events")
def collect_event(event: dict):

    topic = event.get("topic")
    post_id = event.get("post_id")

    if topic and post_id:
        add_knowledge(topic, post_id)

    event_queue.put(event)

    return {"status": "ok"}
