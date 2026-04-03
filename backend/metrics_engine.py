# backend/metrics_engine.py

from backend.events import detect_event_spikes
from backend.storage import get_posts

def get_system_metrics():

    posts = get_posts()
    spikes = detect_event_spikes()

    metrics = {
        "total_posts": len(posts),
        "latest_post": posts[0]["title"] if posts else None,
        "event_spikes": spikes[:5],
        "status": "running"
    }

    return metrics
