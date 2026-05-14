from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import uuid
import time

# Core API key system (senin mevcut dosyan)
from backend.auth import create_api_key, validate_api_key

router = APIRouter()

# -------------------------
# MOCK USER STORE (sonra DB olacak)
# -------------------------
USERS = {}
REFRESH_TOKENS = {}


# -------------------------
# MODELS
# -------------------------
class LoginRequest(BaseModel):
    email: str
    password: str


# -------------------------
# HELPERS
# -------------------------
def create_token():
    return str(uuid.uuid4())


# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(data: LoginRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    user_id = str(uuid.uuid4())

    access_token = create_token()
    refresh_token = create_token()

    api_key = create_api_key(user_id)

    USERS[user_id] = {
        "email": data.email,
        "created_at": time.time()
    }

    REFRESH_TOKENS[refresh_token] = user_id

    return {
        "user_id": user_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "api_key": api_key,
        "expires_in": 3600
    }


# -------------------------
# CURRENT USER (API KEY CHECK)
# -------------------------
@router.get("/me")
def me(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    if not validate_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    user_id = None

    # reverse lookup (mock)
    from backend.auth import API_KEYS
    user_id = API_KEYS.get(x_api_key)

    return {
        "status": "ok",
        "user_id": user_id,
        "user": USERS.get(user_id)
    }


# -------------------------
# REFRESH TOKEN
# -------------------------
@router.post("/refresh")
def refresh(refresh_token: str):
    if refresh_token not in REFRESH_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {
        "access_token": create_token(),
        "expires_in": 3600
    }
