#!/home/mike/Documents/python_envs/location_information_inputs/bin/python3
from location_class import location, currentweather
from keys import WeatherKey, TomTomKey

LocationAddress = "Amersfoort"

Location = location(LocationAddress, TomTomKey)
print(Location.Address)
