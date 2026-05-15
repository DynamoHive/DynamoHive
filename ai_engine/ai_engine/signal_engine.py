from datetime import datetime
import random

from ai_engine.signal_ranking_engine import (
    merge_ranked_signals
)


# -------------------------
# MOCK FEED INPUTS
# -------------------------
def fetch_raw_signals():

    return [
        {
            "topic": "EU market volatility increasing",
            "text": "Economic uncertainty growing in Europe",
            "score": 0.9,
            "sources": ["news_feed"]
        },

        {
            "topic": "Major protests spreading in cities",
            "text": "Social instability signals rising",
            "score": 1.4,
            "sources": ["social_feed"]
        },

        {
            "topic": "AI regulation discussions intensify",
            "text": "Governments preparing AI restrictions",
            "score": 0.8,
            "sources": ["policy_feed"]
        },

        {
            "topic": "Major protests spreading in cities",
            "text": "Urban unrest discussions increasing",
            "score": 1.1,
            "sources": ["alternative_social_feed"]
        }
    ]


# -------------------------
# SIGNAL ENRICHMENT
# -------------------------
def enrich_signal(signal):

    signal["signal_id"] = (
        f"dh_{random.randint(100000,999999)}"
    )

    signal["timestamp"] = (
        datetime.utcnow().isoformat() + "Z"
    )

    signal["confidence"] = round(
        min(signal.get("score", 0) / 3, 0.99),
        2
    )

    return signal


# -------------------------
# MAIN ENGINE
# -------------------------
def run_signal_engine():

    raw_signals = fetch_raw_signals()

    ranked_signals = merge_ranked_signals(
        raw_signals
    )

    enriched_signals = [
        enrich_signal(signal)
        for signal in ranked_signals
    ]

    return {
        "status": "ok",
        "engine": "DynamoHive",
        "count": len(enriched_signals),
        "signals": enriched_signals
    }
