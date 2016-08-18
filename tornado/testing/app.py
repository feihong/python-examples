from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler


def get_app():
    return Application([
        (r'/', MainHandler),
        (r'/websocket/', MyWSHandler),
    ])


INDEX_HTML = """
<h1>Hello World</h1>

<input value='monkey'>
<button>Send</button>

<script src='http://code.jquery.com/jquery-3.1.0.slim.min.js'></script>
<script>
var ws = new WebSocket('ws://' + window.location.host + '/websocket/')
ws.onmessage = function(evt) {
  console.log('Received: ' + evt.data)
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


class MainHandler(RequestHandler):
    def get(self):
        self.write(INDEX_HTML)


class MyWSHandler(WebSocketHandler):
    def on_message(self, message):
        "Echo the message back in upper case"
        self.write_message(message.upper())


if __name__ == '__main__':
    app = get_app()
    app.listen(8000)
    loop = IOLoop.current()
    loop.start()
