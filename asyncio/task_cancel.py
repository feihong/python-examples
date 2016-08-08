import asyncio


async def main():
    task = asyncio.ensure_future(cool_task())

    # await asyncio.sleep(1)
    # await asyncio.sleep(3)

    task.cancel()


async def cool_task():
    print('Starting the cool task')
    await asyncio.sleep(2)
    print('Middle of the cool task')
    await asyncio.sleep(2)
    print('Cool task finished!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    # Stop the loop after 5 seconds.
    loop.call_later(5, loop.stop)
    loop.run_forever()
