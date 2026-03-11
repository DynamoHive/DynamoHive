from datetime import datetime

FEED = []


def publish(items):

    global FEED

    for item in items:

        FEED.append({
            "title": item["title"],
            "content": item["content"],
            "timestamp": datetime.utcnow().isoformat()
        })

    if len(FEED) > 200:
        FEED = FEED[-200:]


def get_feed():

    return list(reversed(FEED[-50:]))
