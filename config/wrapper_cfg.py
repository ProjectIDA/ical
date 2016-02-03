# from config.sensors import Sensors
# from config.sensor import Sensor
# from config.calibs import Calibs
from config.calib import Calib
# from config.auths import Auths
# from config.auth import Auth
# from config.q330s import Q330s
# from config.q330 import Q330
# from config.icalcfgs import Icalcfgs
# from config.icalcfg import Icalcfg

class WrapperCfg(object):

    WRAPPER_KEY_NET               = 'network'
    WRAPPER_KEY_STA               = 'station'
    WRAPPER_KEY_TAGNO             = 'tagno'
    WRAPPER_KEY_SN                = 'sn'
    WRAPPER_KEY_IP                = 'ip_address'
    WRAPPER_KEY_DATAPORT          = 'dataport'
    WRAPPER_KEY_MONPORT_A         = 'sensor_a_mon_port'
    WRAPPER_KEY_MONPORT_B         = 'sensor_b_mon_port'
    WRAPPER_KEY_LAST_LF_A         = 'sensor_a_last_lf'
    WRAPPER_KEY_LAST_LF_B         = 'sensor_b_last_lf'
    WRAPPER_KEY_LAST_HF_A         = 'sensor_a_last_hf'
    WRAPPER_KEY_LAST_HF_B         = 'sensor_b_last_hf'
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

    WRAPPER_KEY_TIMESTAMP_UNK     = 'unk'


    def __init__(self, init_dict={}):
        self.data = {
            self.WRAPPER_KEY_LAST_LF_A : self.WRAPPER_KEY_TIMESTAMP_UNK,
            self.WRAPPER_KEY_LAST_HF_A : self.WRAPPER_KEY_TIMESTAMP_UNK,
            self.WRAPPER_KEY_LAST_LF_B : self.WRAPPER_KEY_TIMESTAMP_UNK,
            self.WRAPPER_KEY_LAST_HF_B : self.WRAPPER_KEY_TIMESTAMP_UNK
        }
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
        return  ' '.join([self.data[self.WRAPPER_KEY_NET],
                self.data[self.WRAPPER_KEY_STA],
                self.data[self.WRAPPER_KEY_TAGNO],
                self.data[self.WRAPPER_KEY_DATAPORT],
                self.data[self.WRAPPER_KEY_MONPORT_A],
                self.data[self.WRAPPER_KEY_MONPORT_B],
                self.data[self.WRAPPER_KEY_LAST_LF_A],
                self.data[self.WRAPPER_KEY_LAST_LF_B],
                self.data[self.WRAPPER_KEY_LAST_HF_A],
                self.data[self.WRAPPER_KEY_LAST_HF_B]])


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
