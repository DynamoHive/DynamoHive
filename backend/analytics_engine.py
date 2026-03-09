from collections import defaultdict

metrics = {
    "users": set(),
    "posts": defaultdict(int),
    "events": defaultdict(int)
}

def record_event(event):

    user_id = event.get("user_id")
    event_type = event.get("type")
    post_id = event.get("post_id")

    if user_id:
        metrics["users"].add(user_id)

    if event_type:
        metrics["events"][event_type] += 1

    if post_id:
        metrics["posts"][post_id] += 1


def get_metrics():

    return {
        "total_users": len(metrics["users"]),
        "events": dict(metrics["events"]),
        "posts": dict(metrics["posts"])
    }
