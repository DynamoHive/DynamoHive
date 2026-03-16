from database import get_cursor


def get_topics():

    cursor = get_cursor()

    cursor.execute(
        """
        SELECT topic, COUNT(*) as count
        FROM posts
        GROUP BY topic
        ORDER BY count DESC
        """
    )

    topics = cursor.fetchall()

    return topics
