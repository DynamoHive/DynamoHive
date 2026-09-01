import time


class AdaptiveDecisionEngine:

    def __init__(self, state):
        self.state = state

        # başlangıç eşikleri
        self.base_threshold = 0.22
        self.min_threshold = 0.12
        self.max_threshold = 0.35

        self.current_threshold = self.base_threshold

    # -------------------------
    # DYNAMIC THRESHOLD UPDATE
    # -------------------------
    def adjust(self, signals_count, generated_count, crisis_count):

        try:
            if signals_count == 0:
                return self.current_threshold

            ratio = generated_count / max(signals_count, 1)

            # -------------------------
            # CRISIS MODE
            # -------------------------
            if crisis_count > 10:
                self.current_threshold = self.min_threshold

            # -------------------------
            # LOW OUTPUT → loosen filter
            # -------------------------
            elif ratio < 0.1:
                self.current_threshold *= 0.85

            # -------------------------
            # HIGH OUTPUT → tighten filter
            # -------------------------
            elif ratio > 0.4:
                self.current_threshold *= 1.05

            # clamp
            self.current_threshold = max(
                self.min_threshold,
                min(self.current_threshold, self.max_threshold)
            )

            self.state.set("decision_threshold", self.current_threshold)

            return self.current_threshold

        except Exception:
            return self.current_threshold

    # -------------------------
    # DECISION OVERRIDE LAYER
    # -------------------------
    def should_publish(self, item):

        try:
            priority = item.get("priority", 0)

            # hard override (critical content)
            if priority >= 0.30:
                return True

            # adaptive gate
            return priority >= self.current_threshold

        except:
            return False
