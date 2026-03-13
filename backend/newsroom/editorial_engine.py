# backend/newsroom/editorial_engine.py

def apply_editorial_layer(story):

    if not story:
        return None

    story["author"] = "DynamoHive AI"
    story["type"] = "Intelligence Brief"

    return story
