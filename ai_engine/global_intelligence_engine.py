from database import cursor


def build_intelligence_index():
    """
    Posts tablosunu analiz eder ve topic bazlı
    global intelligence index üretir.
    """

    cursor.execute(
        """
        SELECT topic, COUNT(*) as score
        FROM posts
        GROUP BY topic
        ORDER BY score DESC
        """
    )

    rows = cursor.fetchall()

    index = []

    for r in rows:
        index.append({
            "topic": r[0],
            "score": r[1]
        })

    return index


def get_top_topics(limit=10):
    """
    En güçlü topic'leri döndürür.
    """

    cursor.execute(
        """
        SELECT topic, COUNT(*) as score
        FROM posts
        GROUP BY topic
        ORDER BY score DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    topics = []

    for r in rows:
        topics.append({
            "topic": r[0],
            "authority": r[1]
        })

    return topics
