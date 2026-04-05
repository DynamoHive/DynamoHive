# -------------------------
# GLOBAL TREND STORAGE
# -------------------------

trend_scores = {}


# -------------------------
# HELPERS
# -------------------------

def normalize_topic(t):
    try:
        return str(t).lower().strip()
    except:
        return ""


# -------------------------
# UPDATE TRENDS
# -------------------------

def update_trends(topics):

    global trend_scores

    try:
        if not isinstance(topics, list):
            return

        for t in topics:

            topic = normalize_topic(t)

            if not topic:
                continue

            if topic not in trend_scores:
                trend_scores[topic] = 0

            trend_scores[topic] += 1

    except:
        pass


# -------------------------
# GET TRENDING
# -------------------------

def get_trending(top_n=5):

    try:
        if not isinstance(top_n, int) or top_n <= 0:
            top_n = 5

        items = list(trend_scores.items())

        # güvenli sort
        try:
            items.sort(key=lambda x: x[1], reverse=True)
        except:
            items = sorted(
                items,
                key=lambda x: x[1] if isinstance(x, tuple) and len(x) > 1 else 0,
                reverse=True
            )

        return items[:top_n]

    except:
        return []
