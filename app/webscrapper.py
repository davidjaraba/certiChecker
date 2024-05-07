from multiprocessing import Process
import time


def add_url_to_queue(queue, url: str):
    """Función para añadir una URL a la cola."""
    print(f"Adding URL to queue: {url}")
    print(queue)
    queue.put(url)
    print("URL added to queue")

def consumer_handler(queue):
    """Función consumidora que maneja los elementos de la cola."""

    while True:
        print(queue)
        if not queue.empty():
            item = queue.get()
            print(f'Item {item} enviado')
        else:
            print("No item enviado ")
            time.sleep(2)