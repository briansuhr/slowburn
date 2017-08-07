import unittest
import context

from slowburn.running import convert_time_to_unix


class MyTest(unittest.TestCase):
    def test_convert_time_to_unix(self):
        self.assertEqual(convert_time_to_unix("2017-06-15T19:01:17.000Z"), '1497553277')


if __name__ == '__main__':
    unittest.main()
