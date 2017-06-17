import tcxparser
from darksky import forecast
from configparser import ConfigParser

# Darksky weather API.
# Create config file manually
parser = ConfigParser()
parser.read('slowburn.config', encoding='utf-8')
darksky_key = parser.get('darksky', 'key')

tcx = tcxparser.TCXParser('gps_logs/2017-06-15_Running.tcx')

print(tcx.duration)
boston = forecast(darksky_key, 42.3601, -71.0589)
print(boston)
