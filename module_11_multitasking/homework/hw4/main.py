import logging
import queue
import threading
import time
import random


logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        logger.info("Producer Running")

    def run(self):
        task_priorities = [
            random.randint(0, 6) for _ in range(10)
        ]  # Пример задач с приоритетами
        for priority in task_priorities:
            sleep = random.uniform(0.1, 0.5)
            logger.info(f"Adding Task(priority={priority}).       sleep({sleep})")
            self.queue.put((priority, sleep))  # Помещаем задачу в очередь
            time.sleep(sleep)  # Случайная задержка
        logger.info("Producer Done")


class Consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        logger.info("Consumer Running")

    def run(self):
        while True:
            priority, sleep = (
                self.queue.get()
            )  # Получаем задачу с наивысшим приоритетом
            logger.info(f"Running Task(priority={priority}).        sleep({sleep})")
            time.sleep(1)  # Имитируем выполнение задачи
            self.queue.task_done()  # Уведомляем очередь о завершении задачи
            if self.queue.empty():
                logger.info("Consumer Done")
                break


def main():
    task_queue = queue.PriorityQueue()  # Создаем приоритетную очередь

    producer = Producer(task_queue)
    consumer = Consumer(task_queue)

    producer.start()  # Запускаем Producer
    producer.join()  # Ожидаем завершения Producer (добавления всех задач в очередь)

    consumer.start()  # Запускаем Consumer
    task_queue.join()  # Блокируем очередь, пока все задачи не будут выполнены


if __name__ == "__main__":
    main()
