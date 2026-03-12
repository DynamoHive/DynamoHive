from collections import deque
import hashlib


class MemoryPatternEngine:

    def __init__(self, size=500):

        self.memory = deque(maxlen=size)

    def _fingerprint(self, signal):

        text = str(signal)

        return hashlib.md5(text.encode()).hexdigest()

    def store(self, signal):

        fp = self._fingerprint(signal)

        self.memory.append(fp)

    def seen_before(self, signal):

        fp = self._fingerprint(signal)

        return fp in self.memory

    def pattern_score(self, signal):

        fp = self._fingerprint(signal)

        count = list(self.memory).count(fp)

        return count
