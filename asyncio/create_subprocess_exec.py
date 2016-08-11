import asyncio


async def count_to_n(n):
    for i in range(1, n+1):
        await asyncio.sleep(1)
        print(i)
    loop.stop()

loop = asyncio.get_event_loop()
asyncio.ensure_future(count_to_n(8))
loop.run_forever()
