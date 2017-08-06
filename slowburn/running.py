import tcxparser
from configparser import ConfigParser
import urllib.request
import dateutil.parser
import json

# Darksky weather API
# Create config file manually
parser = ConfigParser()
parser.read('slowburn.config', encoding='utf-8')
darksky_key = parser.get('darksky', 'key')

tcx = tcxparser.TCXParser('gps_logs/2017-06-15_Running.tcx')
run_time = tcx.completed_at


def convert_time_to_unix(time):
    parsed_time = dateutil.parser.parse(time)
    time_in_unix = parsed_time.strftime('%s')
    return time_in_unix


class GetWeather:
    def __init__(self, run_time):
        self.run_time = run_time

    def darksky_api_request(self):
        unix_run_time = convert_time_to_unix(self.run_time)
        darksky_request = urllib.request.urlopen(
            "https://api.darksky.net/forecast/" + darksky_key + "/" + str(tcx.latitude) + "," + str(
                tcx.longitude) + "," + unix_run_time + "?exclude=currently,flags").read()
        return (darksky_request)

    def all_temperatures(self):
        """Get all hourly temperatures for the day"""

        darksky_json = json.loads(self.darksky_api_request().decode('utf-8'))
        temperatures = {}
        for weather in darksky_json['hourly']['data']:
            temperatures[weather['time']] = weather['temperature']
        return temperatures

    def temperature(self):
        """Get temperature at the hour of run completion."""

        hours = []
        unix_run_time = convert_time_to_unix(self.run_time)
        for time, temperature in self.all_temperatures().items():
            hours.append(((abs(time - int(unix_run_time))), temperature))

        temperature = (min(hours, key=lambda time_delta: time_delta[0]))[1]
        return temperature


weather = GetWeather(run_time)
weather.temperature()
