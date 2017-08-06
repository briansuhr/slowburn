import unittest
import context

from slowburn.running import GetWeather


class MyTest(unittest.TestCase):
    def setUp(self):
        self.chart_group = []

    def test_sample_test(self):
        self.assertEqual(sample_test(1,2), 3)
        self.assertEqual(sample_test(1,4), 5)


if __name__ == '__main__':
    unittest.main()