from configparser import ConfigParser
import urllib.request
import dateutil.parser
import json
import os
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import pytz
import csv
import xml.etree.ElementTree as ET

parser = ConfigParser()
parser.read('../slowburn.config', encoding='utf-8')
darksky_key = parser.get('darksky', 'key')

gps_logs_directory = '../gps_logs/'

tf = TimezoneFinder()


def write_weather_to_csv_file(logs_directory):
    all_gps_files = os.listdir(logs_directory)

    with open('running.csv', 'w') as csv_file:

        file_writer = csv.writer(csv_file, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow(['Date', 'Summary', 'Temperature', 'Humidity', 'Wind', 'Filename'])

        for gps_file in all_gps_files:

            # Ignore any file that isn't a GPS format
            is_gps_file = False

            if ".tcx" in gps_file or "*.gpx" in gps_file:
                is_gps_file = True

            if not is_gps_file:
                continue

            weather = GetWeather(logs_directory + gps_file)
            date = convert_to_local_time(weather.utc_run_time(), weather.local_timezone())

            file_writer.writerow([date, weather.weather_type('icon'), weather.weather_type('temperature'),
                                  weather.weather_type('humidity'), weather.weather_type('windSpeed'), gps_file])


def convert_time_to_unix(time):
    parsed_time = dateutil.parser.parse(time)
    time_in_unix = parsed_time.strftime('%s')
    return time_in_unix


def convert_to_local_time(utc_time, run_timezone):
    """Convert run time from stored UTC time to the local timezone at the latitude/longitude of the run."""
    gps_utc_time = datetime.utcfromtimestamp(float(convert_time_to_unix(utc_time)))
    localized_utc_time = pytz.utc.localize(gps_utc_time)
    local_timezone = pytz.timezone(run_timezone)
    utc_to_local_time = localized_utc_time.astimezone(local_timezone)

    return utc_to_local_time


def convert_to_local_timezone(latitude, longitude):
    return tf.timezone_at(lat=latitude, lng=longitude)


class ReadGPS:
    def __init__(self, gps_file):
        self.gps_file = gps_file
        self.data = ET.parse(gps_file)
        self.root = self.data.getroot()

    def start_time(self):
        """Returns start time of run"""

        for element in self.root.iter():
            if "}Id" in element.tag:
                return element.text

    def total_time(self):
        """Returns total time of run in seconds"""

        for element in self.root.iter():
            if "TotalTimeSeconds" in element.tag:
                return element.text

    def total_distance(self):
        """Returns total distance run in meters"""

        for element in self.root.iter():
            if "DistanceMeters" in element.tag:
                return element.text

    def latitude(self):

        for element in self.root.iter():
            if "LatitudeDegrees" in element.tag:
                return element.text

    def longitude(self):

        for element in self.root.iter():
            if "LongitudeDegrees" in element.tag:
                return element.text

class GetWeather:
    def __init__(self, gps_file):
        self.gps = ReadGPS(gps_file)
        self.run_time = self.gps.start_time()

        self.latitude = self.gps.latitude()
        self.longitude = self.gps.longitude()

        print("Getting Darksky weather for " + str(gps_file) + " ...")
        self.darksky_json = self.darksky_api_request(self.run_time)

    def darksky_api_request(self, run_time):
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

    def local_timezone(self):
        return self.darksky_json['timezone']

    def utc_run_time(self):
        return self.run_time


if __name__ == '__main__':
    gps = ReadGPS("../gps_logs/2017-06-15_Running.tcx")
    print(gps.start_time())
    print(gps.total_time())
    print(gps.total_distance())
    print(gps.latitude())
    print(gps.longitude())

    weather = GetWeather("../gps_logs/2017-06-15_Running.tcx")
    print(weather.weather_type('temperature'))
