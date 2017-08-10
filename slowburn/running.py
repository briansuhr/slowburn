import tcxparser
from configparser import ConfigParser
import urllib.request
import dateutil.parser
import json
import os
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import pytz

parser = ConfigParser()
parser.read('../slowburn.config', encoding='utf-8')
darksky_key = parser.get('darksky', 'key')

gps_logs_directory = '../gps_logs/'

tf = TimezoneFinder()


def read_all_gps_files(gps_logs_directory):
    all_gps_files = os.listdir(gps_logs_directory)
    for gps_file in all_gps_files:
        weather = GetWeather(gps_logs_directory + gps_file)
        print(weather.weather_type('icon'))
        print(weather.weather_type('temperature'))
        print(weather.weather_type('humidity'))
        print(weather.weather_type('windSpeed'))
        print(weather.local_time())


def convert_time_to_unix(time):
    parsed_time = dateutil.parser.parse(time)
    time_in_unix = parsed_time.strftime('%s')
    return time_in_unix


class GetWeather:
    def __init__(self, gps_file):
        self.gps_file = gps_file
        self.tcx = tcxparser.TCXParser(gps_logs_directory + gps_file)
        self.run_time = self.tcx.completed_at

        self.latitude = self.tcx.latitude
        self.longitude = self.tcx.longitude
        self.run_timezone = tf.timezone_at(lat=self.latitude, lng=self.longitude)

        print("Calling Darksky API...")
        self.darksky_json = self.darksky_api_request(self.run_time)

    def darksky_api_request(self, run_time):
        print(run_time)
        darksky_request = urllib.request.urlopen(
            "https://api.darksky.net/forecast/" + darksky_key + "/" + str(self.latitude) + "," + str(
                self.longitude) + "," + convert_time_to_unix(self.run_time) + "?exclude=currently,flags").read()
        return json.loads(darksky_request.decode('utf-8'))

    def filter_weather_type(self, weather_type):
        """Get weather phenomenon data point objects (like temperature, humidity, windSpeed) for each of the 24 hours
        in the day. See https://darksky.net/dev/docs/response for list of available properties."""

        data_points = {}
        for data_point in self.darksky_json['hourly']['data']:
            data_points[data_point['time']] = data_point[weather_type]
        return data_points

    def weather_type(self, weather_type):
        """Get weather type at the hour of run completion."""

        hours = []
        unix_run_time = convert_time_to_unix(self.run_time)
        for time, temperature in self.filter_weather_type(weather_type).items():
            hours.append(((abs(time - int(unix_run_time))), temperature))

        # Filter weather type to hour nearest the run completion time.
        filtered_weather_type = (min(hours, key=lambda time_delta: time_delta[0]))[1]
        return filtered_weather_type

    def local_time(self):
        """Convert run time from stored UTC time to the local timezone at the latitude/longitude of the run."""
        utc_time = datetime.utcfromtimestamp(float(convert_time_to_unix(self.run_time)))
        localized_utc_time = pytz.utc.localize(utc_time)
        local_timezone = pytz.timezone(self.run_timezone)
        utc_to_local_time = localized_utc_time.astimezone(local_timezone)

        return utc_to_local_time


if __name__ == '__main__':
    read_all_gps_files(gps_logs_directory)
