import re
import functools

from config.ical_config_item_reader import IcalConfigItemReader


class CalibBadColumnCountExcept(Exception):
    pass

class CalibMalformedRecordExcept(Exception):
    pass

class Calib(IcalConfigItemReader):

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
    CALIB_CALTYPE_1 = 'rblf'
    CALIB_CALTYPE_2 = 'rbhf'
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
