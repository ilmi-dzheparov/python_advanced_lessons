import string
import random

import requests
import time
import typing as tp
from concurrent.futures import ThreadPoolExecutor

class BookClient:
    URL = 'http://127.0.0.1:5000/api/books'
    TIMEOUT = 5

    def __init__(self):
        self._session = requests.Session()

    def get_all_books(self) -> tp.Dict:
        response = self._session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: tp.Dict):
        response = self._session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            return ValueError('Wrong params. Response message: {}'.format(response.json()))

    def save_session(self):
        self._session.close()

def generate_random_word(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def json_data():
    json_req = {'title': generate_random_word(15), 'author': 'Me'}
    return json_req



def run_test(client, num_request, method='get', use_session=False, use_threads=False):
    URL = 'http://127.0.0.1:5000/api/books'
    def make_request():
        if use_session:
            if method == 'get':
                return client.get_all_books()
            elif method == 'post':
                return client.add_new_book(json_data())
        else:
            if method == 'get':
                return requests.get(URL)
            elif method == 'post':
                return requests.post(URL, json=json_data())

    start_time = time.time()
    if use_threads:
        with ThreadPoolExecutor() as executor:
            executor.map(make_request, range(num_request))
    else:
        for _ in range(num_request):
            make_request()
    end_time = time.time()
    return end_time - start_time


if __name__ == "__main__":
    client = BookClient()
    print(round(run_test(client, 1000, method='post'), 5))
    print(round(run_test(client, 1000, use_threads=True, method='post'), 5))
    print(round(run_test(client, 1000, use_session=True, method='post'), 5))
    print(round(run_test(client, 1000, use_session=True, use_threads=True, method='post'), 5))
