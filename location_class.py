#!/home/mike/Documents/python_envs/location_information_inputs/bin/python3
import requests
import sys

url = "https://api.openweathermap.org/data/2.5/weather"

querystring = {f"lat":"52.1561113","lon":"5.3878266","appid":{WeatherKey},"units":"metric"}

try:
    response = requests.request("GET", url, params=querystring)
except:
    print('Unable to connect to the OpenWeatherAPI')
    sys.exit()

if not response:
    raise Exception(f'Received error from server:{response.text}')
print(response)
print(response.text)
