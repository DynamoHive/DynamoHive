import sqlite3

DB_PATH = "database/dynamohive.db"

def get_posts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # tablo yoksa oluştur
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # veri çek
    cur.execute("SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC LIMIT 50")
    rows = cur.fetchall()
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
