from backend.storage import get_signals


# =====================================================
# SIGNAL ENGINE (SINGLE SOURCE OF TRUTH)
# =====================================================
def run_signal_engine(limit: int = 50):

    try:
        signals = get_signals(limit=limit)

        if not signals:
            return {
                "status": "ok",
                "engine": "DynamoHive",
                "count": 0,
                "signals": []
            }

        # normalize output
        normalized = []

        for s in signals:

            normalized.append({
                "title": s.get("title"),
                "topic": s.get("topic"),
                "content": s.get("content"),
                "priority": s.get("priority", 0.5),
                "timestamp": s.get("timestamp"),
                "published": s.get("published", 1)
            })

        return {
            "status": "ok",
            "engine": "DynamoHive",
            "count": len(normalized),
            "signals": normalized
        }

    except Exception as e:

        return {
            "status": "error",
            "engine": "DynamoHive",
            "count": 0,
            "signals": [],
            "error": str(e)
        }
