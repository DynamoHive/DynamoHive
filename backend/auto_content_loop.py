import time
import random


def generate_content(event):

    if not event:
        return None

    topic = event.get("topic", "unknown")

    article = {
        "title": f"Signal Detected: {topic}",
        "content": f"""
DynamoHive detected a spike in '{topic}'.

Signal intensity: {event.get("count", 0)}
Velocity: {event.get("velocity", 0)}

This indicates a potential emerging event in the global information space.
""",
        "author": "DynamoHive AI",
        "timestamp": time.time()
    }

    print("Generated content:", article)

    return article
