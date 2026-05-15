import sqlite3
import time
import threading

from backend.logger import logger

DB_PATH = "dynamo.db"

LOCK = threading.Lock()


# =====================================================
# DB CONNECTION (REUSABLE PATTERN)
# =====================================================
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# INIT DB
# =====================================================
def init_db():
    try:
        with LOCK:
            conn = get_connection()
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

            logger.info("[DB] initialized")

    except Exception as e:
        logger.error(f"[DB INIT ERROR] {e}")


# =====================================================
# SAVE SIGNAL
# =====================================================
def save_signal(item: dict):

    try:
        with LOCK:
            conn = get_connection()
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
        logger.error(f"[DB SAVE ERROR] {e}")


# =====================================================
# GET SIGNALS
# =====================================================
def get_signals(limit: int = 50):

    try:
        with LOCK:
            conn = get_connection()
            c = conn.cursor()

            c.execute("""
                SELECT title, topic, content, priority, published, timestamp
                FROM signals
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            rows = c.fetchall()
            conn.close()

        return [dict(r) for r in rows]

    except Exception as e:
        logger.error(f"[DB GET ERROR] {e}")
        return []


# =====================================================
# CLEANUP OLD DATA
# =====================================================
def cleanup(max_age_seconds: int = 86400):

    try:
        cutoff = int(time.time()) - max_age_seconds

        with LOCK:
            conn = get_connection()
            c = conn.cursor()

            c.execute("""
                DELETE FROM signals
                WHERE timestamp < ?
            """, (cutoff,))

            conn.commit()
            conn.close()

        logger.info("[DB] cleanup completed")

    except Exception as e:
        logger.error(f"[DB CLEANUP ERROR] {e}")


# =====================================================
# COUNT
# =====================================================
def count_signals():

    try:
        with LOCK:
            conn = get_connection()
            c = conn.cursor()

            c.execute("SELECT COUNT(*) FROM signals")
            count = c.fetchone()[0]

            conn.close()

        return count

    except Exception as e:
        logger.error(f"[DB COUNT ERROR] {e}")
        return 0
