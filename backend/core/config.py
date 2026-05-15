import os


# =====================================================
# DYNAMOHIVE CORE CONFIG
# =====================================================

class Config:

    # -----------------------------
    # APP INFO
    # -----------------------------
    APP_NAME = "DynamoHive"
    VERSION = "1.0.0"
    ENV = os.getenv("ENV", "development")

    # -----------------------------
    # SERVER
    # -----------------------------
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8000))

    # -----------------------------
    # SECURITY
    # -----------------------------
    API_SECRET = os.getenv("API_SECRET", "dev-secret-change-me")
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-jwt-secret")

    # -----------------------------
    # DATABASE / CACHE
    # -----------------------------
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # -----------------------------
    # ORCHESTRATOR SETTINGS
    # -----------------------------
    CYCLE_INTERVAL = int(os.getenv("CYCLE_INTERVAL", 20))
    MAX_CACHE_ITEMS = int(os.getenv("MAX_CACHE_ITEMS", 100))

    # -----------------------------
    # BILLING (Stripe placeholder)
    # -----------------------------
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # -----------------------------
    # FEATURE FLAGS
    # -----------------------------
    ENABLE_CRAWLER = True
    ENABLE_INTELLIGENCE = True
    ENABLE_CRISIS_RADAR = True
