import time
from collections import defaultdict
from datetime import datetime

from database import cursor


WINDOW = 86400  # 24 saat


def parse_time(ts):
    try:
        return datetime.fromisoformat(ts).timestamp()
    except:
        return time.time()


def build_intelligence_index():
    """
    REAL intelligence:
    - frequency (kaç haber)
    - recency (ne kadar yeni)
    - momentum (ne kadar hızlı artıyor)
    """

    cursor.execute(
        """
        SELECT topic, created_at
        FROM posts
        WHERE topic IS NOT NULL
        """
    )

    rows = cursor.fetchall()

    now = time.time()

    topic_times = defaultdict(list)

    # -------------------------
    # 1. VERİYİ TOPLA
    # -------------------------
    for topic, created_at in rows:

        if not topic:
            continue

        t = parse_time(created_at)

        # sadece window içi
        if now - t < WINDOW:
            topic = topic.lower().strip()
            topic_times[topic].append(t)

    intelligence = []

    # -------------------------
    # 2. SCORE HESAPLA
    # -------------------------
    for topic, times in topic_times.items():

        count = len(times)

        if count == 0:
            continue

        first = min(times)
        last = max(times)

        duration = max(last - first, 1)

        # 🔥 momentum = hız
        velocity = count / duration

        # 🔥 recency bonus
        recency = max(0, 1 - ((now - last) / WINDOW))

        # 🔥 final score
        score = (count * 0.6) + (velocity * 100) + (recency * 10)

        intelligence.append({
            "topic": topic,
            "count": count,
            "velocity": round(velocity, 4),
            "recency": round(recency, 4),
            "score": round(score, 2)
        })

    # -------------------------
    # 3. SIRALA
    # -------------------------
    intelligence.sort(key=lambda x: x["score"], reverse=True)

    return intelligence


def get_top_topics(limit=10):

    data = build_intelligence_index()

    return data[:limit]


def get_topic_insight(topic):

    data = build_intelligence_index()

    for item in data:
        if item["topic"] == topic:
            return item

    return None
