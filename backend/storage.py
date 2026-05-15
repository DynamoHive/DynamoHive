import sqlite3
import time
import threading

from backend.logger import logger

DB_PATH = "dynamo.db"

_lock = threading.Lock()


# =====================================================
# CONNECTION
# =====================================================
def get_connection():
    # safer + consistent config
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# =====================================================
# INIT DB
# =====================================================
def init_db():
    try:
        with _lock:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
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

            logger.info("[DB] initialized")

    except Exception as e:
        logger.error(f"[DB INIT ERROR] {e}")


# =====================================================
# SAVE SIGNAL
# =====================================================
def save_signal(item: dict):
    try:
        with _lock:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
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
        logger.error(f"[DB SAVE ERROR] {e}")


# =====================================================
# GET SIGNALS
# =====================================================
def get_signals(limit: int = 50):
    try:
        with _lock:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT title, topic, content, priority, published, timestamp
                FROM signals
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()
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
        logger.error(f"[DB GET ERROR] {e}")
        return []


# =====================================================
# CLEANUP OLD DATA
# =====================================================
def cleanup(max_age_seconds: int = 86400):
    try:
        cutoff = int(time.time()) - max_age_seconds

        with _lock:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM signals
                WHERE timestamp < ?
            """, (cutoff,))

            conn.commit()
            conn.close()

        logger.info("[DB] cleanup done")

    except Exception as e:
        logger.error(f"[DB CLEANUP ERROR] {e}")


# =====================================================
# COUNT
# =====================================================
def count_signals():
    try:
        with _lock:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM signals")
            count = cursor.fetchone()[0]

            conn.close()

        return count

    except Exception as e:
        logger.error(f"[DB COUNT ERROR] {e}")
        return 0
