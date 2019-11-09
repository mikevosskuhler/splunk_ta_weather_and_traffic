#!/home/mike/Documents/python_envs/location_information_inputs/bin/python3
import requests
import sys
import urllib.parse
from keys import WeatherKey, TomTomKey

'''
Credentials are imported from a keys files containing key values like this:
WeatherKey = <openweathermap api key>
TomTomKey = <tomtom api key>
'''
LocationAddress = "antwerpen"


class location:
    def __init__(self, LocationAddress, WeatherKey, TomTomKey):
        self.LocationAddress = LocationAddress
        self.WeatherKey = WeatherKey
        self.TomTomKey = TomTomKey
        LocationAddressEncoded = urllib.parse.quote(LocationAddress.lower())
        TomTomURL = f"https://api.tomtom.com/search/2/geocode/{LocationAddressEncoded}.json"
        TomTomQuery = {"storeResult":"false","limit":"1","key":self.TomTomKey}
        try:
            self.TomTomLocation = requests.request("GET", TomTomURL, params=TomTomQuery)
        except:
            print('Unable to connect to the TomTomAPI')
            sys.exit()
        if not self.TomTomLocation:
            raise Exception(f'Received error from server:{self.TomTomLocation}')
        self.LocationLat = self.TomTomLocation.json()["results"][0]["position"]["lat"]
        self.LocationLon = self.TomTomLocation.json()["results"][0]["position"]["lon"]

    def WeatherCurrent(self):
        WeatherURL = "https://api.openweathermap.org/data/2.5/weather"
        WeatherQuery = {"lat":self.LocationLat,"lon":self.LocationLon,"appid":WeatherKey,"units":"metric"}
        try:
            WeatherCurrent = requests.request("GET", WeatherURL, params=WeatherQuery)
        except:
            print('Unable to connect to the OpenWeatherAPI')
            sys.exit()

        if not WeatherCurrent:
            raise Exception(f'Received error from server:{WeatherCurrent.text}')
        return WeatherCurrent

WeatherCurrent = location(LocationAddress, WeatherKey, TomTomKey).WeatherCurrent()
CurrentTemperature = WeatherCurrent.json()["main"]["temp"]
CurrentCloudiness = WeatherCurrent.json()["clouds"]["all"]
if CurrentCloudiness==0:
    CurrentRainfall=0
elif not WeatherCurrent.json()["rain"]:
    CurrentRainfall = 0
else:
    CurrentRainfall = WeatherCurrent.json()["rain"]["1h"]



# CurrentRainfall = WeatherCurrent.json()["rain"]
print(f"It is currently {CurrentTemperature} degrees Celcius,\
 {CurrentCloudiness} percent cloudy, and we have received {CurrentRainfall}\
 mm of rain")

# print(WeatherCurrent.text)

# TomTomURL = f"https://api.tomtom.com/search/2/geocode/{LocationAddressEncoded}.json"
#
# TomTomQuery = {"storeResult":"false","limit":"1","key":"ZCiCzz3SIiuzxCi12Txt50jwBbW3jgOf"}
#
# TomTomLocation = requests.request("GET", TomTomURL, params=TomTomQuery)
#
# LocationLat = TomTomLocation.json()["results"][0]["position"]["lat"]
# LocationLon = TomTomLocation.json()["results"][0]["position"]["lon"]
#
# print(f"coordinates are: {LocationLat}, {LocationLon}")

# WeatherURL = "https://api.openweathermap.org/data/2.5/weather"
#
# WeatherQuery = {f"lat":"52.1561113","lon":"5.3878266","appid":{WeatherKey},"units":"metric"}
#
# try:
#     WeatherCurrent = requests.request("GET", WeatherURL, params=WeatherQuery)
# except:
#     print('Unable to connect to the OpenWeatherAPI')
#     sys.exit()
#
# if not WeatherCurrent:
#     raise Exception(f'Received error from server:{WeatherCurrent.text}')
# print(WeatherCurrent)
# print(WeatherCurrent.text)
