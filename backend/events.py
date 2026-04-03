import time
from collections import defaultdict

# 🔥 USER LEARNING (KOD-8)
from backend.user_profile_engine import process_event


# -------------------------
# 🔥 EVENT MEMORY (SPIKE ENGINE)
# -------------------------

event_memory = defaultdict(list)

WINDOW = 3600            # 1 saat
SPIKE_THRESHOLD = 2      # minimum event sayısı
CLEANUP_LIMIT = 5000     # memory overflow koruması


# -------------------------
# REGISTER EVENT
# -------------------------

def register_event(topic):

    if not topic:
        return

    try:
        topic = str(topic).lower().strip()
    except:
        return

    now = time.time()

    event_memory[topic].append(now)

    # 🔥 memory overflow koruması
    if len(event_memory[topic]) > CLEANUP_LIMIT:
        event_memory[topic] = event_memory[topic][-CLEANUP_LIMIT:]


# -------------------------
# DETECT SPIKES
# -------------------------

def detect_event_spikes():

    now = time.time()
    spikes = []

    for topic, times in list(event_memory.items()):

        # son WINDOW içindeki eventler
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

    # 🔥 en güçlü spike üstte
    spikes.sort(
        key=lambda x: (x["count"], x["velocity"]),
        reverse=True
    )

    return spikes


# -------------------------
# 🔥 USER EVENT HANDLER (KOD-8 CORE)
# -------------------------

def handle_event(user_id, event):
    """
    event = {
        "type": "click" | "like" | "skip",
        "topic": "ai"
    }
    """

    if not event or not user_id:
        return {"status": "error", "reason": "invalid_input"}

    topic = event.get("topic")

    if not topic:
        return {"status": "error", "reason": "missing_topic"}

    try:
        topic = str(topic).lower().strip()
    except:
        return {"status": "error", "reason": "invalid_topic"}

    # -------------------------
    # 1️⃣ GLOBAL SPIKE ENGINE
    # -------------------------
    register_event(topic)

    # -------------------------
    # 2️⃣ USER LEARNING ENGINE
    # -------------------------
    try:
        profile = process_event(user_id, {
            "type": event.get("type"),
            "topic": topic
        })
    except Exception as e:
        return {"status": "error", "reason": str(e)}

    # -------------------------
    # 3️⃣ RESPONSE
    # -------------------------
    return {
        "status": "ok",
        "topic": topic,
        "user_profile": profile,
        "event_type": event.get("type"),
        "timestamp": int(time.time())
    }
