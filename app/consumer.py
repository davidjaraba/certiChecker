from multiprocessing import Process, Pool, Queue

from app.webscrapper import scrap_process
import time

default_depth = 5


class ExpiringSet:
    def __init__(self):
        self.elements = {}

    def add(self, element):
        """Añade un elemento con un TTL de 120 segundos."""
        current_time = time.time()
        ttl = 900  # 2 minutos en segundos
        if element not in self.elements:
            self.elements[element] = current_time + ttl
            print(f"Elemento '{element}' añadido, expirará en {ttl} segundos.")
            return True
        else:
            # print(f"Elemento '{element}' ya está en la lista.")
            return False

    def cleanup_expired_elements(self):
        """Elimina elementos expirados."""
        current_time = time.time()
        expired_keys = [key for key, expire_time in self.elements.items() if expire_time < current_time]
        for key in expired_keys:
            del self.elements[key]
            print(f"Elemento '{key}' eliminado por expiración.")

    def current_elements(self):
        """Retorna una lista de elementos no expirados."""
        self.cleanup_expired_elements()  # Limpieza antes de mostrar los elementos
        return list(self.elements.keys())


process_set = ExpiringSet()


def add_url_to_queue(queue, url: str, depth=default_depth):
    """Función para añadir una URL a la cola."""
    # print(url)
    # process_set.add(url)
    if process_set.add(url):
        queue.put({'url': url, 'depth': depth})


def consumer_handler(queue):
    """Función consumidora que maneja los elementos de la cola."""

    with Pool(processes=4) as pool:
        while True:
            try:
                print('Elementos actualmente en la cola =>>> '+str(queue.qsize()))
                item = queue.get(timeout=300)
                url = item['url']
                depth = item['depth']
                print(f'[ ======= ] Url {url} con depth {depth} agregado.')
                # pool.starmap(scrap_process, [(url, queue, depth)])
                pool.apply_async(scrap_process, args=(url, queue, depth))
            except Exception as e:
                print("No hay más elementos temporalmente en la cola, esperando más.")
                time.sleep(5)

    # results = []
    # with Pool(8) as pool:
    #     while True:
    #         while not queue.empty():
    #             item = queue.get()
    #             url = item['url']
    #             depth = item['depth']
    #             print(f'[ ======= ] Url {url} con depth {depth} agregado.')
    #             if depth > 0:
    #                 result = pool.apply_async(scrap_process, (url, depth, queue))
    #                 results.append(result)
    #
    #             # Limpiar y verificar resultados completados
    #         results = [r for r in results if not r.ready()]  # Mantener solo tareas no completadas
    #
    #         if not results and queue.empty():
    #             break  # Si no hay tareas activas y la cola está vacía, termina el bucle
    #
    #         time.sleep(0.1)

    # while True:
    #     if not queue.empty():
    #         item = queue.get()
    #         url = item['url']
    #         depth = item['depth']
    #         print(f'[ ======= ] Url {url} con depth {depth} agregado.')
    #         if depth > 0:
    # p = Process(target=scrap_process, args=(url, queue, depth))
    # p.start()
    # for new_url in new_urls:
    #     print(f'New URL: {new_url}')
    #     add_url_to_queue(queue, new_url)
