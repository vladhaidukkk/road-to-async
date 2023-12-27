import asyncio
import random


async def launch_rocket(delay, countdown):
    await asyncio.sleep(delay)
    for i in reversed(range(countdown)):
        print(f"{i + 1}...")
        await asyncio.sleep(1)
    print("Rocket was launched")


def rockets_args(n):
    while n > 0:
        yield (random.random() * 5, random.randrange(5))
        n -= 1


async def run_rockets(rockets):
    coroutines = [launch_rocket(d, c) for d, c in rockets]
    await asyncio.gather(*coroutines)


if __name__ == "__main__":
    rockets = list(rockets_args(10_000))
    asyncio.run(run_rockets(rockets))
