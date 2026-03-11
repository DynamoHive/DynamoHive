import time
from collections import defaultdict

event_memory = defaultdict(list)

WINDOW = 3600
SPIKE_THRESHOLD = 5


def register_event(topic):

    now = time.time()

    event_memory[topic].append(now)


def detect_event_spikes():

    now = time.time()

    spikes = []

    for topic, times in event_memory.items():

        recent = [t for t in times if now - t < WINDOW]

        event_memory[topic] = recent

        if len(recent) >= SPIKE_THRESHOLD:

            spikes.append({
                "topic": topic,
                "count": len(recent)
            })

    return spikes
