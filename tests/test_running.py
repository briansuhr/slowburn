import unittest
import context

from slowburn.running import convert_time_to_unix


class MyTest(unittest.TestCase):
    def test_convert_time_to_unix(self):
        self.assertEqual(convert_time_to_unix("2017-06-15T19:01:17.000Z"), '1497553277')
        self.assertEqual(convert_time_to_unix("2012-04-01T04:59:22.000Z"), '1333256362')


if __name__ == '__main__':
    unittest.main()
