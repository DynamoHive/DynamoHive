import threading
import time


def growth_loop():

    while True:

        print("Growth engine running")

        time.sleep(60)


def start_growth():

    worker = threading.Thread(target=growth_loop)

    worker.daemon = True

    worker.start()

    print("Growth engine started")
