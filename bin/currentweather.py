#!/usr/bin/env python3
# coding=utf-8
#
# Copyright © 2011-2015 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function, unicode_literals
import app
import os,sys
import time
from keys import WeatherKey, TomTomKey
from location_class import location, currentweather

splunkhome = os.environ['SPLUNK_HOME']
sys.path.append(os.path.join(splunkhome, 'etc', 'apps', 'searchcommands_app', 'lib'))
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators
from splunklib.six.moves import range


@Configuration()
class GenerateCurrentWeatherCommand(GeneratingCommand):

    locations = Option(require=True, validate=validators.List())

    def generate(self):
        self.logger.debug("Generating %s events" % self.locations)
        n = 1
        for i in self.locations:
            Location = location(i, TomTomKey)
            CurrentWeather = currentweather(Location, WeatherKey)
            Lon = "longitude=\"" + str(Location.LocationLon) + "\" "
            Lat = "lattitude=\"" + str(Location.LocationLat) + "\" "
            Address = "address=\"" + str(Location.Address) + "\" "
            Temp = "temperature=\"" + str(CurrentWeather.Temperature) + "\""
            Clouds = "clouds=\"" + str(CurrentWeather.Cloudiness) + "\""
            Rain = "rain=\"" + str(CurrentWeather.Rainfall) + "\""
            text = Lon + Lat + Address + Temp + Clouds + Rain
            yield {'_time': time.time(), 'event_no': n, '_raw': text}
            n += 1

dispatch(GenerateCurrentWeatherCommand, sys.argv, sys.stdin, sys.stdout, __name__)
