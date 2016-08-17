import unittest
from tornado.testing import AsyncHTTPTestCase

import app


class TestHelloApp(AsyncHTTPTestCase):
    def get_app(self):
        return app.app

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'Hello World')


if __name__ == '__main__':
    unittest.main()
