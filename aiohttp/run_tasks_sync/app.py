"""
This web app can start one of two tasks with a different numerical argument.
While a given task is running, it sends messages to all active websockets.

"""

import sys
import time
import asyncio
import functools
import threading
from pathlib import Path
from aiohttp import web
from mako.template import Template


class GeneratorTask:
    def __init__(self, name, fn, callback):
        self.name = name
        self.fn = fn
        self.stop_event = threading.Event()
        self.callback = callback

    def cancel(self):
        self.stop_event.set()

    def done(self):
        return self.stop_event.is_set()

    def run(self):
        self.task = asyncio.ensure_future(self._run())

    def add_done_callback(self, callback):
        self.task.add_done_callback(callback)

    async def _run(self):
        loop = asyncio.get_event_loop()
        threadsafe_callback = functools.partial(loop.call_soon_threadsafe, self.callback)

        def wrapper():
            for value in self.fn():
                if self.stop_event.is_set():
                    break
                time.sleep(1)   # to simulate a computation-intensiveness
                threadsafe_callback(value)
            self.stop_event.set()

        await loop.run_in_executor(None, wrapper)


def get_function_pairs(names):
    project_root = Path(__file__).absolute().parents[2]
    sys.path.append(str(project_root))
    import generate

    for name in names:
        yield name, getattr(generate, name)


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
    fn = functools.partial(FUNCTIONS[name], count)
    task = GeneratorTask(name, fn, logger.info)
    task.run()

    app['current_task'] = task
    app['logger'].info('Started task: %s' % task.name)
    app['current_task'].add_done_callback(
        lambda f: logger.info('Task %s completed' % task.name))
    return web.Response(text='task started')


async def stop_task(request):
    app = request.app
    task = app['current_task']
    if task and not task.done():
        task.cancel()
        app['logger'].info('Trying to cancel task %s' % task.name)
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
        resp.send_str('Current running task: %s' % app['current_task'].name)

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
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/start-task/', start_task)
    app.router.add_route('GET', '/stop-task/', stop_task)
    app.router.add_route('GET', '/status/', status)
    app.router.add_static('/static/', Path(__file__).parent)
    web.run_app(app)


if __name__ == '__main__':
    main()
