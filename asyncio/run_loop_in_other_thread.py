import time
import threading
import asyncio


def run_event_loop(loop, stop_event):
    loop.run_until_complete(loop_main(stop_event))


async def loop_main(stop_event):
    for i in range(10):
        print(i)
        asyncio.sleep(0.1)

    await stop_event.wait()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    stop_event = asyncio.Event()

    thread = threading.Thread(target=run_event_loop, args=[loop, stop_event])
    thread.start()
    print('Sleep...')
    time.sleep(3)
    print('Awoke')
    loop.call_soon_threadsafe(stop_event.set)
    thread.join()
