from ai_engine.signal_ranking_engine import merge_ranked_signals


# =====================================================
# MOCK / INPUT COMPATIBILITY SAFE
# =====================================================
def fetch_raw_signals():
    """
    Eğer crawler / upstream boş gelirse bile sistem çökmesin.
    """

    return []


# =====================================================
# SIGNAL NORMALIZER
# =====================================================
def normalize_signal(s):
    """
    Her engine farklı format döndürebilir.
    bunu tek standarda sokuyoruz.
    """

    if not isinstance(s, dict):
        return None

    topic = (
        s.get("topic")
        or s.get("title")
        or s.get("text")
        or "unknown"
    )

    score = s.get("score", 0.5)

    return {
        "topic": str(topic),
        "signal": {"score": float(score)},
        "prediction": {"impact_score": 0.5},
        "reasoning": {"confidence": 0.5}
    }


# =====================================================
# MAIN ENGINE
# =====================================================
def run_signal_engine():

    raw = fetch_raw_signals()

    # upstream fallback (IMPORTANT)
    if not raw or len(raw) == 0:
        return {
            "signals": []
        }

    normalized = []

    for r in raw:
        n = normalize_signal(r)
        if n:
            normalized.append(n)

    # safety fallback if everything failed
    if not normalized:
        return {
            "signals": []
        }

    # ranking layer
    try:
        ranked = merge_ranked_signals(normalized) or normalized
    except Exception:
        ranked = normalized

    # FINAL GUARANTEE: always structured output
    return {
        "status": "ok",
        "count": len(ranked),
        "signals": ranked
    }
