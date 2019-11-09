#!/home/mike/Documents/python_envs/location_information_inputs/bin/python3
import requests
import sys
try:
    from urllib.parse import quote
except:
    from urllib import quote
from keys import WeatherKey, TomTomKey

'''
Credentials are imported from a keys file containing key values like this:
WeatherKey = <openweathermap api key>
TomTomKey = <tomtom api key>
'''
LocationAddress = "antwerpen"


class location:
    def __init__(self, LocationAddress, TomTomKey):
        self.LocationAddress = LocationAddress
        self.TomTomKey = TomTomKey
        LocationAddressEncoded = quote(LocationAddress.lower())
        TomTomURL = "https://api.tomtom.com/search/2/geocode/"+LocationAddressEncoded+".json"
        TomTomQuery = {"storeResult":"false","limit":"1","key":self.TomTomKey}
        try:
            self.TomTomLocation = requests.request("GET", TomTomURL, params=TomTomQuery)
        except:
            print('Unable to connect to the TomTomAPI')
            sys.exit()
        if not self.TomTomLocation:
            raise Exception("Received error from server:"+self.TomTomLocation)
        self.LocationLat = self.TomTomLocation.json()["results"][0]["position"]["lat"]
        self.LocationLon = self.TomTomLocation.json()["results"][0]["position"]["lon"]
        self.Address = self.TomTomLocation.json()["results"][0]["address"]["freeformAddress"]

class currentweather:
    def __init__(self, location, WeatherKey):
        WeatherURL = "https://api.openweathermap.org/data/2.5/weather"
        WeatherQuery = {"lat":location.LocationLat,"lon":location.LocationLon,"appid":WeatherKey,"units":"metric"}
        try:
            WeatherCurrent = requests.request("GET", WeatherURL, params=WeatherQuery)
        except:
            print('Unable to connect to the OpenWeatherAPI')
            sys.exit()
        if not WeatherCurrent:
            raise Exception("Received error from server:"+WeatherCurrent.text)
        self.AllInfo = WeatherCurrent.json()
        self.Temperature = self.AllInfo["main"]["temp"]
        self.Cloudiness = self.AllInfo["clouds"]["all"]
        self.Description = self.AllInfo["weather"][0]["description"]
        if self.Cloudiness==0:
            self.Rainfall=0
        try:
            self.Rainfall = self.Rainfall = self.AllInfo["rain"]["1h"]
        except:
            self.Rainfall = 0
