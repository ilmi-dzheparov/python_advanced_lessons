import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
TOTAL_SEATS: int = 30

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        logger.info("Director started work")

    def run(self) -> None:
        global TOTAL_TICKETS
        global TOTAL_SEATS
        start_seats = 10
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 5:
                    TOTAL_SEATS = TOTAL_SEATS - start_seats + TOTAL_TICKETS
                    start_seats = TOTAL_TICKETS + 5
                    if TOTAL_SEATS > 5:
                        TOTAL_TICKETS += 5
                    logger.info(
                        f"Total seats {TOTAL_SEATS} left. Total tickets {TOTAL_TICKETS} left."
                    )
                if TOTAL_SEATS <= 5:
                    break

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info("Seller started work")

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f"{self.name} sold one;  {TOTAL_TICKETS} left")
        logger.info(f"Seller {self.name} sold {self.tickets_sold} tickets")

    def random_sleep(self) -> None:
        time.sleep(random.randint(1, 2))


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    sellers: List[Seller] = []

    for _ in range(3):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)
    director = Director(semaphore)
    director.start()
    sellers.append(director)
    for seller in sellers:
        seller.join()


if __name__ == "__main__":
    main()
