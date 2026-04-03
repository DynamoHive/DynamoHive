class DominanceCore:

    def rank(self, items):

        if not items:
            return []

        ranked = sorted(
            items,
            key=lambda x: (
                x.get("score", 0),
                x.get("cluster_size", 1),
                x.get("momentum", 0)
            ),
            reverse=True
        )

        for i, item in enumerate(ranked):
            item["rank"] = i + 1

        return ranked[:20]
