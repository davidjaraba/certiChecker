import logging

from celery import Celery
import time

app = Celery('tasks', broker='sqla+sqlite:///celerydb.sqlite', backend='db+sqlite:///resultsdb.sqlite')


@app.task
def test(x, y):
    logging.info('Testing task')
    return x + y
