import asyncio
import time


async def _factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f


async def _main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        _factorial("A", 2),
        _factorial("B", 3),
        _factorial("C", 4),
    )
    print(L)


def run():
    asyncio.run(_main())


class WordFinderAA(object):
    TOTAL_PAGES = 2
    WordChunks = [set() for _ in range(TOTAL_PAGES)]
    WordsList = [['taxon', 'taxonomy', 'taxonomic'], ['apple', 'taxonomically', 'taxonomies']]

    def __init__(self):
        self.WordChunks = [set() for _ in range(self.TOTAL_PAGES)]
        p = 0
        for sp in self.WordsList:
            self.WordChunks[p] = set(sp)
            p += 1

    async def say_after(self, delay, what):
        await asyncio.sleep(delay)
        print(what)

    async def find_ver_3(self) -> list[str]:
        answer = []
        print(f"started at {time.strftime('%X')}")
        task1 = asyncio.create_task(self.say_after(2, self.WordChunks[0].pop()))
        task2 = asyncio.create_task(self.say_after(2, self.WordChunks[1].pop()))
        await task1
        await task2
        print(f"finished at {time.strftime('%X')}")
        return answer

