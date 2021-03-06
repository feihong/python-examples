import tornado.testing
from tornado.websocket import websocket_connect

import app


class TestMyApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.get_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertIn(b'Hello World', response.body)

    def test_slow_page(self):
        self.http_client.fetch(self.get_url('/slow/'), self.stop)
        # Set this value to 3 or less to cause the test to fail.
        timeout = 3.1
        response = self.wait(timeout=timeout)
        self.assertEqual(response.code, 200)
        self.assertIn(b'Sorry for being so slow', response.body)

    @tornado.testing.gen_test
    def test_websocket(self):
        url = 'ws://localhost:%s/websocket/' % self.get_http_port()
        conn = yield websocket_connect(url)
        conn.write_message('hoo BOY 888')
        msg = yield conn.read_message()
        self.assertEqual(msg, 'HOO BOY 888')

        conn.write_message('YeAh DuDe 蟒蛇')
        msg = yield conn.read_message()
        self.assertEqual(msg, 'YEAH DUDE 蟒蛇')


if __name__ == '__main__':
    import unittest
    unittest.main()
    # tornado.testing.main()
