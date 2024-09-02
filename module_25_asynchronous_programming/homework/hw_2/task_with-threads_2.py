import threading
from queue import Queue
from pathlib import Path
import time
import requests

URL = 'https://picsum.photos/800'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

# Очередь для хранения загруженных изображений
image_queue = Queue()


def get_pic(url: str, idx: int):
    response = requests.get(url, timeout=(15, 15))
    if response.status_code == 200:
        print(f"Downloaded image {idx}")
        image_queue.put((idx, response.content))
    else:
        print(f"Failed to download image {idx}")


def save_pic():
    while True:
        idx, content = image_queue.get()
        if idx is None:  # сигнал для завершения работы
            break
        with open(f"{OUT_PATH}/cat_{idx}.png", "wb") as f:
            f.write(content)
        print(f"Saved image {idx}")
        image_queue.task_done()


def main():
    threads = []

    # Запуск потока для сохранения изображений
    saver_thread = threading.Thread(target=save_pic)
    saver_thread.start()

    # Запуск потоков для загрузки изображений
    for id in range(CATS_WE_WANT):
        thread = threading.Thread(target=get_pic, args=(URL, id))
        thread.start()
        threads.append(thread)

    # Ожидание завершения загрузки всех изображений
    for thread in threads:
        thread.join()

    # Добавление сигнала завершения для потока сохранения
    image_queue.put((None, None))
    saver_thread.join()


if __name__ == "__main__":
    time_start = time.time()
    main()
    print(f"Time taken: {time.time() - time_start:.2f} seconds")
