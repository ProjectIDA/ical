# from config.io import *
from config.utils import configresult

from config.wrapper_cfg import WrapperCfg

from config.sensors import Sensors
from config.sensor import Sensor
from config.calibs import Calibs
from config.calib import Calib
from config.auths import Auths
from config.auth import Auth
from config.q330s import Q330s
from config.q330 import Q330
from config.icalcfgs import Icalcfgs
from config.icalcfg import Icalcfg

import os

class IcalFileNotFound(Exception):
    pass

class IcalWriteError(Exception):
    pass

class IcalConfig(object):

    ICAL_ICALCFG_FILEKEY = 'ical'
    ICAL_Q330CFG_FILEKEY = 'q330'
    ICAL_AUTH_FILEKEY = 'auth'
    ICAL_CALIB_FILEKEY = 'calib'
    ICAL_SENSOR_FILEKEY = 'sensor'
    ICAL_LCQ_FILEKEY = 'lcq'
    ICAL_DETECTOR_FILEKEY = 'detector'

    ICALDB_FILE_STRUCT = {
        ICAL_ICALCFG_FILEKEY: {
            'path': os.sep.join(['.', 'etc']),
            'file': 'ical.cfg'
        },
        ICAL_Q330CFG_FILEKEY: {
            'path': os.sep.join(['.', 'etc']),
            'file': 'q330.cfg'
        },
        ICAL_AUTH_FILEKEY: {
            'path': os.sep.join(['.', 'etc', 'q330']),
            'file': 'auth'
        },
        ICAL_LCQ_FILEKEY: {
            'path': os.sep.join(['.', 'etc', 'q330']),
            'file': 'lcq'
        },
        ICAL_CALIB_FILEKEY: {
            'path': os.sep.join(['.', 'etc', 'q330']),
            'file': 'calib'
        },
        ICAL_SENSOR_FILEKEY: {
            'path': os.sep.join(['.', 'etc', 'q330']),
            'file': 'sensor'
        },
        ICAL_DETECTOR_FILEKEY: {
            'path': os.sep.join(['.', 'etc', 'q330']),
            'file': 'detector'
        },
    }


    def __init__(self, cfg_dir='.'):

        self._root_dir = cfg_dir
        self.clear()


    def clear(self):

        self._config = {
            'ical'    : None,
            'q330'    : None,
            'auth'    : None,
            'sensor' : None,
            'calib'   : None
        }
        self.merged_cfg = []

        self._loaded = False

        self.warnmsgs = []
        self.errmsgs = []


    def load_config(self):

        self.clear()
        success = True

        # read sensor
        success_sensor_cfg, wmsgs, emsgs  = self.load_config_file(IcalConfig.ICAL_SENSOR_FILEKEY)
        self.warnmsgs.extend(wmsgs); self.errmsgs.extend(emsgs)


        # read calib, will sensors complex names against calib records for matches
        success_calib_cfg, wmsgs, emsgs  = self.load_config_file(IcalConfig.ICAL_CALIB_FILEKEY)
        self.warnmsgs.extend(wmsgs); self.errmsgs.extend(emsgs)

        # read ok so far, read q330
        if success_sensor_cfg and success_calib_cfg:
            # read ical.cfg
            success_ical_cfg, wmsgs, emsgs = self.load_config_file(IcalConfig.ICAL_ICALCFG_FILEKEY)
            self.warnmsgs.extend(wmsgs); self.errmsgs.extend(emsgs)

            # read q330.cfg
            success_q330_cfg, wmsgs, emsgs = self.load_config_file(IcalConfig.ICAL_Q330CFG_FILEKEY)
            self.warnmsgs.extend(wmsgs); self.errmsgs.extend(emsgs)

            # read auth
            success_auth_cfg, wmsgs, emsgs = self.load_config_file(IcalConfig.ICAL_AUTH_FILEKEY)
            self.warnmsgs.extend(wmsgs); self.errmsgs.extend(emsgs)

            # build merged_config...

            for icalentry in self._config[IcalConfig.ICAL_ICALCFG_FILEKEY].items:

                # lets see if there is matching q330 data by TAGNO
                q330entry = self._config[IcalConfig.ICAL_Q330CFG_FILEKEY].find(icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO])

                # get info from sensor cfgs if q330 exists. Need q330 for sensor names
                sens_a = self._config[IcalConfig.ICAL_SENSOR_FILEKEY]. \
                            find(q330entry.data[Q330.Q330_KEY_SENS_ROOTNAME_A]) if q330entry else None
                sens_b = self._config[IcalConfig.ICAL_SENSOR_FILEKEY]. \
                            find(q330entry.data[Q330.Q330_KEY_SENS_ROOTNAME_B]) if q330entry else None

                # lets check for auth recs
                authentry = self._config[IcalConfig.ICAL_AUTH_FILEKEY].find(icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO])

                wrapcfg = self.create_wrapper(icalentry, q330entry, authentry, sens_a, sens_b)
                self.merged_cfg.append(wrapcfg)

            self.merged_cfg.sort()
        
        return configresult(success, self.warnmsgs, self.errmsgs, [])


    def load_config_file(self, file_key=None):

        success = False
        errmsgs = []
        msgs = []

        if file_key in IcalConfig.ICALDB_FILE_STRUCT.keys():

            fpath = os.path.abspath(
                        os.sep.join([self._root_dir, 
                            IcalConfig.ICALDB_FILE_STRUCT[file_key]['path'], 
                            IcalConfig.ICALDB_FILE_STRUCT[file_key]['file']]))

            try:

                if file_key == IcalConfig.ICAL_SENSOR_FILEKEY:
                    self._config[IcalConfig.ICAL_SENSOR_FILEKEY] = Sensors(fpath)
                    success = self._config[IcalConfig.ICAL_SENSOR_FILEKEY].parsed_ok
                    msgs += self._config[IcalConfig.ICAL_SENSOR_FILEKEY].msgs

                elif file_key == IcalConfig.ICAL_CALIB_FILEKEY:
                    self._config[IcalConfig.ICAL_CALIB_FILEKEY] = Calibs(fpath)
                    success = self._config[IcalConfig.ICAL_CALIB_FILEKEY].parsed_ok
                    msgs += self._config[IcalConfig.ICAL_CALIB_FILEKEY].msgs

                elif file_key == IcalConfig.ICAL_AUTH_FILEKEY:
                    self._config[IcalConfig.ICAL_AUTH_FILEKEY] = Auths(fpath)
                    success = self._config[IcalConfig.ICAL_AUTH_FILEKEY].parsed_ok
                    msgs += self._config[IcalConfig.ICAL_AUTH_FILEKEY].msgs

                elif file_key == IcalConfig.ICAL_Q330CFG_FILEKEY:
                    self._config[IcalConfig.ICAL_Q330CFG_FILEKEY] = Q330s(fpath)
                    success = self._config[IcalConfig.ICAL_Q330CFG_FILEKEY].parsed_ok
                    msgs += self._config[IcalConfig.ICAL_Q330CFG_FILEKEY].msgs

                elif file_key == IcalConfig.ICAL_ICALCFG_FILEKEY:
                    self._config[IcalConfig.ICAL_ICALCFG_FILEKEY] = Icalcfgs(fpath)
                    success = self._config[IcalConfig.ICAL_ICALCFG_FILEKEY].parsed_ok
                    msgs += self._config[IcalConfig.ICAL_ICALCFG_FILEKEY].msgs

            except Exception as e:
                errmsgs.append('ERROR: Failure reading or parsing file [' + fpath + ']\n' + e.__str__())

            if not success:
                errmsgs.append('ERROR: Failure reading or parsing file [' + fpath + ']')

        else:
            errmsgs.append('ERROR: Invalid file_key: ' + file_key)

        return (success, msgs, errmsgs)


    def save_config(self):

        self.save_config_file(IcalConfig.ICAL_Q330CFG_FILEKEY)
        self.save_config_file(IcalConfig.ICAL_ICALCFG_FILEKEY)
        self.save_config_file(IcalConfig.ICAL_AUTH_FILEKEY)


    def save_config_file(self, file_key=None):

        success = False
        msgs = []

        if file_key in [IcalConfig.ICAL_Q330CFG_FILEKEY, 
                        IcalConfig.ICAL_AUTH_FILEKEY, 
                        IcalConfig.ICAL_ICALCFG_FILEKEY
                      ]:

            fpath = os.path.abspath(
                        os.sep.join([self._root_dir, 
                            IcalConfig.ICALDB_FILE_STRUCT[file_key]['path'], 
                            IcalConfig.ICALDB_FILE_STRUCT[file_key]['file']]))

            try:
                if self._config[file_key]:
                    success, msgs = self._config[file_key].write()
                else:
                    msgs.append('ERROR: Config data for ' + file_key + ' not in memory.')
            except Exception as e:
                msgs.append('ERROR: Error writing to ical.cfg to [' + fpath + ']\n' + str(e))

        return success, msgs


    def create_wrapper(self, icalentry, q330entry, authentry, sens_a_entry, sens_b_entry):

        tmpdict = {}
        # from ical.cfg
        tmpdict[WrapperCfg.WRAPPER_KEY_NET]       = icalentry.data[Icalcfg.ICALCFG_KEY_NET]
        tmpdict[WrapperCfg.WRAPPER_KEY_STA]       = icalentry.data[Icalcfg.ICALCFG_KEY_STA]
        tmpdict[WrapperCfg.WRAPPER_KEY_TAGNO]     = icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO]
        tmpdict[WrapperCfg.WRAPPER_KEY_DATAPORT]  = icalentry.data[Icalcfg.ICALCFG_KEY_DATAPORT]
        tmpdict[WrapperCfg.WRAPPER_KEY_MONPORT_A] = icalentry.data[Icalcfg.ICALCFG_KEY_MONPORT_A]
        tmpdict[WrapperCfg.WRAPPER_KEY_MONPORT_B] = icalentry.data[Icalcfg.ICALCFG_KEY_MONPORT_B]
        tmpdict[WrapperCfg.WRAPPER_KEY_LAST_LF_A] = icalentry.data[Icalcfg.ICALCFG_KEY_LAST_LF_A]
        tmpdict[WrapperCfg.WRAPPER_KEY_LAST_HF_A] = icalentry.data[Icalcfg.ICALCFG_KEY_LAST_HF_A]
        tmpdict[WrapperCfg.WRAPPER_KEY_LAST_LF_B] = icalentry.data[Icalcfg.ICALCFG_KEY_LAST_LF_B]
        tmpdict[WrapperCfg.WRAPPER_KEY_LAST_HF_B] = icalentry.data[Icalcfg.ICALCFG_KEY_LAST_HF_B]

        if q330entry:
            tmpdict[WrapperCfg.WRAPPER_KEY_IP] = q330entry.data[Q330.Q330_KEY_IP]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] = q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_A]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B] = q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_B]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A] = q330entry.data[Q330.Q330_KEY_SENS_ROOTNAME_A]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B] = q330entry.data[Q330.Q330_KEY_SENS_ROOTNAME_B]

            if sens_a_entry:
                tmpdict[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A] = sens_a_entry.data[Sensor.SENSOR_KEY_DESCR]

            if sens_b_entry:
                tmpdict[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B] = sens_b_entry.data[Sensor.SENSOR_KEY_DESCR]

        if authentry:
            tmpdict[WrapperCfg.WRAPPER_KEY_SN]       = authentry.data[Auth.AUTH_KEY_SN]
            tmpdict[WrapperCfg.WRAPPER_KEY_CFG_AUTH] = authentry.data[Auth.AUTH_KEY_CFG_AUTH]
            tmpdict[WrapperCfg.WRAPPER_KEY_SFN_AUTH] = authentry.data[Auth.AUTH_KEY_SFN_AUTH]
            tmpdict[WrapperCfg.WRAPPER_KEY_DP1_AUTH] = authentry.data[Auth.AUTH_KEY_DP1_AUTH]
            tmpdict[WrapperCfg.WRAPPER_KEY_DP2_AUTH] = authentry.data[Auth.AUTH_KEY_DP2_AUTH]
            tmpdict[WrapperCfg.WRAPPER_KEY_DP3_AUTH] = authentry.data[Auth.AUTH_KEY_DP3_AUTH]
            tmpdict[WrapperCfg.WRAPPER_KEY_DP4_AUTH] = authentry.data[Auth.AUTH_KEY_DP4_AUTH]

        wrapcfg = WrapperCfg(tmpdict)

        return wrapcfg


    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError
        elif key >= len(self.merged_cfg):
            raise IndexError
        else:
            return self.merged_cfg[key]      


    def __iter__(self):
        self.iter_ndx = 0
        return self


    def __next__(self):
        self.iter_ndx += 1
        if self.iter_ndx == len(self.merged_cfg):
            raise StopIteration
        return self.merged_cfg[self.iter_ndx - 1]


    def find(self, key):
        """Returns the first WrapperCfg with TAGNO
        If none is found, returns None.
        """
        return next(filter(lambda s: s.data[WrapperCfg.WRAPPER_KEY_TAGNO] == key, self.merged_cfg), None)

