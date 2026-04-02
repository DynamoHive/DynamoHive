def distribute(post):

    if not post:
        return

    # 🔥 güvenli title alma
    if isinstance(post, dict):
        text = post.get("title", "No Title")
    else:
        text = str(post)

    post_x(text)
    post_linkedin(text)
    post_reddit(text)


def post_x(text):
    print("X:", text)


def post_linkedin(text):
    print("LinkedIn:", text)


def post_reddit(text):
    print("Reddit:", text)
