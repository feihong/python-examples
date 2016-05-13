import time
import asyncio


COUNT = 5


def synchronous_function():
    for i in range(COUNT):
        print(i)
        time.sleep(1)


def synchronous_generator_function():
    for i in range(65, 65 + COUNT):
        yield chr(i)
        time.sleep(1)


async def func1():
    await loop.run_in_executor(None, synchronous_function)


async def func2():
    def generator_function_wrapper(fn):
        for v in fn():
            loop.call_soon_threadsafe(lambda: print(v + ' in bed!'))

    await loop.run_in_executor(None, generator_function_wrapper, synchronous_generator_function)


async def main():
    await asyncio.wait([func1(), func2()])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
