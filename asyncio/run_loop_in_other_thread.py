import threading
import asyncio


def run_event_loop():
    loop.run_until_complete(count(10))


async def count(n):
    for i in range(n):
        print(i)
        asyncio.sleep(0.1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    thread = threading.Thread(target=run_event_loop)
    thread.start()

    thread.join()
