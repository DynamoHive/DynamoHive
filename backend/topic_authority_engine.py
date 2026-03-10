topics = {
    "ai_geopolitics": [
        "AI regulation in Europe",
        "AI regulation in US",
        "China AI strategy",
        "AI arms race",
        "AI governance models"
    ],

    "energy_transition": [
        "Global energy crisis",
        "Energy geopolitics",
        "Europe energy security",
        "Future of nuclear energy",
        "Renewable energy strategy"
    ],

    "china_technology": [
        "China semiconductor strategy",
        "US-China technology war",
        "Chinese AI ecosystem",
        "China digital economy",
        "Tech sanctions impact"
    ]
}


def generate_topic_content():

    articles = []

    for category in topics:

        for t in topics[category]:

            article = {
                "category": category,
                "title": t,
                "author": "DynamoHive AI"
            }

            articles.append(article)

    print("Topic authority articles:", len(articles))

    return articles


def run():

    generate_topic_content()
