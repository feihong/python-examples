from pathlib import Path
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado import gen
from tornado.httpclient import AsyncHTTPClient


class MainHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class IpAddressHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        client = AsyncHTTPClient()
        response = yield client.fetch('http://ipecho.net/plain')
        yield gen.sleep(1)
        self.write(response.body)


if __name__ == '__main__':
    settings = dict(
        static_path=str(Path(__file__).parent.absolute())
    )
    app = Application([
        (r'/', MainHandler),
        (r'/ip/', IpAddressHandler),
    ], **settings)
    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
