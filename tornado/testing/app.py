from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler


class MainHandler(RequestHandler):
    def get(self):
        self.write('Hello World')


app = Application([
    (r'/', MainHandler),
])

if __name__ == '__main__':
    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
