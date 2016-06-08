#######################################################################################################################
# Copyright (C) 2016  Regents of the University of California
#
# This is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License (GNU GPL) as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# A copy of the GNU General Public License can be found in LICENSE.TXT in the root of the source code repository.
# Additionally, it can be found at http://www.gnu.org/licenses/.
#
# NOTES: Per GNU GPLv3 terms:
#   * This notice must be kept in this source file
#   * Changes to the source must be clearly noted with date & time of change
#
# If you use this software in a product, an explicit acknowledgment in the product documentation of the contribution
# by Project IDA, Institute of Geophysics and Planetary Physics, UCSD would be appreciated but is not required.
#######################################################################################################################

import re
import functools

from config.ical_config_item_reader import IcalConfigItemReader


class SensorBadColumnCountExcept(Exception):
    pass

class SensorMalformedRecordExcept(Exception):
    pass

class Sensor(IcalConfigItemReader):

    SENSOR_COLCOUNT = 5 # this is minimum cause last col (5) is quoted and contains spaces
    SENSOR_NDX_SHORTNAME = 0
    SENSOR_NDX_ACTIVESTATE = 1
    SENSOR_NDX_CTRLLNA = 2
    SENSOR_NDX_CTRLLNB = 3
    SENSOR_NDX_DESCR = 4
    SENSOR_KEY_SHORTNAME = 'short_name'
    SENSOR_KEY_DESCR = 'descr'

    SENSOR_VALUES_ACTIVESTATE = ['na', 'lo', 'hi']

    def __init__(self, record):

        tokens = re.split('\s+',record)
        self.data = {}

        if len(tokens) >= Sensor.SENSOR_COLCOUNT:

            # check middle 3 columns that we really won't use
            # first; Active state,  hi/lo column
            if not (tokens[Sensor.SENSOR_NDX_ACTIVESTATE] in Sensor.SENSOR_VALUES_ACTIVESTATE):
                raise SensorMalformedRecordExcept

            # Check Sensor A control lines
            ctrllines = tokens[Sensor.SENSOR_NDX_CTRLLNA]
            chans = re.split(',', ctrllines)
            if (len(chans) != 4) or (not functools.reduce(lambda cchn, nchn: (cchn and len(re.split(':', nchn)) == 2), chans, True)):
                raise SensorMalformedRecordExcept

            #  check Sensor B cntrl lines
            ctrllines = tokens[Sensor.SENSOR_NDX_CTRLLNB]
            chans = re.split(',', ctrllines)
            if (len(chans) != 4) or (not functools.reduce(lambda cchn, nchn: (cchn and len(re.split(':', nchn)) == 2), chans, True)):
                raise SensorMalformedRecordExcept


            # get all description words together
            tokens[Sensor.SENSOR_NDX_DESCR] = ' '.join(tokens[Sensor.SENSOR_NDX_DESCR:])
            # strip quotes on description
            tokens[Sensor.SENSOR_NDX_DESCR] = tokens[Sensor.SENSOR_NDX_DESCR].strip('"')

            self.data[Sensor.SENSOR_KEY_SHORTNAME] = tokens[Sensor.SENSOR_NDX_SHORTNAME]
            self.data[Sensor.SENSOR_KEY_DESCR] = tokens[Sensor.SENSOR_NDX_DESCR]

        else:
            raise SensorBadColumnCountExcept



    def __str__(self):
        return ' '.join(
                    [self.data[Sensor.SENSOR_KEY_SHORTNAME],
                     self.data[Sensor.SENSOR_KEY_DESCR]
                ])

    def __eq__(self, other):
        return (type(other) == type(self)) and \
            self.data[Sensor.SENSOR_KEY_SHORTNAME] == other.data[Sensor.SENSOR_KEY_SHORTNAME]

    def __lt__(self, other):
        return (type(other) == type(self)) and \
            self.data[Sensor.SENSOR_KEY_SHORTNAME].lower() < other.data[Sensor.SENSOR_KEY_SHORTNAME].lower()

    def write(self):
        pass