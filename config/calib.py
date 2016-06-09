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
"""Class representing single record from qcal calib file"""

import re
from ida.instruments import CALTYPE_RBLF, CALTYPE_RBHF


class CalibBadColumnCountExcept(Exception):
    pass

class CalibMalformedRecordExcept(Exception):
    pass

class Calib(object):

    CALIB_COLCOUNT = 8
    CALIB_NDX_CALTYPE = 0
    CALIB_NDX_SENSNAME = 1
    CALIB_NDX_WF = 2
    CALIB_NDX_AMP = 3
    CALIB_NDX_DUR = 4
    CALIB_NDX_SET = 5
    CALIB_NDX_TRL = 6
    CALIB_NDX_DIV = 7
    CALIB_KEY_SENSNAME = 'sensor_comp_name'
    CALIB_KEY_CALTYPE = 'caltype'
    CALIB_KEY_WF = 'wf'
    CALIB_KEY_AMP = 'amp'
    CALIB_KEY_DUR = 'dur'
    CALIB_KEY_SET = 'set'
    CALIB_KEY_TRL = 'trl'
    CALIB_KEY_DIV = 'div'
    CALIB_CALTYPE_1 = CALTYPE_RBLF
    CALIB_CALTYPE_2 = CALTYPE_RBHF
    CALIB_VALUES_CALTYPE = [CALIB_CALTYPE_1, CALIB_CALTYPE_2]
    CALIB_DESCRIPTIONS = {
        CALIB_CALTYPE_1: "Low Freq; Random Binary",
        CALIB_CALTYPE_2: "High Freq; Random Binary",
    }


    @classmethod 
    def caltype_descr(cls, caltype):
        return cls.CALIB_DESCRIPTIONS.get(caltype, 'INVALID CAL TYPE: ' + caltype)



    def __init__(self, record):

        tokens = re.split('\s+',record.strip())
        self.data = {}

        if len(tokens) == Calib.CALIB_COLCOUNT:

            # first; Check cal type
            if not (tokens[Calib.CALIB_NDX_CALTYPE] in Calib.CALIB_VALUES_CALTYPE):
                raise CalibMalformedRecordExcept

            if not ((re.fullmatch('\d+', tokens[Calib.CALIB_NDX_WF]) != None) and 
                    (re.fullmatch('\d+', tokens[Calib.CALIB_NDX_AMP]) != None) and
                    (re.fullmatch('\d+', tokens[Calib.CALIB_NDX_DUR]) != None) and
                    (re.fullmatch('\d+', tokens[Calib.CALIB_NDX_SET]) != None) and
                    (re.fullmatch('\d+', tokens[Calib.CALIB_NDX_TRL]) != None) and
                    (re.fullmatch('\d+', tokens[Calib.CALIB_NDX_DIV]) != None)):
                raise CalibMalformedRecordExcept

            self.data[Calib.CALIB_KEY_SENSNAME] = tokens[Calib.CALIB_NDX_SENSNAME]
            self.data[Calib.CALIB_KEY_CALTYPE] = tokens[Calib.CALIB_NDX_CALTYPE]
            self.data[Calib.CALIB_KEY_WF]  = tokens[Calib.CALIB_NDX_WF]
            self.data[Calib.CALIB_KEY_AMP] = tokens[Calib.CALIB_NDX_AMP]
            self.data[Calib.CALIB_KEY_DUR] = tokens[Calib.CALIB_NDX_DUR]
            self.data[Calib.CALIB_KEY_SET] = tokens[Calib.CALIB_NDX_SET]
            self.data[Calib.CALIB_KEY_TRL] = tokens[Calib.CALIB_NDX_TRL]
            self.data[Calib.CALIB_KEY_DIV] = tokens[Calib.CALIB_NDX_DIV]

        else:
            raise CalibBadColumnCountExcept

    def __str__(self):
        return ' '.join( [
                    self.data[Calib.CALIB_KEY_SENSNAME],
                    self.data[Calib.CALIB_KEY_CALTYPE],
                    self.data[Calib.CALIB_KEY_WF],
                    self.data[Calib.CALIB_KEY_AMP],
                    self.data[Calib.CALIB_KEY_DUR],
                    self.data[Calib.CALIB_KEY_SET],
                    self.data[Calib.CALIB_KEY_TRL],
                    self.data[Calib.CALIB_KEY_DIV]
                ])

    def cal_time_sec(self):
        try:
            secs = int(self.data[Calib.CALIB_KEY_DUR]) + \
                    int(self.data[Calib.CALIB_KEY_SET]) + \
                    int(self.data[Calib.CALIB_KEY_TRL])
        except:
            secs = None

        return secs

    def cal_time_min(self):
        secs = self.cal_time_sec()
        if secs:
            mins = secs / 60
        else:
            mins = None

        return mins

    def __eq__(self, other):
            return (type(other) == type(self)) and \
                ((self.data[Calib.CALIB_KEY_SENSNAME].lower() == other.data[Calib.CALIB_KEY_SENSNAME].lower()) and 
                (self.data[Calib.CALIB_KEY_CALTYPE].lower() == other.data[Calib.CALIB_KEY_CALTYPE].lower()))


    def __lt__(self, other):
        return (type(other) == type(self)) and \
            ((self.data[Calib.CALIB_KEY_SENSNAME].lower() < other.data[Calib.CALIB_KEY_SENSNAME].lower()) or 
            ((self.data[Calib.CALIB_KEY_SENSNAME].lower() == other.data[Calib.CALIB_KEY_SENSNAME].lower()) and 
                (self.data[Calib.CALIB_KEY_CALTYPE].lower() < other.data[Calib.CALIB_KEY_CALTYPE].lower())))
