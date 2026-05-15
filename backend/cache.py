import time
import threading

# =====================================================
# INTERNAL STATE
# =====================================================
_last_data = None
_duplicate_cache = {}

_lock = threading.Lock()

# 5 dakika TTL
DUPLICATE_TTL = 300


# =====================================================
# LAST DATA
# =====================================================
def set_last_data(data):
    global _last_data

    with _lock:
        _last_data = data


def get_last_data():
    with _lock:
        return _last_data


# =====================================================
# DUPLICATE CONTROL
# =====================================================
def is_duplicate(key: str) -> bool:
    """
    Returns True if key was already processed recently
    """

    now = time.time()

    with _lock:
        # TTL cleanup
        expired = [
            k for k, t in _duplicate_cache.items()
            if now - t > DUPLICATE_TTL
        ]

        for k in expired:
            del _duplicate_cache[k]

        # check duplicate
        if key in _duplicate_cache:
            return True

        _duplicate_cache[key] = now
        return False


# =====================================================
# CLEANUP
# =====================================================
def cleanup_cache():
    """
    Hard cleanup (manual or scheduler call)
    """
    with _lock:
        _duplicate_cache.clear()
