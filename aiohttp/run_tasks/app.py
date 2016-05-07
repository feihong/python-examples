"""
This web app can start one of two tasks with a different numerical argument.
While a given task is running, it sends messages to all active websockets.

"""

import asyncio
from pathlib import Path
from aiohttp import web


async def index(request):
    with (Path(__file__).parent / 'index.html').open() as fp:
        return web.Response(text=fp.read(), content_type='text/html')


async def start_task(request):
    app = request.app
    # Only run one task at a time.
    if app['current_task'] and not app['current_task'].done():
        return web.Response(text='task not started')
    name = request.GET['name']
    count = int(request.GET['count'])
    fn = dict(
        random=generate_random_numbers,
        uuid=generate_uuids,
    )[name]
    coroutine = fn(app['logger'], count)
    app['current_task'] = asyncio.ensure_future(coroutine)
    app['current_task_name'] = fn.__name__
    app['logger'].info('Started task: %s' % fn.__name__)
    app['current_task'].add_done_callback(
        lambda f: app['logger'].info('Task %s completed' % app['current_task_name']))
    return web.Response(text='task started')


async def stop_task(request):
    app = request.app
    current_task = app['current_task']
    if current_task and not current_task.done():
        current_task.cancel()
        app['logger'].info('Task was cancelled')
        return web.Response(text='task cancelled')
    else:
        return web.Response(text='task not cancelled')


async def status(request):
    print('Websocket connection opened')
    resp = web.WebSocketResponse()
    await resp.prepare(request)

    app = request.app
    app['sockets'].add(resp)

    if app['current_task'] and not app['current_task'].done():
        resp.send_str('Current running task: %s' % app['current_task_name'])

    async for msg in resp: pass
    await resp.close()
    print('Websocket connection closed')
    app['sockets'].remove(resp)
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
    app['current_task'] = None
    app['current_task_name'] = None
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/start-task/', start_task)
    app.router.add_route('GET', '/stop-task/', stop_task)
    app.router.add_route('GET', '/status/', status)
    app.router.add_static('/static/', Path(__file__).parent)
    web.run_app(app)


if __name__ == '__main__':
    main()
