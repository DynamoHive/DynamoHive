import time
import threading

# -----------------------------
# INTERNAL STATE
# -----------------------------
_last_data = None
_last_timestamp = 0

_duplicate_cache = set()
_cache_lock = threading.Lock()

# TTL (seconds)
DUPLICATE_TTL = 300  # 5 min


# -----------------------------
# LAST DATA HANDLING
# -----------------------------
def set_last_data(data):
    global _last_data, _last_timestamp

    with _cache_lock:
        _last_data = data
        _last_timestamp = time.time()


def get_last_data():
    with _cache_lock:
        return _last_data


# -----------------------------
# DUPLICATE CONTROL
# -----------------------------
def is_duplicate(signal_id: str) -> bool:
    """
    Returns True if signal already processed recently
    """
    with _cache_lock:
        if signal_id in _duplicate_cache:
            return True

        _duplicate_cache.add(signal_id)
        return False


# -----------------------------
# CLEANUP (TTL)
# -----------------------------
def cleanup_cache():
    """
    Simple TTL-based cleanup for duplicate cache
    """
    global _duplicate_cache

    with _cache_lock:
        _duplicate_cache.clear()


def auto_cleanup_worker(interval: int = 60):
    """
    Optional background cleaner (can be used by scheduler)
    """
    while True:
        time.sleep(interval)
        cleanup_cache()
