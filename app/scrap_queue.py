from multiprocessing import Queue

# Definición global
_webscrap_queue = None


def get_webscrap_queue():
    global _webscrap_queue
    if _webscrap_queue is None:
        _webscrap_queue = Queue()
    return _webscrap_queue