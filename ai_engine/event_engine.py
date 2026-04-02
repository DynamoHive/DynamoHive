import time
from collections import defaultdict

event_memory = defaultdict(list)

WINDOW = 3600          # 1 saat
SPIKE_THRESHOLD = 5    # minimum tekrar


def register_event(topic):

    if not topic:
        return

    now = time.time()

    # normalize (çok önemli)
    topic = str(topic).lower().strip()

    event_memory[topic].append(now)


def detect_event_spikes():

    now = time.time()
    spikes = []

    # 🔴 boş liste hatasını önlemek için kopya üzerinden dön
    for topic, times in list(event_memory.items()):

        # 🔴 sadece window içindekileri tut
        recent = [t for t in times if now - t < WINDOW]
        event_memory[topic] = recent

        count = len(recent)

        if count >= SPIKE_THRESHOLD:

            # 🔥 strength (yoğunluk + hız)
            first = min(recent)
            last = max(recent)
            duration = max(last - first, 1)

            velocity = count / duration  # ne kadar hızlı büyüyor

            spikes.append({
                "topic": topic,
                "count": count,
                "velocity": round(velocity, 4)
            })

    # 🔥 en güçlü eventleri öne al
    spikes.sort(key=lambda x: (x["count"], x["velocity"]), reverse=True)

    print("events detected:", len(spikes))

    return spikes
