import unittest
import context

from slowburn.running import *


class MyTest(unittest.TestCase):
    # Limit API calls by using setUP only once
    class_is_set_up = False

    def setUp(self):
        if not self.class_is_set_up:
            print("Initializing Darksky API call...")
            self.setupClass()
            self.__class__.class_is_set_up = True

    def setupClass(self):
        unittest.TestCase.setUp(self)
        self.__class__.weather = GetWeather('../gps_logs/2017-06-15_Running.tcx')

    def test_convert_time_to_unix(self):
        self.assertEqual(convert_time_to_unix("2017-06-15T19:01:17.000Z"), '1497553277')
        self.assertEqual(convert_time_to_unix("2012-04-01T04:59:22.000Z"), '1333256362')

    def test_get_data_point_object_gets_24_hour_temperatures(self):
        self.assertEqual(self.weather.filter_weather_type('temperature'),
                         {1497513600: 63.97, 1497571200: 92.05, 1497585600: 79.66, 1497531600: 58.57, 1497546000: 74.09,
                          1497517200: 62.94, 1497560400: 89.52, 1497574800: 91.72, 1497589200: 75.92, 1497520800: 61.24,
                          1497535200: 61.09, 1497549600: 78.7, 1497578400: 89.1, 1497564000: 90.43, 1497592800: 72.91,
                          1497510000: 65.52, 1497538800: 64.78, 1497553200: 83.76, 1497524400: 59.58, 1497567600: 91.85,
                          1497582000: 84.73, 1497556800: 86.95, 1497528000: 58.84, 1497542400: 68.9}
                         )

    def test_weather_type_at_start_of_run(self):
        self.assertEqual(self.weather.weather_type('icon'), 'clear-day')
        self.assertEqual(self.weather.weather_type('temperature'), 78.7)
        self.assertEqual(self.weather.weather_type('humidity'), 0.37)
        self.assertEqual(self.weather.weather_type('windSpeed'), 6.82)

    def test_convert_to_local_time_converts_utc_to_local_timezone(self):
        self.assertEqual(str(convert_to_local_time(self.weather.utc_run_time(), self.weather.local_timezone())),
                         '2017-06-15 11:11:02-07:00')


if __name__ == '__main__':
    unittest.main()
