from fastapi import APIRouter, Query
from ai_engine.signal_engine import run_signal_engine
import time
import threading

router = APIRouter()


# =====================================================
# THREAD SAFE CACHE
# =====================================================
CACHE = {
    "signals": [],
    "last_update": 0,
    "loading": False
}

CACHE_TTL = 30
LOCK = threading.Lock()


# =====================================================
# REFRESH CACHE (SAFE)
# =====================================================
def refresh_cache():

    with LOCK:

        if CACHE["loading"]:
            return

        CACHE["loading"] = True

        try:
            result = run_signal_engine()

            CACHE["signals"] = result.get("signals", [])
            CACHE["last_update"] = int(time.time())

        except Exception as e:
            print("[CACHE ERROR]", e)

        finally:
            CACHE["loading"] = False


# =====================================================
# ENSURE CACHE FRESH
# =====================================================
def ensure_cache_fresh():

    if time.time() - CACHE["last_update"] > CACHE_TTL:
        refresh_cache()


# =====================================================
# GET CACHE
# =====================================================
def get_cached_signals():
    ensure_cache_fresh()
    return CACHE["signals"]


# =====================================================
# LIVE SIGNALS
# =====================================================
@router.get("/live")
def get_live_signals(limit: int = Query(10, ge=1, le=50)):

    signals = get_cached_signals()[:limit]

    return {
        "status": "ok",
        "engine": "DynamoHive",
        "count": len(signals),
        "signals": signals
    }


# =====================================================
# FILTER
# =====================================================
@router.get("/filter")
def filter_signals(severity: str = None):

    signals = get_cached_signals()

    if severity:
        signals = [
            s for s in signals
            if s.get("severity") == severity
        ]

    return {
        "status": "ok",
        "count": len(signals),
        "signals": signals
    }


# =====================================================
# HISTORY
# =====================================================
@router.get("/history")
def get_history():

    return {
        "status": "ok",
        "mode": "cached_snapshot",
        "last_update": CACHE["last_update"],
        "count": len(CACHE["signals"]),
        "signals": CACHE["signals"]
    }
