import hashlib
from datetime import datetime

class SourceIntelligence:

    def __init__(self):
        self.sources = {}

    def _source_id(self, url: str):
        return hashlib.md5(url.encode()).hexdigest()

    def register(self, url: str):

        sid = self._source_id(url)

        if sid not in self.sources:
            self.sources[sid] = {
                "url": url,
                "credibility": 0.5,
                "historical_accuracy": 0.5,
                "signal_density": 0.5,
                "last_seen": datetime.utcnow()
            }

        return sid

    def score(self, url: str):

        sid = self.register(url)

        s = self.sources[sid]

        score = (
            s["credibility"] * 0.5 +
            s["historical_accuracy"] * 0.3 +
            s["signal_density"] * 0.2
        )

        return round(score, 3)

    def update(self, url: str, credibility=None, accuracy=None, density=None):

        sid = self.register(url)

        if credibility is not None:
            self.sources[sid]["credibility"] = credibility

        if accuracy is not None:
            self.sources[sid]["historical_accuracy"] = accuracy

        if density is not None:
            self.sources[sid]["signal_density"] = density
