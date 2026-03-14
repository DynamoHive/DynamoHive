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


def save_post(title, content):

    init_posts_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (title, content)
    )

    conn.commit()
    conn.close()


def get_posts():

    init_posts_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "title": r["title"],
            "content": r["content"],
            "created_at": r["created_at"]
        }
        for r in rows
    ]
    
