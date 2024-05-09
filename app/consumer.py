from multiprocessing import Process, Pool

from app.webscrapper import scrap_process
import time


default_depth = 5

def add_url_to_queue(queue, url: str):
    """Función para añadir una URL a la cola."""
    queue.put({'url': url, 'depth': default_depth})


def consumer_handler(queue):
    """Función consumidora que maneja los elementos de la cola."""

    results = []
    with Pool(8) as pool:
        while True:
            while not queue.empty():
                item = queue.get()
                url = item['url']
                depth = item['depth']
                print(f'[ ======= ] Url {url} con depth {depth} agregado.')
                if depth > 0:
                    result = pool.apply_async(scrap_process, (url, depth, queue))
                    results.append(result)

                # Limpiar y verificar resultados completados
            results = [r for r in results if not r.ready()]  # Mantener solo tareas no completadas

            if not results and queue.empty():
                break  # Si no hay tareas activas y la cola está vacía, termina el bucle

            time.sleep(0.1)



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
