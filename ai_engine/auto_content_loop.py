import random
import json
from datetime import datetime


TEMPLATES = [

    "Recent developments in {topic} show significant global momentum.",
    "Experts highlight growing influence of {topic} across industries.",
    "New discussions around {topic} are shaping technological and geopolitical debates.",
    "Analysts report increasing attention toward {topic} in global policy circles."

]


def build_title(topic):

    titles = [
        f"Global developments in {topic}",
        f"New signals emerging in {topic}",
        f"Trends shaping the future of {topic}",
        f"Why {topic} is gaining global attention"
    ]

    return random.choice(titles)



def build_content(topic):

    paragraphs = []

    for template in TEMPLATES:
        paragraphs.append(template.format(topic=topic))

    return " ".join(paragraphs)



def save_post(post):

    try:

        with open("generated_posts.json", "a") as f:
            f.write(json.dumps(post) + "\n")

    except Exception as e:
        print("save error:", e)



def generate_content(intelligence):

    if not intelligence:
        return None

    topic = intelligence.get("topic", "technology")

    title = build_title(topic)
    content = build_content(topic)

    post = {

        "title": title,
        "content": content,
        "topic": topic,
        "created_at": datetime.utcnow().isoformat()

    }

    print("content generated:", title)

    save_post(post)

    return post
