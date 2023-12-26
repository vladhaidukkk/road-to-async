import heapq
import random
import time
import types
from enum import Enum, auto


@types.coroutine
def sleep(secs):
    yield Op.WAIT, secs


async def launch_rocket(delay, countdown):
    await sleep(delay)
    for i in reversed(range(countdown)):
        print(f"{i + 1}...")
        await sleep(1)
    print("Rocket was launched")


def rockets_args(n):
    while n > 0:
        yield (random.random() * 5, random.randrange(5))
        n -= 1


class Op(Enum):
    WAIT = auto()


def now():
    return time.time()


def run_fsm(rockets):
    start = now()
    work = [(start, i, launch_rocket(d, c)) for i, (d, c) in enumerate(rockets)]

    while work:
        step_at, id, launch = heapq.heappop(
            work,
        )
        wait = step_at - now()
        if wait > 0:
            time.sleep(wait)

        try:
            op, arg = launch.send(None)
        except StopIteration:
            continue

        if op is Op.WAIT:
            step_at = now() + arg
            heapq.heappush(work, (step_at, id, launch))
        else:
            assert False, op


if __name__ == "__main__":
    rockets = list(rockets_args(10_000))
    run_fsm(rockets)
