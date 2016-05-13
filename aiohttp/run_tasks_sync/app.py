"""
This web app can start one of two tasks with a different numerical argument.
While a given task is running, it sends messages to all active websockets.

"""

import sys
import asyncio
import functools
import threading
from pathlib import Path
from aiohttp import web


class GeneratorTask:
    def __init__(self, name):
        self.name = name
        self.stop_event = threading.Event()

    def cancel(self):
        self.stop_event.set()

    def done(self):
        return self.stop_event.is_set()

    def start(self):
        loop = asyncio.get_event_loop()
        coroutine = loop.run_in_executor(None, self._stoppable_run)
        self.task = asyncio.ensure_future(coroutine)

    def run(self):
        """
        Override with generator method.

        """
        raise NotImplemented

    def add_done_callback(self, callback):
        self.task.add_done_callback(callback)

    def _stoppable_run(self):
        for value in self.run():
            if self.stop_event.is_set():
                break
        self.stop_event.set()


class AwesomeTask(GeneratorTask):
    def __init__(self, name, count, logger):
        super(AwesomeTask, self).__init__(name)
        self.count = count
        loop = asyncio.get_event_loop()
        self.log = functools.partial(loop.call_soon_threadsafe, logger.info)

    def run(self):
        import random
        import time
        for i in range(65, 65 + self.count):
            c = chr(i)
            self.log(c * random.randint(10, 50))
            time.sleep(1)
            yield


async def index(request):
    with (Path(__file__).parent / 'index.html').open() as fp:
        return web.Response(text=fp.read(), content_type='text/html')


async def start_task(request):
    app = request.app
    logger = app['logger']

    # Only run one task at a time.
    if app['current_task'] and not app['current_task'].done():
        return web.Response(text='task not started')

    count = int(request.GET['count'])
    task = AwesomeTask('AwesomeTask', count, logger)
    task.start()

    app['current_task'] = task
    app['logger'].info('Started task: %s' % task.name)

    def done(*args):
        logger.info('Task %s completed' % task.name)
        app['current_task'] = None
    app['current_task'].add_done_callback(done)
    return web.Response(text='task started')


async def stop_task(request):
    app = request.app
    task = app['current_task']
    if task and not task.done():
        app['logger'].info('Cancelling task %s...' % task.name)
        task.cancel()
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
