import re
import functools

from config.ical_config_item_reader import IcalConfigItemReader


class Q330BadColumnCountExcept(Exception):
    pass

class Q330MalformedRecordExcept(Exception):
    pass

class Q330(IcalConfigItemReader):

    Q330_COLCOUNT = 4
    Q330_NDX_IP = 0
    Q330_NDX_TAGNO = 1
    Q330_NDX_SENS_COMPNAME_A = 2
    Q330_NDX_SENS_COMPNAME_B = 3

    Q330_KEY_IP = 'ip_address'
    Q330_KEY_TAGNO = 'tagno_q330cfg'
    Q330_KEY_SENS_COMPNAME_A = 'sensor_a_comp_name'
    Q330_KEY_SENS_COMPNAME_B = 'sensor_b_comp_name'
    Q330_KEY_SENS_ROOTNAME_A = 'sensor_a_root_name'
    Q330_KEY_SENS_ROOTNAME_B = 'sensor_b_root_name'


    def __init__(self, record):

        tokens = re.split('\s+',record.strip())
        self.data = {}

        if len(tokens) == self.Q330_COLCOUNT:

            if not ((re.fullmatch('\d+\.\d+\.\d+\.\d+', tokens[self.Q330_NDX_IP]) != None) and 
                    (re.fullmatch('\d+', tokens[self.Q330_NDX_TAGNO]) != None)):
                raise Q330MalformedRecordExcept

            self.data[self.Q330_KEY_IP]                 = tokens[self.Q330_NDX_IP]
            self.data[self.Q330_KEY_TAGNO]              = tokens[self.Q330_NDX_TAGNO]
            self.data[self.Q330_KEY_SENS_COMPNAME_A]    = tokens[self.Q330_NDX_SENS_COMPNAME_A]
            self.data[self.Q330_KEY_SENS_COMPNAME_B]    = tokens[self.Q330_NDX_SENS_COMPNAME_B]
            self.data[self.Q330_KEY_SENS_ROOTNAME_A]    = tokens[self.Q330_NDX_SENS_COMPNAME_A].split(':')[0]
            self.data[self.Q330_KEY_SENS_ROOTNAME_B]    = tokens[self.Q330_NDX_SENS_COMPNAME_B].split(':')[0]

        else:
            raise Q330BadColumnCountExcept

 
    def __str__(self):
        return ' '.join( [
                    self.data[self.Q330_KEY_IP],
                    self.data[self.Q330_KEY_TAGNO],
                    self.data[self.Q330_KEY_SENS_COMPNAME_A],
                    self.data[self.Q330_KEY_SENS_COMPNAME_B]
                ])


    def __eq__(self, other):
            return (type(other) == type(self)) and \
                (self.data[self.Q330_KEY_TAGNO] == other.data[self.Q330_KEY_TAGNO])


    def __lt__(self, other):
        return (type(other) == type(self)) and \
                (int(self.data[self.Q330_KEY_TAGNO]) < int(other.data[self.Q330_KEY_TAGNO]))
