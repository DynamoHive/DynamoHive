from database.database import cursor, conn


def create_post(title, content, topic):

    cursor.execute(

        """
        INSERT INTO posts(title,content,topic)
        VALUES (%s,%s,%s)
        """,

        (title, content, topic)

    )

    conn.commit()


def get_feed():

    cursor.execute(

        """
        SELECT id,title,content,topic,created_at
        FROM posts
        ORDER BY id DESC
        LIMIT 50
        """

    )

    rows = cursor.fetchall()

    posts = []

    for r in rows:

        posts.append({

            "id": r[0],
            "title": r[1],
            "content": r[2],
            "topic": r[3],
            "created_at": str(r[4])

        })

    return posts


def get_post(post_id):

    cursor.execute(

        "SELECT id,title,content,topic,created_at FROM posts WHERE id=%s",

        (post_id,)

    )

    r = cursor.fetchone()

    if not r:
        return None

    return {

        "id": r[0],
        "title": r[1],
        "content": r[2],
        "topic": r[3],
        "created_at": str(r[4])

    }
