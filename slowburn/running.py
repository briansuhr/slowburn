import tcxparser
from configparser import ConfigParser
import urllib.request
import dateutil.parser
import json

parser = ConfigParser()
parser.read('../slowburn.config', encoding='utf-8')
darksky_key = parser.get('darksky', 'key')

tcx = tcxparser.TCXParser('../gps_logs/2017-06-15_Running.tcx')
run_time = tcx.completed_at


def convert_time_to_unix(time):
    parsed_time = dateutil.parser.parse(time)
    time_in_unix = parsed_time.strftime('%s')
    return time_in_unix

def darksky_api_request(run_time):
    unix_run_time = convert_time_to_unix(run_time)
    darksky_request = urllib.request.urlopen(
        "https://api.darksky.net/forecast/" + darksky_key + "/" + str(tcx.latitude) + "," + str(
            tcx.longitude) + "," + unix_run_time + "?exclude=currently,flags").read()
    return json.loads(darksky_request.decode('utf-8'))


class GetWeather:
    def __init__(self, run_time):
        self.run_time = run_time

        print("Calling Darksky API...")
        self.darksky_json = darksky_api_request(run_time)

    def all_temperatures(self):
        """Get all hourly temperatures for the day"""

        temperatures = {}
        for weather in self.darksky_json['hourly']['data']:
            temperatures[weather['time']] = weather['temperature']
        return temperatures

    def all_humidity_levels(self):
        humidity = {}
        for humidity_level in self.darksky_json['hourly']['data']:
            humidity[humidity_level['time']] = humidity_level['humidity']
        return humidity

    def temperature(self):
        """Get temperature at the hour of run completion."""

        hours = []
        unix_run_time = convert_time_to_unix(self.run_time)
        for time, temperature in self.all_temperatures().items():
            hours.append(((abs(time - int(unix_run_time))), temperature))

        temperature = (min(hours, key=lambda time_delta: time_delta[0]))[1]
        return temperature


if __name__ == '__main__':

    weather = GetWeather(run_time)
    print(weather.all_temperatures())
    print(weather.temperature())
    print(weather.all_humidity_levels())
