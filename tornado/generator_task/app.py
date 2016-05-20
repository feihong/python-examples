import random
import time
import functools
from pathlib import Path
import threading
import json
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado import gen
from tornado.websocket import WebSocketHandler


executor = ThreadPoolExecutor()


class GeneratorTask:
    def __init__(self):
        self.stop_event = threading.Event()
        self.future = None

    def cancel(self):
        self.stop_event.set()

    def done(self):
        return self.stop_event.is_set()

    def start(self):
        """
        Unlike asyncio's run_in_executor(), submit() does not raise an exception
        when the function it tries errors out.

        """
        self.future = executor.submit(self._stoppable_run)
        self.add_done_callback(self._done_callback)

    def run(self):
        """
        Override with generator method.

        """
        raise NotImplemented

    def add_done_callback(self, callback):
        if self.future:
            self.future.add_done_callback(callback)

    def _stoppable_run(self):
        for _ in self.run():
            if self.stop_event.is_set():
                break
        self.stop_event.set()

    def _done_callback(self, future):
        # If there was an exception inside of self._stoppable_run, then it won't
        # be raised until you call future.result().
        try:
            future.result()
        except Exception as ex:
            self.log('Error: %s' % ex)


class GenerateCharactersTask(GeneratorTask):
    def __init__(self, count, logger):
        super(GenerateCharactersTask, self).__init__()
        self.count = count
        loop = IOLoop.current()
        self.log = functools.partial(loop.add_callback, logger.info)

    def run(self):
        self.log('Preparing to generate %d characters' % self.count)

        for i in range(self.count):
            c = chr(random.randint(0x4e00, 0x9fff))
            self.log(c)
            self.log(dict(type='progress', current=i+1, total=self.count))
            time.sleep(1)
            yield

        self.log('Finished generating characters')


class MainHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class StartHandler(RequestHandler):
    def get(self):
        count = int(self.get_query_argument('count', 5))
        app = self.application
        if not app.current_task:
            app.current_task = GenerateCharactersTask(count, app.logger)
            app.current_task.start()
            self.write('Started background task')
            # Set app.current_task to None when task finishes.
            def done_callback(future):
                app.current_task = None
            app.current_task.add_done_callback(done_callback)


class StopHandler(RequestHandler):
    def get(self):
        app = self.application
        if app.current_task:
            app.current_task.cancel()
            self.write('Stopping background task...')
            app.logger.info('Stopping background task...')


class StatusHandler(WebSocketHandler):
    def open(self):
        print('WebSocket opened')
        self.application.sockets.add(self)

    def on_close(self):
        print('WebSocket closed')
        self.application.sockets.remove(self)


class Logger:
    def __init__(self, sockets):
        self.sockets = sockets

    def info(self, obj):
        print(obj)
        if isinstance(obj, str):
            obj = dict(type='message', value=obj)
        data = json.dumps(obj)
        for socket in self.sockets:
            socket.write_message(data)


class NoCacheStaticFileHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            path=str(Path(__file__).parent.absolute()),
            default_filename='index.html',
        )
        super(NoCacheStaticFileHandler, self).__init__(*args, **kwargs)

    def set_extra_headers(self, path):
        self.set_header('Cache-control', 'no-cache')


if __name__ == '__main__':
    settings = dict(
        debug=True,
        autoreload=True,
    )
    app = Application([
        (r'/start/', StartHandler),
        (r'/stop/', StopHandler),
        (r'/websocket/', StatusHandler),
        (r'/(.*)', NoCacheStaticFileHandler),
    ], **settings)
    app.sockets = set()
    app.current_task = None
    app.logger = Logger(app.sockets)

    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
