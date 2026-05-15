from fastapi import APIRouter, Query
from ai_engine.signal_engine import run_signal_engine
import time

router = APIRouter()

# =====================================================
# SIMPLE THREAD-SAFE CACHE
# =====================================================

CACHE = {
    "signals": [],
    "last_update": 0
}

CACHE_TTL = 30  # seconds


def refresh_cache():
    """
    Engine'i kontrollü şekilde çalıştırır
    """
    global CACHE

    result = run_signal_engine()

    CACHE["signals"] = result.get("signals", [])
    CACHE["last_update"] = int(time.time())


def ensure_cache_fresh():
    """
    TTL bazlı cache kontrolü
    """
    if time.time() - CACHE["last_update"] > CACHE_TTL:
        refresh_cache()


def get_cached_signals():
    ensure_cache_fresh()
    return CACHE["signals"]


# =====================================================
# LIVE SIGNALS
# =====================================================

@router.get("/live")
def get_live_signals(
    limit: int = Query(10, ge=1, le=50)
):

    signals = get_cached_signals()[:limit]

    return {
        "status": "ok",
        "engine": "DynamoHive",
        "count": len(signals),
        "signals": signals
    }


# =====================================================
# FILTERED SIGNALS
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
# HISTORY (SNAPSHOT)
# =====================================================

@router.get("/history")
def get_history():

    return {
        "status": "ok",
        "mode": "cached_snapshot",
        "last_update": CACHE["last_update"],
        "signals": CACHE["signals"]
    }
