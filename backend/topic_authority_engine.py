    ]
}


def generate_topic_content():

    articles = []

    for category in topics:

        for title in topics[category]:

            article = {
                "category": category,
                "title": title,
                "author": "DynamoHive AI"
            }

            articles.append(article)

    print("Topic authority articles:", len(articles))

    return articles


def run():

    return generate_topic_content()
