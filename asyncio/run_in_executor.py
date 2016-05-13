import time
import asyncio


COUNT = 5


def synchronous_function():
    for i in range(COUNT):
        print(i)
        time.sleep(1)
    return 'Hoosier Mama'


def synchronous_generator_function():
    for i in range(65, 65 + COUNT):
        yield chr(i)
        time.sleep(1)
        

async def func1():
    message = await loop.run_in_executor(None, synchronous_function)
    print('The secret message is:', message)


async def func2():
    generator = synchronous_generator_function()
    while True:
        try:
            value = await loop.run_in_executor(None, lambda: next(generator))
            print(value)
        except StopIteration:
            break


async def main():
    await asyncio.wait([func1(), func2()])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
