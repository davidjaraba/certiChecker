import multiprocessing
from multiprocessing import Process


def get_queue():
    return multiprocessing.Queue()


def consumer_handler(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consumiendo {item}")


def start_consumer(queue):
    consumer = Process(target=consumer_handler, args=(queue,))
    consumer.start()
    return consumer
