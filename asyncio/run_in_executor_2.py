import time
import asyncio
import threading


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
        interrupted = False
        for v in fn():
            if stopEvent.is_set():
                print('Stopping the generator')
                interrupted = True
                break
            loop.call_soon_threadsafe(lambda: print(v * 8))
        if not interrupted:
            print('Generator completed')

    await loop.run_in_executor(None, generator_function_wrapper, synchronous_generator_function)


async def stop_func2():
    await asyncio.sleep(3)
    stopEvent.set()


async def main():
    await asyncio.wait([func1(), func2(), stop_func2()])


stopEvent = threading.Event()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
