"""
This web app can start one of a few tasks with a different numerical argument.
While a given task is running, it sends messages to all active websockets.

"""

import asyncio
from pathlib import Path
from aiohttp import web


async def index(request):
    with (Path(__file__).parent / 'index.html').open() as fp:
        return web.Response(text=fp.read(), content_type='text/html')


async def start_task(request):
    name = request.GET['name']
    count = int(request.GET['count'])
    fn = dict(
        random=generate_random_numbers,
        uuid=generate_uuids,
    )[name]
    app = request.app
    coroutine = fn(app['logger'], count)
    app['current_operation'] = asyncio.ensure_future(coroutine)
    return web.Response(text='ok')


async def status(request):
    print('Websocket connection opened')
    resp = web.WebSocketResponse()
    await resp.prepare(request)
    request.app['sockets'].add(resp)
    async for msg in resp: pass
    await resp.close()
    print('Websocket connection closed')
    request.app['sockets'].remove(resp)
    return resp


async def generate_random_numbers(logger, n):
    import random
    for i in range(n):
        await asyncio.sleep(1.0)
        value = random.randint(1, 100)
        logger.info(str(value))


async def generate_uuids(logger, n):
    import uuid
    for i in range(n):
        await asyncio.sleep(1.0)
        value = uuid.uuid4()
        logger.info(str(value))


class Logger:
    def __init__(self, sockets):
        self.sockets = sockets

    def info(self, value):
        print('Logging: %s' % value)
        for ws in self.sockets:
            ws.send_str(value)


def main():
    app = web.Application()
    app['sockets'] = set()
    app['logger'] = Logger(app['sockets'])
    app['current_operation'] = None
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/start-task/', start_task)
    app.router.add_route('GET', '/status/', status)
    app.router.add_static('/static/', Path(__file__).parent)
    web.run_app(app)


if __name__ == '__main__':
    main()
