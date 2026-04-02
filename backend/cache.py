import redis
import time

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

COOLDOWN = 300  # 5 dakika


def is_duplicate(topic):

    if not topic:
        return False

    key = f"topic:{topic}"

    last_time = redis_client.get(key)

    if last_time:
        last_time = float(last_time)

        if time.time() - last_time < COOLDOWN:
            return True

    return False


def mark_generated(topic):

    if not topic:
        return

    key = f"topic:{topic}"

    redis_client.set(key, time.time())
