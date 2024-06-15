import logging
from datetime import datetime
import requests
import multiprocessing

from flask import Flask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app: Flask = Flask(__name__)


@app.route('/timestamp/<timestamp>')
def get_timestamp(timestamp: str) -> str:
    timestamp: float = float(timestamp)
    return str(datetime.fromtimestamp(timestamp))


URL = '127.0.0.1:8080/timestamp/'



def task(url:str):
    url = f'{url}{datetime.now().fromtimestamp()}'
    response = requests.get(url, timeout=(20, 20))
    print(response)
    return response

def worker(queue: multiprocessing.Queue):
    while not queue.empty():
        obj = queue.get()


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
