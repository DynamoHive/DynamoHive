class ReinforcementEngine:

    def reinforce(self, items, feedbacks):

        success_topics = {
            fb["topic"] for fb in feedbacks if fb["success"]
        }

        for item in items:

            if item.get("topic") in success_topics:
                item["score"] += 1.5

        return items
