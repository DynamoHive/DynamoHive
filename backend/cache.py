import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def set_cache(key, value):
    redis_client.set(key, value)

def get_cache(key):
    return redis_client.get(key)
