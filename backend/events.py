# backend/events.py

import time
from collections import defaultdict

# 🔥 KOD-8 bağlantısı
from backend.user_profile_engine import process_event


# -------------------------
# EVENT MEMORY (SPIKE ENGINE)
# -------------------------

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

        # sadece son WINDOW içindeki eventleri tut
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


# -------------------------
# 🔥 USER EVENT HANDLER (KOD-8)
# -------------------------

def handle_event(user_id, event):
    """
    event = {
        "type": "click" | "like" | "skip",
        "topic": "ai"
    }
    """

    if not event:
        return

    topic = event.get("topic")

    # 1️⃣ spike sistemi beslenir
    register_event(topic)

    # 2️⃣ user learning sistemi beslenir
    profile = process_event(user_id, event)

    return {
        "status": "ok",
        "user_profile": profile
    }
