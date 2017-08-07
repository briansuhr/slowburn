import unittest
import context

from slowburn.running import *

class MyTest(unittest.TestCase):
    def setUp(self):
        self.weather = GetWeather('2017-06-15T19:01:17.000Z')

    def test_convert_time_to_unix(self):
        self.assertEqual(convert_time_to_unix("2017-06-15T19:01:17.000Z"), '1497553277')
        self.assertEqual(convert_time_to_unix("2012-04-01T04:59:22.000Z"), '1333256362')

    def test_get_all_hourly_temperatures_of_day(self):
        self.assertEqual(self.weather.all_temperatures(),
                         {1497513600: 63.97, 1497571200: 92.05, 1497585600: 79.66, 1497531600: 58.57, 1497546000: 74.09,
                          1497517200: 62.94, 1497560400: 89.52, 1497574800: 91.72, 1497589200: 75.92, 1497520800: 61.24,
                          1497535200: 61.09, 1497549600: 78.7, 1497578400: 89.1, 1497564000: 90.43, 1497592800: 72.91,
                          1497510000: 65.52, 1497538800: 64.78, 1497553200: 83.76, 1497524400: 59.58, 1497567600: 91.85,
                          1497582000: 84.73, 1497556800: 86.95, 1497528000: 58.84, 1497542400: 68.9}
                         )

if __name__ == '__main__':
    unittest.main()
