def recommend_posts(user_id):
    posts = [
        {"id": 1, "content": "Welcome to DynamoHive"},
        {"id": 2, "content": "AI powered creator platform"},
        {"id": 3, "content": "Discover trending creators"}
    ]

    return {
        "user": user_id,
        "recommended_posts": posts
    }
