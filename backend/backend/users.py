from fastapi import APIRouter

router = APIRouter()

users = []

@router.post("/users/register")
def register_user(username: str, email: str):
    user = {
        "id": len(users) + 1,
        "username": username,
        "email": email
    }
    users.append(user)
    return {"message": "user registered", "user": user}

@router.get("/users")
def list_users():
    return {"users": users}
