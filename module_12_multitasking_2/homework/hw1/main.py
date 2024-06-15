import sqlite3
import logging
import threading
import time
from multiprocessing.pool import ThreadPool
import multiprocessing
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
URL = "https://swapi.dev/api/people/{}/"
INPUT_VALUES = [URL.format(i + 1) for i in range(20)]


def get_info(url: str):
    try:
        response = requests.get(url, timeout=(5, 5))
        if response.status_code == 200:
            data = response.json()
            data_tuple = (data["name"], data["birth_year"], data["gender"])
            # logger.info(f"Added object by name {data_tuple[0]}")
            return data_tuple
        else:
            logger.error(f"Error {response.status_code} for URL {url}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request exception: {e} for URL {url}")
        return None


def load_info_with_threadpool():
    pool = ThreadPool(processes=multiprocessing.cpu_count() * 5)
    start = time.time()
    result = pool.map(get_info, INPUT_VALUES)
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f"Time taken with threadpool - {end - start}")
    return result


def load_info_with_processpool():
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start = time.time()
    result = pool.map(get_info, INPUT_VALUES)
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f"Time taken with processpool - {end - start}")
    return result


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
            if data != None:
                cursor.execute(insert_query, data)
            else:
                pass
        logger.info("SQLite Data Base {} is created".format(name_db))


def main():
    processpool_lst = load_info_with_processpool()
    threadpool_list = load_info_with_threadpool()

    # print(threadpool_list)
    # print(processpool_lst)
    create_db("thread.db", threadpool_list)
    create_db("process.db", processpool_lst)


if __name__ == "__main__":
    main()
