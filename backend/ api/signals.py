from fastapi import APIRouter, Query
from datetime import datetime
import random

router = APIRouter()

# -------------------------
# SIGNAL CORE TYPES
# -------------------------
SIGNAL_TYPES = ["economic", "social", "crisis", "tech"]
SEVERITY_LEVELS = ["low", "medium", "high"]


# -------------------------
# SIGNAL GENERATOR (mock engine placeholder)
# -------------------------
def build_signal():
    severity = random.choice(SEVERITY_LEVELS)

    return {
        "signal_id": f"sig_{random.randint(10000, 99999)}",
        "type": random.choice(SIGNAL_TYPES),
        "severity": severity,
        "confidence": round(random.uniform(0.55, 0.99), 2),
        "impact_score": round(random.uniform(0.1, 1.0), 2),
        "source_cluster": [
            f"feed_{random.randint(1,5)}",
            f"feed_{random.randint(6,10)}"
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# -------------------------
# LIVE SIGNALS
# -------------------------
@router.get("/live")
def get_live_signals(limit: int = Query(5, ge=1, le=20)):
    signals = [build_signal() for _ in range(limit)]

    return {
        "status": "ok",
        "mode": "live_mock",
        "count": len(signals),
        "signals": signals
    }


# -------------------------
# FILTERED SIGNALS
# -------------------------
@router.get("/filter")
def filter_signals(
    severity: str = None,
    signal_type: str = None
):
    signals = [build_signal() for _ in range(15)]

    if severity:
        signals = [s for s in signals if s["severity"] == severity]

    if signal_type:
        signals = [s for s in signals if s["type"] == signal_type]

    return {
        "status": "ok",
        "filters": {
            "severity": severity,
            "type": signal_type
        },
        "count": len(signals),
        "signals": signals
    }


# -------------------------
# HISTORY (mock stream)
# -------------------------
@router.get("/history")
def get_history():
    return {
        "status": "ok",
        "mode": "historical_mock",
        "signals": [build_signal() for _ in range(30)]
    }
