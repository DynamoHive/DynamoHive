import sys
import os

# make project root visible to Python
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# preload database module (fix for database.database import)
import database.database

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import sqlite3
from threading import Thread

from backend.storage import get_posts


app = FastAPI(
    title="DynamoHive",
    version="1.0"
)

# -------------------------
# PATHS
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

DATABASE_DIR = os.path.join(BASE_DIR, "..", "database")
DB_PATH = os.path.join(DATABASE_DIR, "dynamohive.db")


# -------------------------
# TEMPLATES
# -------------------------

templates = Jinja2Templates(directory=TEMPLATES_DIR)


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
# STARTUP
# -------------------------

@app.on_event("startup")
def startup():

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


# -------------------------
# LANDING PAGE
# -------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -------------------------
# DASHBOARD
# -------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


# -------------------------
# FEED PAGE
# -------------------------

@app.get("/feed", response_class=HTMLResponse)
def feed_page(request: Request):

    return templates.TemplateResponse(
        "feed.html",
        {"request": request}
    )


# -------------------------
# API FEED
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
