import asyncio


async def main():
    stop_event = asyncio.Event()
    asyncio.ensure_future(do_stuff(stop_event))
    await stop_event.wait()
    print('Done!')


async def do_stuff(stop_event):
    print('Sleep for a little while')
    await asyncio.sleep(2.5)
    print('Now setting stop event')
    stop_event.set()


asyncio.get_event_loop().run_until_complete(main())
