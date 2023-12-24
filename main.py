import random
import time


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


if __name__ == "__main__":
    for d, c in rockets_args(100):
        launch_rocket(d, c)
