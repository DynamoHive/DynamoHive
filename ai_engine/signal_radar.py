from collections import deque
from datetime import datetime

class SignalRadar:

    def __init__(self, size=100):

        self.signals = deque(maxlen=size)

    def push(self, signal):

        signal_entry = {
            "signal": signal,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.signals.append(signal_entry)

    def latest(self, n=10):

        return list(self.signals)[-n:]

    def all(self):

        return list(self.signals)
