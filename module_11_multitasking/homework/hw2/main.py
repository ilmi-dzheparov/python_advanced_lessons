import sqlite3
import logging
import threading
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
URL = "https://swapi.dev/api/people/{}/"


def get_info(url: str, data_list: list):
    response = requests.get(url, timeout=(5, 5))
    if response.status_code == 200:
        data = response.json()
        data_tuple = (data["name"], data["birth_year"], data["gender"])
        data_list.append(data_tuple)
    else:
        logger.error(response.status_code)


def load_info_sequential():
    start = time.time()
    seq_list = []
    for i in range(20):
        get_info(URL.format(i + 1), seq_list)
    logger.info("Sequential request done in {:.4}".format(time.time() - start))
    return seq_list


def load_info_multithreading():
    start = time.time()
    thread_list = []
    threads = []
    for i in range(20):
        thread = threading.Thread(
            target=get_info, args=(URL.format(i + 1), thread_list)
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    logger.info("Multithreading request done in {:.4}".format(time.time() - start))
    return thread_list


def create_db(name_db: str, user_data: list):
    db_file = name_db
    with sqlite3.connect(db_file) as con:
        cursor = con.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        birth_year TEXT NOT NULL,
                        gender TEXT NOT NULL
                    )"""
        )
        insert_query = "INSERT INTO users (name, birth_year, gender) VALUES (?, ?, ?)"
        for data in user_data:
            cursor.execute(insert_query, data)
        print("SQLite Data Base {} is created".format(name_db))


def main():
    seq_list = load_info_sequential()
    thread_lst = load_info_multithreading()
    create_db("seq.db", seq_list)
    create_db("thread.db", thread_lst)


if __name__ == "__main__":
    main()
