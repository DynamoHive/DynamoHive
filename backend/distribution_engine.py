posts = []


def create_social_posts():

    global posts

    articles = [
        "AI regulation in Europe",
        "Energy crisis in Europe",
        "China technology strategy",
        "Middle East geopolitics"
    ]

    generated = []

    for a in articles:

        post = f"New analysis: {a} – Read more on DynamoHive"

        generated.append(post)

    posts = generated

    print("Distribution posts:", posts)


def run():
    create_social_posts()
