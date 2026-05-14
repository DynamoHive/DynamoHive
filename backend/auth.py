import uuid

API_KEYS = {
    "demo": "demo-key-123"
}


def create_api_key(user_id: str) -> str:
    key = f"dh_{uuid.uuid4().hex[:24]}"
    API_KEYS[key] = user_id
    return key


def validate_api_key(key: str) -> bool:
    return key in API_KEYS
