import random
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
        self.write(response.body)


class GenerateCharactersHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        result = []
        count = random.randint(2, 6)
        print('Preparing to generate %d characters' % count)
        for i in range(count):
            c = chr(random.randint(0x4e00, 0x9fff))
            print('Generated:', c)
            result.append(c)
            yield gen.sleep(1)
        self.write(', '.join(result))


if __name__ == '__main__':
    settings = dict(
        static_path=str(Path(__file__).parent.absolute())
    )
    app = Application([
        (r'/', MainHandler),
        (r'/ip/', IpAddressHandler),
        (r'/generate/', GenerateCharactersHandler),
    ], **settings)
    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
