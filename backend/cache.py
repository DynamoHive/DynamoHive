import time
import threading

# =====================================================
# INTERNAL STATE
# =====================================================
_last_data = None
_duplicate_cache = {}

_lock = threading.Lock()

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
# INTERNAL CLEANUP (OPTIMIZED)
# =====================================================
def _cleanup_expired(now: float):
    """
    Internal TTL cleanup (O(n), but isolated)
    """
    expired_keys = [
        k for k, t in _duplicate_cache.items()
        if now - t > DUPLICATE_TTL
    ]

    for k in expired_keys:
        _duplicate_cache.pop(k, None)


# =====================================================
# DUPLICATE CONTROL
# =====================================================
def is_duplicate(key: str) -> bool:
    now = time.time()

    with _lock:
        _cleanup_expired(now)

        if key in _duplicate_cache:
            return True

        _duplicate_cache[key] = now
        return False


# =====================================================
# CLEANUP
# =====================================================
def cleanup_cache():
    with _lock:
        _duplicate_cache.clear()
