import signal
import sys
from threading import Semaphore, Thread
import time

sem: Semaphore = Semaphore()


def fun1():
    while True:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while True:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


def signal_handler(sig, frame):
    print("\nReceived keyboard interrupt, quitting threads.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


t1: Thread = Thread(target=fun1, daemon=True)
t2: Thread = Thread(target=fun2, daemon=True)

try:
    t1.start()
    t2.start()
    t1.join()
    t2.join()

except KeyboardInterrupt:
    print("\nReceived keyboard interrupt, quitting threads.")
    sys.exit(0)
