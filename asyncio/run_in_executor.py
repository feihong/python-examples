import asyncio


COUNT = 5


def synchronous_function():
    import time
    for i in range(COUNT):
        print(i)
        time.sleep(1)
    return 'Hoosier Mama'


async def func1():
    message = await loop.run_in_executor(None, synchronous_function)
    print('The secret message is:', message)


async def func2():
    for i in range(65, 65 + COUNT):
        print(chr(i))
        await asyncio.sleep(1)


async def main():
    await asyncio.wait([func1(), func2()])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
