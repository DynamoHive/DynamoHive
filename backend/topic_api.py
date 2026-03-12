from database.database import get_cursor


def get_topics():

    cursor.execute(

        """
        SELECT topic, COUNT(*) as count
        FROM posts
        GROUP BY topic
        ORDER BY count DESC
        """

    )

    rows = cursor.fetchall()

    topics = []

    for r in rows:

        topics.append({

            "topic": r[0],
            "count": r[1]

        })

    return topics
