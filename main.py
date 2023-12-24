import heapq
import random
import sys
import time
from enum import Enum, auto
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


def run_threads(rockets):
    try:
        threads = [Thread(target=launch_rocket, args=(d, c)) for d, c in rockets]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    except Exception as e:
        # with 4500+ threads I have "can't start new thread" error
        print(e, file=sys.stderr)


class State(Enum):
    WAITING = auto()
    COUNTING = auto()
    LAUNCHING = auto()


class Op(Enum):
    WAIT = auto()
    STOP = auto()


class Launch:
    def __init__(self, delay, countdown):
        self._state = State.WAITING
        self._delay = delay
        self._countdown = countdown

    def step(self):
        if self._state is State.WAITING:
            self._state = State.COUNTING
            return Op.WAIT, self._delay
        if self._state is State.COUNTING:
            if self._countdown == 0:
                self._state = State.LAUNCHING
            else:
                print(f"{self._countdown}...")
                self._countdown -= 1
                return Op.WAIT, 1
        if self._state is State.LAUNCHING:
            print("Rocket launched!")
            return Op.STOP, None

        assert False, self._state


def now():
    return time.time()


def run_fsm(rockets):
    start = now()
    # priority queue, where we prioritize by (1 - when to step), (2 - by id if step_at isn't unique)
    work = [
        (start, i, Launch(d, c)) for i, (d, c) in enumerate(rockets)
    ]  # we don't need to heapify it, because it's already sorted at the beginning

    while work:
        step_at, id, launch = heapq.heappop(
            work,
        )
        # when we have reached a point where there's nothing to run step for, we need to wait (because of heapq it will always be the smallest time from the queue)
        # note: on the first cycle will always be < 0
        wait = step_at - now()
        if wait > 0:
            time.sleep(wait)

        op, arg = launch.step()
        if op is Op.WAIT:
            step_at = now() + arg
            # push it back into the heapq with a new step_at based on the time it needs to wait
            heapq.heappush(work, (step_at, id, launch))
        else:
            assert op is Op.STOP, op


if __name__ == "__main__":
    rockets = list(rockets_args(100))
    if sys.argv[1] == "threads":
        run_threads(rockets)
    else:
        assert sys.argv[1] == "fsm"
        run_fsm(rockets)
