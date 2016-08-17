import tornado.testing

import app


class TestHelloApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.get_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertIn(b'Hello World', response.body)


if __name__ == '__main__':
    import unittest
    unittest.main()
    # tornado.testing.main()
