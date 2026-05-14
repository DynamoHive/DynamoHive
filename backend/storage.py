import sqlite3
import time
import json

DB_PATH = "dynamo.db"


def init_db():
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


def save_signal(item):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO signals (title, topic, content, priority, published, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        item.get("title"),
        item.get("topic"),
        item.get("content"),
        item.get("priority", 0.5),
        1 if item.get("published") else 0,
        item.get("timestamp", int(time.time()))
    ))

    conn.commit()
    conn.close()


def get_signals(limit=50):
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
