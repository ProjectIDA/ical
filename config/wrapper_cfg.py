import re
from config.calib import Calib
from config.auth import Auth
from config.q330 import Q330
from config.icalcfg import Icalcfg

class WrapperCfg(object):

    WRAPPER_KEY_NET               = 'network'
    WRAPPER_KEY_STA               = 'station'
    WRAPPER_KEY_TAGNO             = 'tagno'
    WRAPPER_KEY_SN                = 'sn'
    WRAPPER_KEY_IP                = 'ip_address'
    WRAPPER_KEY_DATAPORT          = 'dataport'
    WRAPPER_KEY_MONPORT_A         = 'sensor_a_mon_port'
    WRAPPER_KEY_MONPORT_B         = 'sensor_b_mon_port'
    WRAPPER_KEY_LOCATION_A        = 'sensor_a_location'
    WRAPPER_KEY_LOCATION_B        = 'sensor_b_location'
    WRAPPER_KEY_CHANNELS_A        = 'sensor_a_channels'
    WRAPPER_KEY_CHANNELS_B        = 'sensor_b_channels'
    WRAPPER_KEY_LAST_CAL_A        = 'sensor_a_last_cal'
    WRAPPER_KEY_LAST_CAL_B        = 'sensor_b_last_cal'
    WRAPPER_KEY_SENS_COMPNAME_A   = 'sensor_a_comp_name'
    WRAPPER_KEY_SENS_COMPNAME_B   = 'sensor_b_comp_name'
    WRAPPER_KEY_SENS_ROOTNAME_A   = 'sensor_a_root_name'
    WRAPPER_KEY_SENS_ROOTNAME_B   = 'sensor_b_root_name'
    WRAPPER_KEY_SENS_DESCR_A      = 'sensor_a_descr'
    WRAPPER_KEY_SENS_DESCR_B      = 'sensor_b_descr'
    WRAPPER_KEY_CFG_AUTH          = 'cfgport_auth'
    WRAPPER_KEY_SFN_AUTH          = 'sfnport_auth'
    WRAPPER_KEY_DP1_AUTH          = 'dp1_auth'
    WRAPPER_KEY_DP2_AUTH          = 'dp2_auth'
    WRAPPER_KEY_DP3_AUTH          = 'dp3_auth'
    WRAPPER_KEY_DP4_AUTH          = 'dp4_auth'

    WRAPPER_KEY_NONE              = 'none'  # this text val much match 'none' in the sensor and calib cfg files.
    WRAPPER_SENSOR_UNK            = 'UNK SENSOR'


    @classmethod
    def is_valid_wcfg_key(cls, key, val):

        if key == cls.WRAPPER_KEY_NET:
            return re.fullmatch(Icalcfg.ICALCFG_NET_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_STA:
            return re.fullmatch(Icalcfg.ICALCFG_STA_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_IP:
            return re.fullmatch(Q330.Q330_IP_VALID_REGEX, 
                val) != None
        elif key == cls.WRAPPER_KEY_TAGNO:
            return re.fullmatch(Icalcfg.ICALCFG_TAGNO_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_SN:
            return re.fullmatch(Auth.AUTH_SN_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_DATAPORT:
            return re.fullmatch(Icalcfg.ICALCFG_DATAPORT_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_DP1_AUTH:
            return re.fullmatch(Auth.AUTH_AUTHCODE_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_MONPORT_A:
            return re.fullmatch(Icalcfg.ICALCFG_MONPORT_A_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_MONPORT_B:
            return re.fullmatch(Icalcfg.ICALCFG_MONPORT_B_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_LOCATION_A:
            return re.fullmatch(Icalcfg.ICALCFG_LOCATION_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_LOCATION_B:
            return re.fullmatch(Icalcfg.ICALCFG_LOCATION_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_CHANNELS_A:
            return re.fullmatch(Icalcfg.ICALCFG_CHANNELS_VALID_REGEX, val) != None
        elif key == cls.WRAPPER_KEY_CHANNELS_B:
            return re.fullmatch(Icalcfg.ICALCFG_CHANNELS_VALID_REGEX, val) != None

    @classmethod
    def new_dict(cls):
        return {
            cls.WRAPPER_KEY_NET : '',
            cls.WRAPPER_KEY_STA : '',
            cls.WRAPPER_KEY_TAGNO : '',
            cls.WRAPPER_KEY_SN : '',
            cls.WRAPPER_KEY_IP : '',
            cls.WRAPPER_KEY_DATAPORT : '',
            cls.WRAPPER_KEY_MONPORT_A : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_MONPORT_B : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_LAST_CAL_A : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_LAST_CAL_B : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_SENS_COMPNAME_A : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_SENS_COMPNAME_B : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_SENS_ROOTNAME_A : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_SENS_ROOTNAME_B : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_SENS_DESCR_A : '',
            cls.WRAPPER_KEY_SENS_DESCR_B : '',
            cls.WRAPPER_KEY_CFG_AUTH : '',
            cls.WRAPPER_KEY_SFN_AUTH : '',
            cls.WRAPPER_KEY_DP1_AUTH : '',
            cls.WRAPPER_KEY_DP2_AUTH : '',
            cls.WRAPPER_KEY_DP3_AUTH : '',
            cls.WRAPPER_KEY_DP4_AUTH : '',
            cls.WRAPPER_KEY_LOCATION_A : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_LOCATION_B : cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_CHANNELS_A: cls.WRAPPER_KEY_NONE,
            cls.WRAPPER_KEY_CHANNELS_B: cls.WRAPPER_KEY_NONE
        }

    def __init__(self, init_dict={}):
        self.data = self.new_dict()
        self.update(init_dict)


    def update(self, update_dict):
        self.data.update(update_dict)
        self.sortkey = self.data.get(WrapperCfg.WRAPPER_KEY_NET, 'net').ljust(10, ' ') + \
                        self.data.get(WrapperCfg.WRAPPER_KEY_STA, 'sta').ljust(10, ' ') + \
                        self.data.get(WrapperCfg.WRAPPER_KEY_TAGNO, 'tagno').ljust(10, ' ')


    def gen_qcal_cmdline(self, sensor, caltype):

        if (sensor in ['A', 'B']) and caltype in Calib.CALIB_VALUES_CALTYPE:
            # return 'please run ' + caltype + ' on sensor ' + sensor
            calports = '123' if sensor == 'A' else '456'
            monport = self.data[WrapperCfg.WRAPPER_KEY_MONPORT_A] if sensor == 'A' else self.data[WrapperCfg.WRAPPER_KEY_MONPORT_B]

            cmd = ''.join([
                        'qcal ',
                        self.data[WrapperCfg.WRAPPER_KEY_IP],
                        ':',
                        self.data[WrapperCfg.WRAPPER_KEY_DATAPORT],
                        ':',
                        caltype,
                        '00',
                        sensor,
                        monport,
                        ':',
                        self.data[WrapperCfg.WRAPPER_KEY_STA],
                        ':',
                        self.data[WrapperCfg.WRAPPER_KEY_NET],
                        ' '+caltype,
                        ' cal='+calports,
                        ' mon='+monport 
                        ]) # caller responsible for appending confgi root_dir cmd param: root='...'
            return cmd

        else:
            return 'ERROR: Check sensors [' + sensor + '] and caltype [' + caltype + ']'


    def ical_rec(self):

        rec = '{:<3} {:<6} {:<7} {:<2} {:<5} {:<5} {:<30} {:<30} {:<3} {:<3} {:<12} {:<12}'.format(
                    self.data[self.WRAPPER_KEY_NET],
                    self.data[self.WRAPPER_KEY_STA],
                    self.data[self.WRAPPER_KEY_TAGNO],
                    self.data[self.WRAPPER_KEY_DATAPORT],
                    self.data[self.WRAPPER_KEY_MONPORT_A],
                    self.data[self.WRAPPER_KEY_MONPORT_B],
                    self.data[self.WRAPPER_KEY_LAST_CAL_A],
                    self.data[self.WRAPPER_KEY_LAST_CAL_B],
                    self.data[self.WRAPPER_KEY_LOCATION_A],
                    self.data[self.WRAPPER_KEY_LOCATION_B],
                    self.data[self.WRAPPER_KEY_CHANNELS_A],
                    self.data[self.WRAPPER_KEY_CHANNELS_B])

        return rec

    def q330_rec(self):
        return ' '.join([self.data[self.WRAPPER_KEY_IP],
                self.data[self.WRAPPER_KEY_TAGNO],
                self.data[self.WRAPPER_KEY_SENS_COMPNAME_A],
                self.data[self.WRAPPER_KEY_SENS_COMPNAME_B]])


    def auth_rec(self):
        return  ' '.join([self.data[self.WRAPPER_KEY_TAGNO],
                self.data[self.WRAPPER_KEY_SN],
                self.data[self.WRAPPER_KEY_CFG_AUTH],
                self.data[self.WRAPPER_KEY_SFN_AUTH],
                self.data[self.WRAPPER_KEY_DP1_AUTH],
                self.data[self.WRAPPER_KEY_DP2_AUTH],
                self.data[self.WRAPPER_KEY_DP3_AUTH],
                self.data[self.WRAPPER_KEY_DP4_AUTH]])


    def tagno(self):
        return self.data.get(WrapperCfg.WRAPPER_KEY_TAGNO)


    def __str__(self):
        return str(self.data)


    def __eq__(self, other):
            return (type(other) == type(self)) and (self.sortkey == other.sortkey)


    def __lt__(self, other):
        return (type(other) == type(self)) and (self.sortkey < other.sortkey)
