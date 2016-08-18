import tornado.gen
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler


def get_app():
    return Application([
        (r'/', IndexHandler),
        (r'/slow/', SlowHandler),
        (r'/websocket/', MyWSHandler),
    ], debug=True)


INDEX_HTML = """
<h1>Hello World</h1>

<input value='monkey'>
<button>Send</button>
<p></p>

<script src='http://code.jquery.com/jquery-3.1.0.slim.min.js'></script>
<script>
var ws = new WebSocket('ws://' + window.location.host + '/websocket/')
ws.onmessage = function(evt) {
  $('p').text('Received: ' + evt.data)
}
function sendInput() {
  ws.send($('input').val())
}
$('input').on('keypress', function(evt) {
  if (evt.keyCode === 13) {
    sendInput()
  }
})
$('button').on('click', sendInput)
</script>
"""


class IndexHandler(RequestHandler):
    def get(self):
        self.write(INDEX_HTML)


class SlowHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.sleep(3)
        self.write('Sorry for being so slow...')


class MyWSHandler(WebSocketHandler):
    def on_message(self, message):
        "Echo the message back in upper case"
        self.write_message(message.upper())


if __name__ == '__main__':
    app = get_app()
    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
