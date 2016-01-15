import re
import functools

from config.ical_config_item_reader import IcalConfigItemReader
from config.ical_config_item_writer import IcalConfigItemWriter


class AuthBadColumnCountExcept(Exception):
    pass

class AuthMalformedRecordExcept(Exception):
    pass

class Auth(IcalConfigItemReader, IcalConfigItemWriter):

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


    def __init__(self, record):

        tokens = re.split('\s+',record.strip())
        self.data = {}

        if len(tokens) == Auth.AUTH_COLCOUNT:

            if not ((re.fullmatch('\d+', tokens[Auth.AUTH_NDX_TAGNO]) != None) and 
                    (re.fullmatch('[0-9A-Fa-f]{16}', tokens[Auth.AUTH_NDX_SN]) != None)):
                raise AuthMalformedRecordExcept

            self.data[Auth.AUTH_KEY_TAGNO]      = tokens[Auth.AUTH_NDX_TAGNO]
            self.data[Auth.AUTH_KEY_SN]         = tokens[Auth.AUTH_NDX_SN]
            self.data[Auth.AUTH_KEY_CFG_AUTH]   = tokens[Auth.AUTH_NDX_CFG_AUTH]
            self.data[Auth.AUTH_KEY_SFN_AUTH]   = tokens[Auth.AUTH_NDX_SFN_AUTH]
            self.data[Auth.AUTH_KEY_DP1_AUTH]   = tokens[Auth.AUTH_NDX_DP1_AUTH]
            self.data[Auth.AUTH_KEY_DP2_AUTH]   = tokens[Auth.AUTH_NDX_DP2_AUTH]
            self.data[Auth.AUTH_KEY_DP3_AUTH]   = tokens[Auth.AUTH_NDX_DP3_AUTH]
            self.data[Auth.AUTH_KEY_DP4_AUTH]   = tokens[Auth.AUTH_NDX_DP4_AUTH]

        else:
            raise AuthBadColumnCountExcept

 
    def __str__(self):
        return ' '.join( [
                    self.data[Auth.AUTH_KEY_TAGNO],
                    self.data[Auth.AUTH_KEY_SN],
                    self.data[Auth.AUTH_KEY_CFG_AUTH],
                    self.data[Auth.AUTH_KEY_SFN_AUTH],
                    self.data[Auth.AUTH_KEY_DP1_AUTH],
                    self.data[Auth.AUTH_KEY_DP2_AUTH],
                    self.data[Auth.AUTH_KEY_DP3_AUTH],
                    self.data[Auth.AUTH_KEY_DP4_AUTH]
                ])


    def __eq__(self, other):
            return (type(other) == type(self)) and \
                (self.data[Auth.AUTH_KEY_TAGNO] == other.data[Auth.AUTH_KEY_TAGNO])


    def __lt__(self, other):
        return (type(other) == type(self)) and \
                (int(self.data[Auth.AUTH_KEY_TAGNO]) < int(other.data[Auth.AUTH_KEY_TAGNO]))
