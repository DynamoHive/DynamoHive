import sys
import os
from contextlib import asynccontextmanager

# make project root visible to Python
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import sqlite3
from threading import Thread

from backend.storage import get_posts

# 🔥 ROUTER EKLENDİ
from backend.api.routes.posts import router as posts_router


# -------------------------
# PATHS
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")
DATABASE_DIR = os.path.join(BASE_DIR, "..", "database")
DB_PATH = os.path.join(DATABASE_DIR, "dynamohive.db")


# -------------------------
# DATABASE INIT
# -------------------------

def init_database():

    os.makedirs(DATABASE_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
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


# -------------------------
# AI ORCHESTRATOR
# -------------------------

def start_orchestrator():

    try:
        from backend.orchestrator import start

        print("Starting DynamoHive AI engine")
        start()

    except Exception as e:
        print("AI engine failed:", e)


# -------------------------
# LIFESPAN STARTUP
# -------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("DynamoHive boot sequence")

    try:
        init_database()
        print("Database ready")
    except Exception as e:
        print("Database error:", e)

    try:
        thread = Thread(target=start_orchestrator, daemon=True)
        thread.start()
        print("AI engine started")
    except Exception as e:
        print("AI engine failed:", e)

    yield


app = FastAPI(
    title="DynamoHive",
    version="1.0",
    lifespan=lifespan
)


# -------------------------
# ROUTES (🔥 KRİTİK)
# -------------------------

app.include_router(posts_router)


# -------------------------
# STATIC
# -------------------------

os.makedirs(STATIC_DIR, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# -------------------------
# ROOT
# -------------------------

@app.get("/")
def home():
    return {"status": "DynamoHive running"}


# -------------------------
# API FEED (opsiyonel)
# -------------------------

@app.get("/api/feed")
def feed_api():

    try:
        posts = get_posts()
    except Exception as e:
        print("Feed error:", e)
        posts = []

    return {
        "platform": "DynamoHive",
        "feed": posts
    }


# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/health")
def health():
    return {"status": "ok"}
