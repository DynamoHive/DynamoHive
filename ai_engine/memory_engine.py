class MemoryEngine:

    def __init__(self):
        self.store = {}

    def load(self, signal):

        try:
            topic = str(
                signal.get("topic") or
                signal.get("title") or
                ""
            )

            return self.store.get(topic, {
                "history": [],
                "related_events": []
            })

        except:
            return {
                "history": [],
                "related_events": []
            }

    def save(self, signal, data):

        try:
            topic = str(
                signal.get("topic") or
                signal.get("title") or
                ""
            )

            if not topic:
                return

            self.store[topic] = data

        except:
            pass
