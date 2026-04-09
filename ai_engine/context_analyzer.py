class ContextAnalyzer:

    def build(self, signal, memory):

        try:
            topic = str(signal.get("topic", ""))

            return {
                "actors": ["state actors"],
                "region": "global",
                "topic": topic,
                "history": memory.get("history", []),
                "insight": ""  # başlangıç boş, sonra doldurulacak
            }

        except:
            return {
                "actors": [],
                "region": "global",
                "topic": "",
                "history": [],
                "insight": ""
            }
