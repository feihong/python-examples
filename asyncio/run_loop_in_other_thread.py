import time
import threading
import asyncio


def run_event_loop():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_main())


async def loop_main():
    global stop_event
    stop_event = asyncio.Event()

    print('Event loop is running inside: ' + threading.current_thread().name)
    for i in range(10):
        print(i)
        asyncio.sleep(0.1)

    await stop_event.wait()


if __name__ == '__main__':
    loop = None
    stop_event = None

    thread = threading.Thread(target=run_event_loop)
    thread.start()
    print('Sleep...')
    time.sleep(3)
    print('Awoke')

    # Set the stop event to make the loop coroutine stop blocking.
    loop.call_soon_threadsafe(stop_event.set)

    thread.join()
