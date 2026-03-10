import threading
import time
import random

from backend.growth_engine import record_referral, record_engagement

fake_users = [
    "alice",
    "bob",
    "charlie",
    "diana",
    "eric",
    "fatima",
    "george"
]


def viral_action():

    user = random.choice(fake_users)

    action = random.choice(["share", "invite", "like"])

    if action == "invite":

        record_referral(user)
        print("Viral invite by:", user)

    else:

        record_engagement(user)
        print("Viral engagement by:", user)


def viral_loop():

    while True:

        try:

            viral_action()

        except Exception as e:

            print("Viral engine error:", e)

        time.sleep(45)


def start_viral_engine():

    worker = threading.Thread(target=viral_loop)

    worker.daemon = True

    worker.start()

    print("Viral engine started")
