import asyncio


def synchronous_function():
    import time
    for i in range(4):
        print(i)
        time.sleep(1.0)
    return 'Hoosier Mama'


async def main():
    message = await loop.run_in_executor(None, synchronous_function)
    print('The secret message is:', message)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
