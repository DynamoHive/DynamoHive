

def add_task(task, *args):

    TASK_QUEUE.put((task, args))


def worker():

    while True:

        task, args = TASK_QUEUE.get()

        try:
            task(*args)

        except Exception as e:
            print("task error:", e)

        TASK_QUEUE.task_done()


def start_workers(count=2):

    for _ in range(count):

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
