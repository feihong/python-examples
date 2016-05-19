import random
import time
import functools
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
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
        self.future = executor.submit(self._stoppable_run)

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
        print("WebSocket opened")
        self.application.sockets.add(self)

    def on_close(self):
        print("WebSocket closed")
        self.application.sockets.remove(self)


class Logger:
    def __init__(self, sockets):
        self.sockets = sockets

    def info(self, text):
        print(text)
        for socket in self.sockets:
            socket.write_message(text)


if __name__ == '__main__':
    settings = dict(
        static_path=str(Path(__file__).parent.absolute())
    )
    app = Application([
        (r'/', MainHandler),
        (r'/start/', StartHandler),
        (r'/stop/', StopHandler),
        (r'/websocket/', StatusHandler),
    ], **settings)
    app.sockets = set()
    app.current_task = None
    app.logger = Logger(app.sockets)

    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
