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


def register_invite(user_id):
    record_referral(user_id)


def viral_action():

    user = random.choice(fake_users)

    action = random.choice(["share", "invite", "like"])

    if action == "invite":
        register_invite(user)
        print("Viral invite:", user)

    else:
        record_engagement(user)
        print("Viral engagement:", user)


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
