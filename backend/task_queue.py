import queue
import threading

task_queue = queue.Queue()


def add_task(task, *args):

    task_queue.put((task, args))


def worker():

    while True:

        task, args = task_queue.get()

        try:
            task(*args)

        except Exception as e:
            print("Task error:", e)

        task_queue.task_done()


def start_workers(num=3):

    for _ in range(num):

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
