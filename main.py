import random
import time
from threading import Thread


def launch_rocket(delay, countdown):
    time.sleep(delay)
    for i in reversed(range(countdown)):
        print(f"{i + 1}...")
        time.sleep(1)
    print("Rocket was launched")


def rockets_args(n):
    while n > 0:
        yield (random.random() * 5, random.randrange(5))
        n -= 1


def run_threads():
    threads = [Thread(target=launch_rocket, args=(d, c)) for d, c in rockets_args(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    run_threads()
