from collections import deque
from datetime import datetime, timezone

class SignalRadar:

    def __init__(self, size=100):
        self.signals = deque(maxlen=size)

    def push(self, signal):

        entry = {
            "title": signal.get("title", "Unknown signal"),
            "score": signal.get("score", 50),
            "lat": signal.get("lat", 0),
            "lon": signal.get("lon", 0),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.signals.append(entry)

    def latest(self, n=10):
        return list(self.signals)[-n:]

    def all(self):
        return list(self.signals)


radar = SignalRadar()


def get_latest_signals():

    if not radar.signals:

        radar.push({
            "title": "Energy Market Instability",
            "score": 82,
            "lat": 48,
            "lon": 16
        })

        radar.push({
            "title": "AI Strategic Competition",
            "score": 71,
            "lat": 37,
            "lon": -122
        })

        radar.push({
            "title": "Supply Chain Stress",
            "score": 64,
            "lat": 31,
            "lon": 121
        })

    return radar.latest(10)
