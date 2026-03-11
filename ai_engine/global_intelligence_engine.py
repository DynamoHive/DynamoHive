from database.database import cursor, conn


def build_intelligence_index():

    cursor.execute(
        """
        SELECT topic, COUNT(*) as count
        FROM posts
        GROUP BY topic
        ORDER BY count DESC
        """
    )

    rows = cursor.fetchall()

    index = []

    for r in rows:

        topic = r[0]
        score = r[1]

        index.append({

            "topic": topic,
            "score": score

        })

    return index



def get_top_topics(limit=10):

    cursor.execute(
        """
        SELECT topic, COUNT(*) as count
        FROM posts
        GROUP BY topic
        ORDER BY count DESC
        LIMIT %s
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
