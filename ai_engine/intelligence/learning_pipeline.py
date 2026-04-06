class LearningPipeline:

    def __init__(self, weights=None):
        self.weights = weights or {}

    def run(self, items):

        if not isinstance(items, list):
            return []

        # şimdilik sadece passthrough (stabil çalışsın diye)
        output = []

        for item in items:

            if not isinstance(item, dict):
                continue

            score = item.get("score", 0)

            try:
                score = float(score)
            except:
                score = 0

            # küçük stabil boost (opsiyonel)
            if score > 3:
                item["score"] = score + 0.5

            output.append(item)

        return output
