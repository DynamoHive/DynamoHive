from database.database import get_connection


def init_posts_table():
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

    conn.commit()
    conn.close()


def save_post(title: str, content: str):
    if not title:
        return False

    init_posts_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (title, content or "")
    )

    conn.commit()
    conn.close()

    return True


def get_posts(limit: int = 50):
    init_posts_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    posts = []

    for r in rows:
        posts.append({
            "id": r["id"],
            "title": r["title"],
            "content": r["content"],
            "created_at": r["created_at"]
        })

    return posts
    
