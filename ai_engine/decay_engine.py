import time

class DecayEngine:

    def __init__(self, half_life=3600):
        self.half_life = half_life  # saniye

    def apply(self, items):

        now = time.time()

        for item in items:

            ts = item.get("timestamp", now)

            age = now - ts

            decay_factor = 0.5 ** (age / self.half_life)

            item["score"] *= decay_factor

        return items
