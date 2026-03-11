import queue
import threading

# görev kuyruğu
task_queue = queue.Queue()


def add_task(task, *args):
    """
    Kuyruğa yeni görev ekler
    """
    task_queue.put((task, args))


def worker():
    """
    Kuyruktaki görevleri çalıştıran worker
    """

    while True:

        task, args = task_queue.get()

        try:
            task(*args)

        except Exception as e:
            print("Task error:", e)

        task_queue.task_done()


def start_workers(num=3):
    """
    Worker threadleri başlatır
    """

    for _ in range(num):

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
