import re
import functools

from config.ical_config_item_reader import IcalConfigItemReader
from config.ical_config_item_writer import IcalConfigItemWriter


class IcalcfgBadColumnCountExcept(Exception):
    pass

class IcalcfgMalformedRecordExcept(Exception):
    pass

class Icalcfg(IcalConfigItemReader, IcalConfigItemWriter):

    ICALCFG_COLCOUNT = 10
    ICALCFG_NDX_NET = 0
    ICALCFG_NDX_STA = 1
    ICALCFG_NDX_TAGNO = 2
    ICALCFG_NDX_DATAPORT = 3
    ICALCFG_NDX_MONPORT_A = 4
    ICALCFG_NDX_MONPORT_B = 5
    ICALCFG_NDX_LAST_LF_A = 6
    ICALCFG_NDX_LAST_HF_A = 7
    ICALCFG_NDX_LAST_LF_B = 8
    ICALCFG_NDX_LAST_HF_B = 9

    ICALCFG_KEY_NET = 'network'
    ICALCFG_KEY_STA = 'station'
    ICALCFG_KEY_TAGNO = 'tagno'
    ICALCFG_KEY_DATAPORT = 'dataport'
    ICALCFG_KEY_MONPORT_A = 'sensor_a_mon_port'
    ICALCFG_KEY_MONPORT_B = 'sensor_b_mon_port'
    ICALCFG_KEY_LAST_LF_A = 'sensor_a_last_lf'
    ICALCFG_KEY_LAST_HF_A = 'sensor_a_last_hf'
    ICALCFG_KEY_LAST_LF_B = 'sensor_b_last_lf'
    ICALCFG_KEY_LAST_HF_B = 'sensor_b_last_hf'


    def __init__(self, record):

        tokens = re.split('\s+',record.strip())
        self.data = {}

        if len(tokens) == Icalcfg.ICALCFG_COLCOUNT:

            if not ((re.fullmatch('[A-Za-z][A-Za-z0-9]{1,9}', tokens[Icalcfg.ICALCFG_NDX_NET]) != None) and
                    (re.fullmatch('[A-Za-z][A-Za-z0-9]{2,5}', tokens[Icalcfg.ICALCFG_NDX_STA]) != None) and
                    (re.fullmatch('\d+', tokens[Icalcfg.ICALCFG_NDX_TAGNO]) != None) and
                    (re.fullmatch('[1-4]', tokens[Icalcfg.ICALCFG_NDX_DATAPORT]) != None) and
                    (re.fullmatch('[0,4-6]', tokens[Icalcfg.ICALCFG_NDX_MONPORT_A]) != None) and
                    (re.fullmatch('[0,1-3]', tokens[Icalcfg.ICALCFG_NDX_MONPORT_B]) != None)):
                raise IcalcfgMalformedRecordExcept

            self.data[Icalcfg.ICALCFG_KEY_NET]          = tokens[Icalcfg.ICALCFG_NDX_NET]
            self.data[Icalcfg.ICALCFG_KEY_STA]          = tokens[Icalcfg.ICALCFG_NDX_STA]
            self.data[Icalcfg.ICALCFG_KEY_TAGNO]        = tokens[Icalcfg.ICALCFG_NDX_TAGNO]
            self.data[Icalcfg.ICALCFG_KEY_DATAPORT]     = tokens[Icalcfg.ICALCFG_NDX_DATAPORT]
            self.data[Icalcfg.ICALCFG_KEY_MONPORT_A]    = tokens[Icalcfg.ICALCFG_NDX_MONPORT_A]
            self.data[Icalcfg.ICALCFG_KEY_MONPORT_B]    = tokens[Icalcfg.ICALCFG_NDX_MONPORT_B]

            # deal with parsing dates of last calibrations
            try:
                self.data[Icalcfg.ICALCFG_KEY_LAST_LF_A] = 'unk' if tokens[Icalcfg.ICALCFG_NDX_LAST_LF_A] == 'unk' else dateutil.parser.parse(tokens[Icalcfg.ICALCFG_NDX_LAST_LF_A])
            except Exception:
                self.data[Icalcfg.ICALCFG_KEY_LAST_LF_A] = 'unk'

            try:
                self.data[Icalcfg.ICALCFG_KEY_LAST_HF_A] = 'unk' if tokens[Icalcfg.ICALCFG_NDX_LAST_HF_A] == 'unk' else dateutil.parser.parse(tokens[Icalcfg.ICALCFG_NDX_LAST_HF_A])
            except Exception:
                self.data[Icalcfg.ICALCFG_KEY_LAST_HF_A] = 'unk'

            try:
                self.data[Icalcfg.ICALCFG_KEY_LAST_LF_B] = 'unk' if tokens[Icalcfg.ICALCFG_NDX_LAST_LF_B] == 'unk' else dateutil.parser.parse(tokens[Icalcfg.ICALCFG_NDX_LAST_LF_B])
            except Exception:
                self.data[Icalcfg.ICALCFG_KEY_LAST_LF_B] = 'unk'

            try:
                self.data[Icalcfg.ICALCFG_KEY_LAST_HF_B] = 'unk' if tokens[Icalcfg.ICALCFG_NDX_LAST_HF_B] == 'unk' else dateutil.parser.parse(tokens[Icalcfg.ICALCFG_NDX_LAST_HF_B])
            except Exception:
                self.data[Icalcfg.ICALCFG_KEY_LAST_HF_B] = 'unk'

        else:
            raise IcalcfgBadColumnCountExcept
 

    def __str__(self):
        return ' '.join( [
                    self.data[Icalcfg.ICALCFG_KEY_NET],
                    self.data[Icalcfg.ICALCFG_KEY_STA],
                    self.data[Icalcfg.ICALCFG_KEY_TAGNO],
                    self.data[Icalcfg.ICALCFG_KEY_DATAPORT],
                    self.data[Icalcfg.ICALCFG_KEY_MONPORT_A],
                    self.data[Icalcfg.ICALCFG_KEY_MONPORT_B],
                    self.data[Icalcfg.ICALCFG_KEY_LAST_LF_A],
                    self.data[Icalcfg.ICALCFG_KEY_LAST_HF_A],
                    self.data[Icalcfg.ICALCFG_KEY_LAST_LF_B],
                    self.data[Icalcfg.ICALCFG_KEY_LAST_HF_B]
                ])


    def __eq__(self, other):
            return (type(other) == type(self)) and \
                (self.data[Icalcfg.ICALCFG_KEY_TAGNO] == other.data[Icalcfg.ICALCFG_KEY_TAGNO])


    def __lt__(self, other):
        return (type(other) == type(self)) and \
                (int(self.data[Icalcfg.ICALCFG_KEY_TAGNO]) < int(other.data[Icalcfg.ICALCFG_KEY_TAGNO]))
