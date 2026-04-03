import math
from collections import defaultdict

class IntelligenceLayer:

    def __init__(self):
        self.topic_memory = defaultdict(list)

    def process(self, signals):

        enriched = []

        # -------------------------
        # GROUP SIMILAR TOPICS
        # -------------------------
        clusters = self._cluster(signals)

        for cluster in clusters:

            topics = [s["topic"] for s in cluster]
            scores = [s.get("score", 1.0) for s in cluster]

            main_topic = self._select_main(topics)

            enriched.append({
                "topic": main_topic,
                "cluster_size": len(cluster),
                "score": sum(scores) / len(scores),
                "momentum": self._momentum(main_topic, scores)
            })

        return enriched

    # -------------------------
    # CLUSTER
    # -------------------------
    def _cluster(self, signals):

        clusters = []
        used = set()

        for i, s1 in enumerate(signals):

            if i in used:
                continue

            group = [s1]
            used.add(i)

            for j, s2 in enumerate(signals):
                if j in used:
                    continue

                if self._similar(s1["topic"], s2["topic"]):
                    group.append(s2)
                    used.add(j)

            clusters.append(group)

        return clusters

    def _similar(self, a, b):

        a = a.lower().split()
        b = b.lower().split()

        common = set(a) & set(b)

        return len(common) >= 2

    # -------------------------
    # SELECT MAIN TOPIC
    # -------------------------
    def _select_main(self, topics):
        return max(topics, key=len)

    # -------------------------
    # MOMENTUM (LEARNING BASE)
    # -------------------------
    def _momentum(self, topic, scores):

        history = self.topic_memory[topic]

        current = sum(scores)

        if history:
            prev = history[-1]
            delta = current - prev
        else:
            delta = current

        history.append(current)

        return round(delta, 2)
