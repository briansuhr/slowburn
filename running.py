import tcxparser
from configparser import ConfigParser
from datetime import datetime
import urllib.request
import dateutil.parser

t = '1984-06-02T19:05:00.000Z'
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

unix_run_time = convert_time_to_unix(run_time)
darksky_request = urllib.request.urlopen("https://api.darksky.net/forecast/" + darksky_key + "/42.3601,-71.0589," + unix_run_time + "?exclude=currently,flags").read()
print(darksky_request)


class getWeather:
    def __init__(self, date, time):
        self.date = date
        self.time = time

    def goodbye(self, date):
        print("my name is " + date)
