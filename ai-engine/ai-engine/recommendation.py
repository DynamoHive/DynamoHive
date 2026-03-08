def recommend_posts(user_id: int = 1):
    return {
        "user": user_id,
        "recommended_posts": [
            {"id": 1, "content": "Welcome to DynamoHive"},
            {"id": 2, "content": "AI powered creator platform"},
            {"id": 3, "content": "AI recommends this post"}
        ]
    }
