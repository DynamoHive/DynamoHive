import sqlite3
import time
import json
import threading

DB_PATH = "dynamo.db"

# thread safety
LOCK = threading.Lock()


# =====================================================
# INIT DB
# =====================================================
def init_db():
    with LOCK:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                topic TEXT,
                content TEXT,
                priority REAL,
                published INTEGER,
                timestamp INTEGER
            )
        """)

        conn.commit()
        conn.close()


# =====================================================
# SAVE SIGNAL (PRIMARY WRITE METHOD)
# =====================================================
def save_signal(item: dict):
    """
    Expected format:
    {
        "title": str,
        "topic": str,
        "content": str,
        "priority": float,
        "published": int (0/1),
        "timestamp": int
    }
    """

    try:
        with LOCK:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            c.execute("""
                INSERT INTO signals
                (title, topic, content, priority, published, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item.get("title"),
                item.get("topic"),
                item.get("content"),
                float(item.get("priority", 0.5)),
                int(item.get("published", 1)),
                int(item.get("timestamp", time.time()))
            ))

            conn.commit()
            conn.close()

    except Exception as e:
        print("[STORAGE ERROR] save_signal:", e)


# =====================================================
# GET SIGNALS
# =====================================================
def get_signals(limit: int = 50):
    try:
        with LOCK:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            c.execute("""
                SELECT title, topic, content, priority, published, timestamp
                FROM signals
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            rows = c.fetchall()
            conn.close()

        return [
            {
                "title": r[0],
                "topic": r[1],
                "content": r[2],
                "priority": r[3],
                "published": r[4],
                "timestamp": r[5]
            }
            for r in rows
        ]

    except Exception as e:
        print("[STORAGE ERROR] get_signals:", e)
        return []


# =====================================================
# CLEAR OLD DATA (OPTIONAL MAINTENANCE)
# =====================================================
def cleanup(max_age_seconds: int = 86400):
    """
    Remove old signals (default: 24h)
    """
    try:
        cutoff = int(time.time()) - max_age_seconds

        with LOCK:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            c.execute("""
                DELETE FROM signals
                WHERE timestamp < ?
            """, (cutoff,))

            conn.commit()
            conn.close()

    except Exception as e:
        print("[STORAGE ERROR] cleanup:", e)


# =====================================================
# COUNT SIGNALS
# =====================================================
def count_signals():
    try:
        with LOCK:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            c.execute("SELECT COUNT(*) FROM signals")
            count = c.fetchone()[0]

            conn.close()

        return count

    except Exception as e:
        print("[STORAGE ERROR] count:", e)
        return 0
