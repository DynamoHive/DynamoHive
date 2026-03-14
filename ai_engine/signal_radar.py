from collections import deque
from datetime import datetime, timezone

class SignalRadar:

    def __init__(self, size=100):
        self.signals = deque(maxlen=size)

    def push(self, signal):
        if not isinstance(signal, dict) or "title" not in signal:
            raise ValueError("Signal must be a dictionary with at least a 'title' key")

        signal_entry = {
            "signal": signal,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.signals.append(signal_entry)

    def latest(self, n=10):
        return list(self.signals)[-n:]

    def all(self):
        return list(self.signals)
