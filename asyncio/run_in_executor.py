import asyncio


def func(delay):
    import time

    print('Before sleeping...')
    time.sleep(delay)
    print('After sleeping...')


async def main():
    def done_callback(future):
        print(future)
        print('done!')

    future = loop.run_in_executor(None, func, 3)
    future.add_done_callback(done_callback)

    await asyncio.sleep(0.01)
    # future.cancel()    # will not stop execution of the already-running function

    print(future)
    await future
    print('end of main')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
