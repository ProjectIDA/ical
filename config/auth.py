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


class AuthBadColumnCountExcept(Exception):
    pass

class AuthMalformedRecordExcept(Exception):
    pass

class Auth(IcalConfigItemReader):

    AUTH_COLCOUNT = 8
    AUTH_NDX_TAGNO = 0
    AUTH_NDX_SN = 1
    AUTH_NDX_CFG_AUTH = 2
    AUTH_NDX_SFN_AUTH = 3
    AUTH_NDX_DP1_AUTH = 4
    AUTH_NDX_DP2_AUTH = 5
    AUTH_NDX_DP3_AUTH = 6
    AUTH_NDX_DP4_AUTH = 7

    AUTH_KEY_TAGNO = 'tagno_auth'
    AUTH_KEY_SN = 'sn'
    AUTH_KEY_CFG_AUTH = 'cfgport_auth'
    AUTH_KEY_SFN_AUTH = 'sfnport_auth'
    AUTH_KEY_DP1_AUTH = 'dp1_auth'
    AUTH_KEY_DP2_AUTH = 'dp2_auth'
    AUTH_KEY_DP3_AUTH = 'dp3_auth'
    AUTH_KEY_DP4_AUTH = 'dp4_auth'

    AUTH_TAGNO_VALID_REGEX = '\d+'
    AUTH_SN_VALID_REGEX = '[0-9A-Fa-f]{16}'
    AUTH_AUTHCODE_VALID_REGEX = '\d+'

    def __init__(self, record):

        tokens = re.split('\s+',record.strip())
        self.data = {}

        if len(tokens) == self.AUTH_COLCOUNT:

            if not ((re.fullmatch(self.AUTH_TAGNO_VALID_REGEX, tokens[self.AUTH_NDX_TAGNO]) != None) and 
                    (re.fullmatch(self.AUTH_SN_VALID_REGEX, tokens[self.AUTH_NDX_SN]) != None) and
                    (re.fullmatch(self.AUTH_AUTHCODE_VALID_REGEX, tokens[self.AUTH_NDX_DP1_AUTH]) != None)
                    ):
                raise AuthMalformedRecordExcept

            self.data[self.AUTH_KEY_TAGNO]      = tokens[self.AUTH_NDX_TAGNO]
            self.data[self.AUTH_KEY_SN]         = tokens[self.AUTH_NDX_SN]
            self.data[self.AUTH_KEY_CFG_AUTH]   = tokens[self.AUTH_NDX_CFG_AUTH]
            self.data[self.AUTH_KEY_SFN_AUTH]   = tokens[self.AUTH_NDX_SFN_AUTH]
            self.data[self.AUTH_KEY_DP1_AUTH]   = tokens[self.AUTH_NDX_DP1_AUTH]
            self.data[self.AUTH_KEY_DP2_AUTH]   = tokens[self.AUTH_NDX_DP2_AUTH]
            self.data[self.AUTH_KEY_DP3_AUTH]   = tokens[self.AUTH_NDX_DP3_AUTH]
            self.data[self.AUTH_KEY_DP4_AUTH]   = tokens[self.AUTH_NDX_DP4_AUTH]

        else:
            raise AuthBadColumnCountExcept

 
    def __str__(self):
        return ' '.join( [
                    self.data[self.AUTH_KEY_TAGNO],
                    self.data[self.AUTH_KEY_SN],
                    self.data[self.AUTH_KEY_CFG_AUTH],
                    self.data[self.AUTH_KEY_SFN_AUTH],
                    self.data[self.AUTH_KEY_DP1_AUTH],
                    self.data[self.AUTH_KEY_DP2_AUTH],
                    self.data[self.AUTH_KEY_DP3_AUTH],
                    self.data[self.AUTH_KEY_DP4_AUTH]
                ])


    def __eq__(self, other):
            return (type(other) == type(self)) and \
                (self.data[self.AUTH_KEY_TAGNO] == other.data[self.AUTH_KEY_TAGNO])


    def __lt__(self, other):
        return (type(other) == type(self)) and \
                (int(self.data[self.AUTH_KEY_TAGNO]) < int(other.data[self.AUTH_KEY_TAGNO]))
