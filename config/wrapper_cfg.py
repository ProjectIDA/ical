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


    def __init__(self, init_dict={}):
        self.data = init_dict


    def update(self, update_dict):
        self.data.update(update_dict)


    def gen_qcal_cmdline(self, sensor, caltype):

        if (sensor in ['A', 'B']) and caltype in Calib.CALIB_VALUES_CALTYPE:
            # return 'please run ' + caltype + ' on sensor ' + sensor
            cmd = ''.join([
                        'qcal ',
                        self.data[WrapperCfg.WRAPPER_KEY_IP],
                        ':',
                        self.data[WrapperCfg.WRAPPER_KEY_DATAPORT],
                        ':',
                        caltype,
                        '00',
                        sensor,
                        self.data[WrapperCfg.WRAPPER_KEY_MONPORT_A] if sensor == 'A' else self.data[WrapperCfg.WRAPPER_KEY_MONPORT_B],
                        ':',
                        self.data[WrapperCfg.WRAPPER_KEY_STA],
                        ':',
                        self.data[WrapperCfg.WRAPPER_KEY_NET],
                        ' '+caltype,
                        ' cal='+'123' if sensor == 'A' else '456',
                        ' mon='+self.data[WrapperCfg.WRAPPER_KEY_MONPORT_A] if sensor == 'A' else self.data[WrapperCfg.WRAPPER_KEY_MONPORT_B],
                        ' root=./'])
            return cmd

        else:
            return 'ERROR: Check sensors [' + sensor + '] and caltype [' + caltype + ']'


    def __str__(self):
        return str(self.data)


    def __eq__(self, other):
            return (type(other) == type(self)) and \
                ((self.data[WrapperCfg.WRAPPER_KEY_STA].lower() == other.data[WrapperCfg.WRAPPER_KEY_STA].lower()) and 
                (self.data[WrapperCfg.WRAPPER_KEY_TAGNO].lower() == other.data[WrapperCfg.WRAPPER_KEY_TAGNO].lower()))


    def __lt__(self, other):
        return (type(other) == type(self)) and \
            ((self.data[WrapperCfg.WRAPPER_KEY_STA].lower() < other.data[WrapperCfg.WRAPPER_KEY_STA].lower()) or 
            ((self.data[WrapperCfg.WRAPPER_KEY_STA].lower() == other.data[WrapperCfg.WRAPPER_KEY_STA].lower()) and 
                (self.data[WrapperCfg.WRAPPER_KEY_TAGNO].lower() < other.data[WrapperCfg.WRAPPER_KEY_TAGNO].lower())))
