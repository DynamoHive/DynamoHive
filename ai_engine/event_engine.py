import time
from collections import defaultdict

event_memory = defaultdict(list)

WINDOW = 3600
SPIKE_THRESHOLD = 2   # 🔥 5 → 2 (KRİTİK)


def register_event(topic):

    if not topic:
        return

    now = time.time()

    topic = str(topic).lower().strip()

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

    # 🔥 fallback (hiç spike yoksa 1 tane üret)
    if not spikes and event_memory:

        for topic, times in event_memory.items():
            if times:
                spikes.append({
                    "topic": topic,
                    "count": len(times),
                    "velocity": 0.0
                })
                break

    spikes.sort(key=lambda x: (x["count"], x["velocity"]), reverse=True)

    print("events detected:", len(spikes))

    return spikes
