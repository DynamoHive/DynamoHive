import random


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

    content = " ".join(paragraphs)

    return content



def generate_content(intelligence):

    if not intelligence:
        return None

    topic = intelligence.get("topic", "technology")

    title = build_title(topic)

    content = build_content(topic)

    post = {

        "title": title,
        "content": content,
        "topic": topic

    }

    print("content generated:", title)

    return post
