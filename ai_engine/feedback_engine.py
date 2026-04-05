class FeedbackEngine:

    def __init__(self):
        self.history = []

    def ingest(self, items):

        feedback_data = []

        for item in items:

            score = item.get("score", 0)
            engagement = item.get("engagement", 0)

            success = False

            if engagement > 0:
                ratio = engagement / max(score, 1)
                success = ratio > 1.5

            feedback = {
                "topic": item.get("topic"),
                "score": score,
                "engagement": engagement,
                "success": success
            }

            feedback_data.append(feedback)

        self.history.extend(feedback_data)

        return feedback_data
