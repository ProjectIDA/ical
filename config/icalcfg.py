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
from config.ical_config_item_reader import IcalConfigItemReader


class IcalcfgBadColumnCountExcept(Exception):
    pass

class IcalcfgMalformedRecordExcept(Exception):
    pass

class Icalcfg(IcalConfigItemReader):

    ICALCFG_COLCOUNT = 12
    ICALCFG_NDX_NET = 0
    ICALCFG_NDX_STA = 1
    ICALCFG_NDX_TAGNO = 2
    ICALCFG_NDX_DATAPORT = 3
    ICALCFG_NDX_MONPORT_A = 4
    ICALCFG_NDX_MONPORT_B = 5
    ICALCFG_NDX_LAST_CAL_A = 6
    ICALCFG_NDX_LAST_CAL_B = 7
    ICALCFG_NDX_LOCATION_A = 8
    ICALCFG_NDX_LOCATION_B = 9
    ICALCFG_NDX_CHANNELS_A = 10
    ICALCFG_NDX_CHANNELS_B = 11

    ICALCFG_KEY_NET = 'network'
    ICALCFG_KEY_STA = 'station'
    ICALCFG_KEY_TAGNO = 'tagno'
    ICALCFG_KEY_DATAPORT = 'dataport'
    ICALCFG_KEY_MONPORT_A = 'sensor_a_mon_port'
    ICALCFG_KEY_MONPORT_B = 'sensor_b_mon_port'
    ICALCFG_KEY_LOCATION_A = 'sensor_a_location'
    ICALCFG_KEY_LOCATION_B = 'sensor_b_location'
    ICALCFG_KEY_CHANNELS_A = 'sensor_a_channels'
    ICALCFG_KEY_CHANNELS_B = 'sensor_b_channels'
    ICALCFG_KEY_LAST_CAL_A = 'sensor_a_last_cal'
    ICALCFG_KEY_LAST_CAL_B = 'sensor_b_last_cal'

    ICALCFG_KEY_NONE     = 'none'

    ICALCFG_NET_VALID_REGEX = '[A-Za-z][A-Za-z0-9]|__'
    ICALCFG_STA_VALID_REGEX = '[A-Za-z][A-Za-z0-9]{2,4}'
    ICALCFG_TAGNO_VALID_REGEX = '\d+'
    ICALCFG_DATAPORT_VALID_REGEX = '[1-4]'
    ICALCFG_MONPORT_A_VALID_REGEX = '[4-6]'
    ICALCFG_MONPORT_B_VALID_REGEX = '[1-3]'
    ICALCFG_LOCATION_VALID_REGEX = '[0-9]{2}'
    ICALCFG_CHANNELS_VALID_REGEX = '[A-Za-z]{2}[Zz]{1} *, *[A-Za-z]{2}[Nn1] *, *[A-Za-z]{2}[Ee2]{1} *'



    def __init__(self, record):

        tokens = re.split('\s+',record.strip())
        self.data = {}

        if len(tokens) == self.ICALCFG_COLCOUNT:

            if not ((re.fullmatch(self.ICALCFG_NET_VALID_REGEX, tokens[self.ICALCFG_NDX_NET]) != None) and
                        (re.fullmatch(self.ICALCFG_STA_VALID_REGEX, tokens[self.ICALCFG_NDX_STA]) != None) and
                        (re.fullmatch(self.ICALCFG_TAGNO_VALID_REGEX, tokens[self.ICALCFG_NDX_TAGNO]) != None) and
                        (re.fullmatch(self.ICALCFG_DATAPORT_VALID_REGEX, tokens[self.ICALCFG_NDX_DATAPORT]) != None) and
                        ((re.fullmatch(self.ICALCFG_MONPORT_A_VALID_REGEX, tokens[self.ICALCFG_NDX_MONPORT_A]) != None) or
                             (tokens[self.ICALCFG_NDX_MONPORT_A] == self.ICALCFG_KEY_NONE)) and

                        ((re.fullmatch(self.ICALCFG_MONPORT_B_VALID_REGEX, tokens[self.ICALCFG_NDX_MONPORT_B]) != None) or
                             (tokens[self.ICALCFG_NDX_MONPORT_B] == self.ICALCFG_KEY_NONE)) and

                        ((re.fullmatch(self.ICALCFG_LOCATION_VALID_REGEX, tokens[self.ICALCFG_NDX_LOCATION_A]) != None) or
                             (tokens[self.ICALCFG_NDX_LOCATION_A] == self.ICALCFG_KEY_NONE)) and

                        ((re.fullmatch(self.ICALCFG_LOCATION_VALID_REGEX, tokens[self.ICALCFG_NDX_LOCATION_B]) != None) or
                             (tokens[self.ICALCFG_NDX_LOCATION_B] == self.ICALCFG_KEY_NONE)) and

                        ((re.fullmatch(self.ICALCFG_CHANNELS_VALID_REGEX, tokens[self.ICALCFG_NDX_CHANNELS_A]) != None) or
                             (tokens[self.ICALCFG_NDX_CHANNELS_A] == self.ICALCFG_KEY_NONE)) and

                        ((re.fullmatch(self.ICALCFG_CHANNELS_VALID_REGEX, tokens[self.ICALCFG_NDX_CHANNELS_B]) != None) or
                             (tokens[self.ICALCFG_NDX_CHANNELS_B] == self.ICALCFG_KEY_NONE))):
                raise IcalcfgMalformedRecordExcept

            self.data[self.ICALCFG_KEY_NET]          = tokens[self.ICALCFG_NDX_NET]
            self.data[self.ICALCFG_KEY_STA]          = tokens[self.ICALCFG_NDX_STA]
            self.data[self.ICALCFG_KEY_TAGNO]        = tokens[self.ICALCFG_NDX_TAGNO]
            self.data[self.ICALCFG_KEY_DATAPORT]     = tokens[self.ICALCFG_NDX_DATAPORT]
            self.data[self.ICALCFG_KEY_MONPORT_A]    = tokens[self.ICALCFG_NDX_MONPORT_A]
            self.data[self.ICALCFG_KEY_MONPORT_B]    = tokens[self.ICALCFG_NDX_MONPORT_B]
            self.data[self.ICALCFG_KEY_LOCATION_A]    = tokens[self.ICALCFG_NDX_LOCATION_A]
            self.data[self.ICALCFG_KEY_LOCATION_B]    = tokens[self.ICALCFG_NDX_LOCATION_B]
            self.data[self.ICALCFG_KEY_LAST_CAL_A]    = tokens[self.ICALCFG_NDX_LAST_CAL_A]
            self.data[self.ICALCFG_KEY_LAST_CAL_B]    = tokens[self.ICALCFG_NDX_LAST_CAL_B]
            self.data[self.ICALCFG_KEY_CHANNELS_A]    = tokens[self.ICALCFG_NDX_CHANNELS_A]
            self.data[self.ICALCFG_KEY_CHANNELS_B]    = tokens[self.ICALCFG_NDX_CHANNELS_B]

        else:
            raise IcalcfgBadColumnCountExcept


    def update(self, upd_dict):
        self.data.update(upd_dict)
 

    def __str__(self):
        return '{:<3} {:<6} {:<7} {:<2} {:<5} {:<5} {<:30} {<:30} {<:3} {<:3} {<:12} {<:12}'.format(
                    self.data[self.ICALCFG_KEY_NET],
                    self.data[self.ICALCFG_KEY_STA],
                    self.data[self.ICALCFG_KEY_TAGNO],
                    self.data[self.ICALCFG_KEY_DATAPORT],
                    self.data[self.ICALCFG_KEY_MONPORT_A],
                    self.data[self.ICALCFG_KEY_MONPORT_B],
                    self.data[self.ICALCFG_KEY_LAST_CAL_A],
                    self.data[self.ICALCFG_KEY_LAST_CAL_B],
                    self.data[self.ICALCFG_KEY_LOCATION_A],
                    self.data[self.ICALCFG_KEY_LOCATION_B],
                    self.data[self.ICALCFG_KEY_CHANNELS_A],
                    self.data[self.ICALCFG_KEY_CHANNELS_B]
        )


    def __eq__(self, other):
            return (type(other) == type(self)) and \
                (self.data[self.ICALCFG_KEY_TAGNO] == other.data[self.ICALCFG_KEY_TAGNO])


    def __lt__(self, other):
        return (type(other) == type(self)) and \
                (int(self.data[self.ICALCFG_KEY_TAGNO]) < int(other.data[self.ICALCFG_KEY_TAGNO]))
