import threading
from pathlib import Path
import time
import requests

URL = 'https://picsum.photos/800'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'threads'
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
    threads = []
    for id in range(CATS_WE_WANT):
        thread = threading.Thread(target=download_and_save_pic, args=(id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    time_start = time.time()
    main()
    print(round(time.time() - time_start, 5))
