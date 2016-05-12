"""
This web app can start one of two tasks with a different numerical argument.
While a given task is running, it sends messages to all active websockets.

"""

import sys
import time
import asyncio
from pathlib import Path
from aiohttp import web
from mako.template import Template


def get_function_pairs(names):
    project_root = Path(__file__).absolute().parents[2]
    sys.path.append(str(project_root))
    import generate

    for name in names:
        fn = convert_to_async_function(getattr(generate, name))
        yield name, fn


def convert_to_async_function(fn):
    """
    Accept a generator function and turn it into an async function.

    """
    # Add a 1 second delay before each step to simulate long-running task.
    def slow_fn(n):
        for v in fn(n):
            time.sleep(1.0)
            yield v

    async def async_fn(n, logger):
        generator = slow_fn(n)
        while True:
            try:
                value = await asyncio.get_event_loop().run_in_executor(
                    None, next, generator)
                logger.info(value)
            except StopIteration:
                break

    return async_fn


FUNCTIONS = dict(get_function_pairs([
    'generate_chinese_characters', 'generate_emoticons'
]))


async def index(request):
    with (Path(__file__).parent / 'index.html').open() as fp:
        html = Template(fp.read()).render(
            function_names=FUNCTIONS.keys())
        return web.Response(text=html, content_type='text/html')


async def start_task(request):
    app = request.app
    logger = app['logger']

    # Only run one task at a time.
    if app['current_task'] and not app['current_task'].done():
        return web.Response(text='task not started')

    name = request.GET['name']
    count = int(request.GET['count'])
    fn = FUNCTIONS[name]

    app['current_task'] = asyncio.ensure_future(fn(count, logger))
    app['current_task_name'] = name
    app['logger'].info('Started task: %s' % name)
    app['current_task'].add_done_callback(
        lambda f: logger.info('Task %s completed' % name))
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
