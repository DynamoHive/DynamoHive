from fastapi import APIRouter

from backend.data_pipeline import event_queue
from backend.knowledge_graph import add_knowledge

router = APIRouter()


@router.post("/events")
def collect_event(event: dict):

    topic = event.get("topic")
    post_id = event.get("post_id")

    # 🔥 güvenli çağrı (post_id olmasa da çalışır)
    if topic:
        try:
            add_knowledge(topic, post_id)
        except Exception:
            pass

    # 🔥 queue güvenli
    try:
        event_queue.put(event)
    except Exception:
        pass

    return {"status": "event received"}
