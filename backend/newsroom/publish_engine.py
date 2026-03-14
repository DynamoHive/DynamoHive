from database.database import get_connection


def publish_article(article):

    if not article:
        return False

    title = article.get("title", "")
    content = article.get("content", "")

    if not title:
        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO posts (title, content)
        VALUES (?, ?)
    """, (title, content))

    conn.commit()
    conn.close()

    return True
