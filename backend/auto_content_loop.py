import time
import random

topics = [
    "AI regulation in Europe",
    "China technology strategy",
    "Middle East power balance",
    "Future of global energy",
    "Digital surveillance economy",
    "Geopolitics of artificial intelligence",
]


def generate_content():

    topic = random.choice(topics)

    article = {
        "title": topic,
        "content": f"Analysis about {topic}",
        "author": "DynamoHive AI"
    }

    print("Generated content:", article)

    return article


def run():

    article = generate_content()

    print("Publishing:", article)
 
