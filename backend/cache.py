import time

# 🔥 MEMORY CACHE (REDIS YOK)
_cache = {}

COOLDOWN = 300  # 5 dakika


def is_duplicate(topic):

    if not topic:
        return False

    last_time = _cache.get(topic)

    if last_time:
        if time.time() - last_time < COOLDOWN:
            return True

    return False


def mark_generated(topic):

    if not topic:
        return

    _cache[topic] = time.time()
