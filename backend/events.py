import time
from collections import defaultdict

event_memory = defaultdict(list)

WINDOW = 3600
SPIKE_THRESHOLD = 2


def register_event(topic):
    if not topic:
        return

    topic = str(topic).lower().strip()
    now = time.time()
    event_memory[topic].append(now)


def detect_event_spikes():
    now = time.time()
    spikes = []

    for topic, times in list(event_memory.items()):

        recent = [t for t in times if now - t < WINDOW]
        event_memory[topic] = recent

        count = len(recent)

        if count >= SPIKE_THRESHOLD:

            first = min(recent)
            last = max(recent)
            duration = max(last - first, 1)

            velocity = count / duration

            spikes.append({
                "topic": topic,
                "count": count,
                "velocity": round(velocity, 4)
            })

    spikes.sort(key=lambda x: (x["count"], x["velocity"]), reverse=True)

    return spikes
