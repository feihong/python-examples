import random
from pathlib import Path
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado import gen
from tornado.websocket import WebSocketHandler
from tornado.locks import Event


class MainHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class StartHandler(RequestHandler):
    def get(self):
        """
        Note that unlike asyncio.ensure_future(), IOLoop.add_callback() does
        not return an object that allows you cancel the coroutine. That's why
        we pass in an tornado.locks.Event object, which can be used to tell
        the coroutine that it should stop processing.

        """
        count = int(self.get_query_argument('count', 5))
        self.application.stop_event = Event()
        IOLoop.current().add_callback(
            generate_characters,
            count,
            self.application.logger,
            self.application.stop_event)
        self.write('Started background task')


class StopHandler(RequestHandler):
    def get(self):
        if self.application.stop_event:
            self.application.stop_event.set()
            self.write('Stopping background task...')
            self.application.logger.info('Stopping background task...')


class StatusHandler(WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        self.application.sockets.add(self)

    def on_close(self):
        print("WebSocket closed")
        self.application.sockets.remove(self)

    def on_message(self, message):
        pass


@gen.coroutine
def generate_characters(count, logger, stop_event):
    logger.info('Preparing to generate %d characters' % count)

    for i in range(count):
        if stop_event.is_set():
            break
        c = chr(random.randint(0x4e00, 0x9fff))
        logger.info(c)
        yield gen.sleep(1)

    logger.info('Finished generating characters')


class Logger:
    def __init__(self, sockets):
        self.sockets = sockets

    def info(self, text):
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
    app.logger = Logger(app.sockets)
    app.stop_event = None

    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
