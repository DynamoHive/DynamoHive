def distribute(post):

    text = post["title"]

    post_x(text)
    post_linkedin(text)
    post_reddit(text)


def post_x(text):

    print("X:", text)


def post_linkedin(text):

    print("LinkedIn:", text)


def post_reddit(text):

    print("Reddit:", text)
