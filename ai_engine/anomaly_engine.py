# ai_engine/anomaly_engine.py

def detect_anomalies(signals, events):

    anomalies = []

    for s in signals:
        score = s.get("score", 0)

        if score > 15:
            anomalies.append({
                "type": "high_signal_score",
                "topic": s.get("text"),
                "value": score
            })

    for e in events:
        if e.get("velocity", 0) > 0.05:
            anomalies.append({
                "type": "event_spike",
                "topic": e.get("topic"),
                "velocity": e.get("velocity")
            })

    return anomalies
