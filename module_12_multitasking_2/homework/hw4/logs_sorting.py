import logging
import time
from datetime import datetime
import requests
import queue
import threading

from flask import Flask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "http://127.0.0.1:8080/timestamp/"
log_queue = queue.Queue()


def task():
    end_time = time.time() + 20
    while time.time() < end_time:
        timestamp = datetime.now().timestamp()
        url = f"{URL}{timestamp}"
        try:
            response = requests.get(url, timeout=(5, 5))
            logger.info(f"{timestamp}, {response.text}")
            log_queue.put((timestamp, response.text))
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
        time.sleep(1)


def log_writer():
    with open("log.txt", "a") as log_file:
        while True:
            log_entry = log_queue.get()
            if log_entry is None:
                break
            timestamp, log_data = log_entry
            log_file.write(f"{timestamp} {log_data}\n")
            log_queue.task_done()


if __name__ == "__main__":
    log_thread = threading.Thread(target=log_writer)
    log_thread.start()
    threads = []
    start = time.time()

    for _ in range(10):
        thread = threading.Thread(target=task)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    log_queue.put(None)
    log_thread.join()
