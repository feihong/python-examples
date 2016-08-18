"""
To run tests:

python -m unittest

To just run the tests in this module:

python -m unittest test_unittest

"""
import unittest


class TestSomething(unittest.TestCase):
    def test_split(self):
        s = '/a/b/c/'
        self.assertEqual(s.split('/'), ['', 'a', 'b', 'c', ''])


# if __name__ == '__main__':
#     unittest.main()
