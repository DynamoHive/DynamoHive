# ai_engine/anomaly_engine.py

def detect_anomalies(signals, events):

    anomalies = []

    # -------------------------
    # 🔥 SIGNAL ANOMALIES
    # -------------------------
    for s in signals or []:

        try:
            score = float(s.get("score", 0))
        except:
            score = 0

        topic = (
            s.get("text")
            or s.get("topic")
            or "unknown"
        )

        # yüksek skor anomalisi
        if score > 15:
            anomalies.append({
                "type": "high_signal_score",
                "topic": topic,
                "value": round(score, 2)
            })

    # -------------------------
    # 🔥 EVENT SPIKE ANOMALIES
    # -------------------------
    for e in events or []:

        try:
            velocity = float(e.get("velocity", 0))
        except:
            velocity = 0

        topic = (
            e.get("topic")
            or "unknown"
        )

        if velocity > 0.05:
            anomalies.append({
                "type": "event_spike",
                "topic": topic,
                "velocity": round(velocity, 4)
            })

    # -------------------------
    # 🔥 SORT (önemli)
    # -------------------------
    anomalies.sort(
        key=lambda x: (
            x.get("value", 0),
            x.get("velocity", 0)
        ),
        reverse=True
    )

    return anomalies
