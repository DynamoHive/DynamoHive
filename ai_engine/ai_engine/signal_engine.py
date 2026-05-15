from datetime import datetime
import hashlib

from ai_engine.signal_ranking_engine import merge_ranked_signals


# =====================================================
# RAW SIGNAL SOURCE (MOCK / TEMP)
# =====================================================

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


# =====================================================
# DETERMINISTIC SIGNAL ENRICHMENT
# =====================================================

def enrich_signal(signal):

    topic = signal.get("topic", "")

    # stable ID (NO RANDOM)
    signal_id = hashlib.md5(topic.encode()).hexdigest()

    signal["signal_id"] = f"dh_{signal_id[:10]}"

    signal["timestamp"] = datetime.utcnow().isoformat() + "Z"

    score = float(signal.get("score", 0))

    # normalized confidence
    signal["confidence"] = round(min(score / 3.0, 0.99), 2)

    return signal


# =====================================================
# MAIN ENGINE
# =====================================================

def run_signal_engine():

    raw_signals = fetch_raw_signals()

    if not raw_signals:
        return {"status": "ok", "engine": "DynamoHive", "signals": []}

    # ranking layer
    ranked_signals = merge_ranked_signals(raw_signals or [])

    # enrichment layer
    enriched_signals = [
        enrich_signal(signal)
        for signal in ranked_signals
    ]

    return {
        "status": "ok",
        "engine": "DynamoHive",
        "count": len(enriched_signals),
        "signals": enriched_signals,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
