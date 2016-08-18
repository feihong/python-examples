import tornado.testing
from tornado.websocket import websocket_connect

import app


class TestHelloApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.get_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertIn(b'Hello World', response.body)

    @tornado.testing.gen_test
    def test_websocket(self):
        url = 'ws://localhost:%s/websocket/' % self.get_http_port()
        conn = yield websocket_connect(url)
        conn.write_message('hoo BOY 888 yeah DuDe')
        msg = yield conn.read_message()
        self.assertEqual(msg, 'HOO BOY 888 YEAH DUDE')


if __name__ == '__main__':
    import unittest
    unittest.main()
    # tornado.testing.main()
