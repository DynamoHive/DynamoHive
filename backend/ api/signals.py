from fastapi import APIRouter, Query

from ai_engine.signal_engine import (
    run_signal_engine
)

router = APIRouter()


# -------------------------
# LIVE SIGNALS
# -------------------------
@router.get("/live")
def get_live_signals(
    limit: int = Query(10, ge=1, le=50)
):

    result = run_signal_engine()

    signals = result.get("signals", [])[:limit]

    return {
        "status": "ok",
        "engine": "DynamoHive",
        "count": len(signals),
        "signals": signals
    }


# -------------------------
# FILTERED SIGNALS
# -------------------------
@router.get("/filter")
def filter_signals(
    severity: str = None
):

    result = run_signal_engine()

    signals = result.get("signals", [])

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


# -------------------------
# HISTORY PLACEHOLDER
# -------------------------
@router.get("/history")
def get_history():

    result = run_signal_engine()

    return {
        "status": "ok",
        "mode": "historical_placeholder",
        "signals": result.get("signals", [])
    }
