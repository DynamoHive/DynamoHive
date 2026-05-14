from database import get_cursor


def get_topics():

    cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT topic, COUNT(*) as count
            FROM posts
            GROUP BY topic
            ORDER BY count DESC
            """
        )

        rows = cursor.fetchall() or []

        return [
            {
                "topic": r[0],
                "count": r[1]
            }
            for r in rows
        ]

    finally:
        cursor.close()
