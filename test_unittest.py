"""
To run tests:

python -m unittest

To just run the tests in this module:

python -m unittest test_unittest

"""
import unittest
from unittest.mock import Mock, patch

import generate


class TestSomething(unittest.TestCase):
    def test_split(self):
        s = '/a/b/c/'
        self.assertEqual(s.split('/'), ['', 'a', 'b', 'c', ''])

    @patch('generate.urlopen')
    def test_generate_chinese_characters(self, urlopen):
        # Mock the following expression: urlopen(url).read().decode('utf-8')
        test_str = '爱若有光明 为何我的心中一片黑暗'
        urlopen.return_value = Mock(**{
            'read.return_value': Mock(**{
                'decode.return_value': test_str
            })
        })

        lst = generate.generate_chinese_characters(8)
        lst = list(lst)
        # Make sure only 8 characters were produced.
        self.assertEqual(len(lst), 8)

        # Make sure all characters are from test string.
        for x in lst:
            self.assertIn(x, test_str)



# if __name__ == '__main__':
#     unittest.main()
