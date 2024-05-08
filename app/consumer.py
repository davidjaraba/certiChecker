from app.webscrapper import scrap_process
import time


def add_url_to_queue(queue, url: str):
    """Función para añadir una URL a la cola."""
    queue.put(url)


def consumer_handler(queue):
    """Función consumidora que maneja los elementos de la cola."""

    while True:
        time.sleep(2)
        if not queue.empty():
            item = queue.get()
            print(f'Item {item} enviado')
            scrap_process(item)
