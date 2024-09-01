import multiprocessing
import threading
from pathlib import Path
import time
import requests

URL = 'https://picsum.photos/800'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'processes'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def get_pic(url: str) -> bytes:
    response = requests.get(URL, timeout=(15, 15))
    result = response.content
    print(response.status_code)
    return (result)


def save_pic(content: bytes, idx: int):
    with open(f"{OUT_PATH}/cat_{idx}.png", "wb") as f:
        f.write(content)

def download_and_save_pic(idx: int):
    content = get_pic(URL)
    save_pic(content, idx)


def main():
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() * 4)
    # pool = multiprocessing.Pool(processes=CATS_WE_WANT)
    result = pool.map(download_and_save_pic, [i for i in range(CATS_WE_WANT)])
    pool.close()
    pool.join()


if __name__ == "__main__":
    time_start = time.time()
    main()
    print(round(time.time() - time_start, 5))
    print(multiprocessing.cpu_count())
