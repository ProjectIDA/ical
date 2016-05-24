import logging
import os

from config.wrapper_cfg import WrapperCfg
from config.sensors import Sensors
from config.sensor import Sensor
from config.calibs import Calibs
from config.auths import Auths
from config.auth import Auth
from config.q330s import Q330s
from config.q330 import Q330
from config.icalcfgs import Icalcfgs
from config.icalcfg import Icalcfg


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
            'path': os.sep.join(['.']),
            'file': 'ical.cfg'
        },
        ICAL_Q330CFG_FILEKEY: {
            'path': os.sep.join(['.']),
            'file': 'q330.cfg'
        },
        ICAL_AUTH_FILEKEY: {
            'path': os.sep.join(['.', 'q330']),
            'file': 'auth'
        },
        ICAL_LCQ_FILEKEY: {
            'path': os.sep.join(['.', 'q330']),
            'file': 'lcq'
        },
        ICAL_CALIB_FILEKEY: {
            'path': os.sep.join(['.', 'q330']),
            'file': 'calib'
        },
        ICAL_SENSOR_FILEKEY: {
            'path': os.sep.join(['.', 'q330']),
            'file': 'sensor'
        },
        ICAL_DETECTOR_FILEKEY: {
            'path': os.sep.join(['.', 'q330']),
            'file': 'detector'
        },
    }


    def __init__(self, cfg_dir='.'):

        self.root_dir = cfg_dir
        self.clear()
        logging.info('Reading ICAL configuration files from: ' + self.root_dir)


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


    def load(self):

        self.clear()

        # read sensor
        success = self.load_config_file(self.ICAL_SENSOR_FILEKEY)
        if not success:
            return False
        # read calib, will sensors complex names against calib records for matches
        success  = self.load_config_file(self.ICAL_CALIB_FILEKEY)
        if not success:
            return False
        # read ok so far, read q330
        success = self.load_config_file(self.ICAL_ICALCFG_FILEKEY)
        if not success:
            return False

        success = self.load_config_file(self.ICAL_Q330CFG_FILEKEY)
        if not success:
            return False

        success = self.load_config_file(self.ICAL_AUTH_FILEKEY)
        if not success:
            return False

        # everything lodaed ok... now check for data consistency
        # and build merged config objects adn wrappers
        for icalentry in self._config[self.ICAL_ICALCFG_FILEKEY].items:

            config_data_ok = True
            # lets see if there is matching q330 data by TAGNO
            q330entry = self._config[self.ICAL_Q330CFG_FILEKEY].find(icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO])
            if not q330entry:
                config_data_ok = False
                logging.error('No Q330 record found for TAGNO: ' + icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO])

            if config_data_ok:
                # get info from sensor cfgs if q330 exists. Need q330 for sensor names
                sens_a = self._config[self.ICAL_SENSOR_FILEKEY]. \
                            find(q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_A]) if q330entry else None
                sens_b = self._config[self.ICAL_SENSOR_FILEKEY]. \
                            find(q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_B]) if q330entry else None

                if not sens_a:
                    config_data_ok = False
                    logging.error('No SENSOR record found for: ' + q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_A])
                    
                if not sens_b:
                    config_data_ok = False
                    logging.error('No SENSOR record found for: ' + q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_B])

            # lets check for auth recs
            authentry = self._config[self.ICAL_AUTH_FILEKEY].find(icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO])
            if not authentry:
                config_data_ok = False
                logging.error('No AUTH record found for Q330 TAGNO: ' + icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO])

            if config_data_ok:
                wrapcfg = self.create_wrapper(icalentry, q330entry, authentry, sens_a, sens_b)
                self.merged_cfg.append(wrapcfg)

        self.merged_cfg.sort()

        # clear out ical, q300 and auth data so NO chance of confusion with merged_cfg data
        self._config[self.ICAL_ICALCFG_FILEKEY] = None
        self._config[self.ICAL_Q330CFG_FILEKEY] = None
        self._config[self.ICAL_AUTH_FILEKEY] = None
        
        # config loaded...
        return True


    def load_config_file(self, file_key=None):
        success = False

        if file_key in self.ICALDB_FILE_STRUCT.keys():

            fpath = os.path.abspath(
                        os.sep.join([self.root_dir, 
                            self.ICALDB_FILE_STRUCT[file_key]['path'], 
                            self.ICALDB_FILE_STRUCT[file_key]['file']]))

            try:

                if file_key == self.ICAL_SENSOR_FILEKEY:
                    if not os.path.exists(fpath):
                        raise Exception('SENSOR file missing: ' + fpath)
                    self._config[self.ICAL_SENSOR_FILEKEY] = Sensors(fpath)
                    success = self._config[self.ICAL_SENSOR_FILEKEY].parsed_ok

                elif file_key == self.ICAL_CALIB_FILEKEY:
                    if not os.path.exists(fpath):
                        raise Exception('CALIB file missing: ' + fpath)
                    self._config[self.ICAL_CALIB_FILEKEY] = Calibs(fpath)
                    success = self._config[self.ICAL_CALIB_FILEKEY].parsed_ok

                elif file_key == self.ICAL_AUTH_FILEKEY:
                    if not os.path.exists(fpath):
                        raise Exception('AUTH file missing: ' + fpath)
                    self._config[self.ICAL_AUTH_FILEKEY] = Auths(fpath)
                    success = self._config[self.ICAL_AUTH_FILEKEY].parsed_ok

                elif file_key == self.ICAL_Q330CFG_FILEKEY:
                    if not os.path.exists(fpath):
                        raise Exception('q330.cfg file missing: ' + fpath)
                    self._config[self.ICAL_Q330CFG_FILEKEY] = Q330s(fpath)
                    success = self._config[self.ICAL_Q330CFG_FILEKEY].parsed_ok

                elif file_key == self.ICAL_ICALCFG_FILEKEY:
                    if not os.path.exists(fpath):
                        raise Exception('ical.cfg file missing: ' + fpath)
                    self._config[self.ICAL_ICALCFG_FILEKEY] = Icalcfgs(fpath)
                    success = self._config[self.ICAL_ICALCFG_FILEKEY].parsed_ok

            except Exception as e:
                success = False
                logging.error('Failure reading or parsing file [' + fpath + ']\n' + e.__str__())

        else:
            logging.error('Invalid file_key: ' + file_key)

        return success


    def save(self):

        if self.merged_cfg:

            icalfpath = os.path.abspath(
                        os.sep.join([self.root_dir, 
                            self.ICALDB_FILE_STRUCT[self.ICAL_ICALCFG_FILEKEY]['path'], 
                            self.ICALDB_FILE_STRUCT[self.ICAL_ICALCFG_FILEKEY]['file']]))
            q330fpath = os.path.abspath(
                        os.sep.join([self.root_dir, 
                            self.ICALDB_FILE_STRUCT[self.ICAL_Q330CFG_FILEKEY]['path'], 
                            self.ICALDB_FILE_STRUCT[self.ICAL_Q330CFG_FILEKEY]['file']]))
            authfpath = os.path.abspath(
                        os.sep.join([self.root_dir, 
                            self.ICALDB_FILE_STRUCT[self.ICAL_AUTH_FILEKEY]['path'], 
                            self.ICALDB_FILE_STRUCT[self.ICAL_AUTH_FILEKEY]['file']]))

            with open(icalfpath, 'w') as ical_f, \
                    open(q330fpath, 'w') as q330_f, \
                    open(authfpath, 'w') as auth_f:

                ical_f.write(Icalcfgs.file_header())
                q330_f.write(Q330s.file_header())
                auth_f.write(Auths.file_header())

                for cfg in self.merged_cfg:
                    ical_f.write(cfg.ical_rec() + '\n')
                    q330_f.write(cfg.q330_rec() + '\n')
                    auth_f.write(cfg.auth_rec() + '\n')

                logging.info('ical.cfg, q330 and auth files saved.')


    def create_wrapper(self, icalentry, q330entry, authentry, sens_a_entry, sens_b_entry):

        tmpdict = {}
        # from ical.cfg
        tmpdict[WrapperCfg.WRAPPER_KEY_NET]       = icalentry.data[Icalcfg.ICALCFG_KEY_NET]
        tmpdict[WrapperCfg.WRAPPER_KEY_STA]       = icalentry.data[Icalcfg.ICALCFG_KEY_STA]
        tmpdict[WrapperCfg.WRAPPER_KEY_TAGNO]     = icalentry.data[Icalcfg.ICALCFG_KEY_TAGNO]
        tmpdict[WrapperCfg.WRAPPER_KEY_DATAPORT]  = icalentry.data[Icalcfg.ICALCFG_KEY_DATAPORT]
        tmpdict[WrapperCfg.WRAPPER_KEY_MONPORT_A] = icalentry.data[Icalcfg.ICALCFG_KEY_MONPORT_A]
        tmpdict[WrapperCfg.WRAPPER_KEY_MONPORT_B] = icalentry.data[Icalcfg.ICALCFG_KEY_MONPORT_B]
        tmpdict[WrapperCfg.WRAPPER_KEY_LAST_CAL_A] = icalentry.data[Icalcfg.ICALCFG_KEY_LAST_CAL_A]
        tmpdict[WrapperCfg.WRAPPER_KEY_LAST_CAL_B] = icalentry.data[Icalcfg.ICALCFG_KEY_LAST_CAL_B]
        tmpdict[WrapperCfg.WRAPPER_KEY_LOCATION_A] = icalentry.data[Icalcfg.ICALCFG_KEY_LOCATION_A]
        tmpdict[WrapperCfg.WRAPPER_KEY_LOCATION_B] = icalentry.data[Icalcfg.ICALCFG_KEY_LOCATION_B]
        tmpdict[WrapperCfg.WRAPPER_KEY_CHANNELS_A] = icalentry.data[Icalcfg.ICALCFG_KEY_CHANNELS_A]
        tmpdict[WrapperCfg.WRAPPER_KEY_CHANNELS_B] = icalentry.data[Icalcfg.ICALCFG_KEY_CHANNELS_B]

        if q330entry:
            tmpdict[WrapperCfg.WRAPPER_KEY_IP] = q330entry.data[Q330.Q330_KEY_IP]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] = q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_A]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B] = q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_B]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A] = q330entry.data[Q330.Q330_KEY_SENS_ROOTNAME_A]
            tmpdict[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B] = q330entry.data[Q330.Q330_KEY_SENS_ROOTNAME_B]

            if sens_a_entry:
                tmpdict[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A] = sens_a_entry.data[Sensor.SENSOR_KEY_DESCR]
            else:
                tmpdict[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A] = WrapperCfg.WRAPPER_SENSOR_UNK + ' (' + q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_A] + ')'

            if sens_b_entry:
                tmpdict[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B] = sens_b_entry.data[Sensor.SENSOR_KEY_DESCR]
            else:
                tmpdict[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B] = WrapperCfg.WRAPPER_SENSOR_UNK + ' (' + q330entry.data[Q330.Q330_KEY_SENS_COMPNAME_B] + ')'

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


    def append(self, new_cfg):

        try:
            wcfg = WrapperCfg(new_cfg)
            self.merged_cfg.append(wcfg)
            self.merged_cfg.sort()

            self.save()
            logging.info('Added configuration for Q330 Tag # {}'.format(new_cfg[WrapperCfg.WRAPPER_KEY_TAGNO]))

        except Exception as e:
            logging.error('Error adding configuration for Q330 Tag # {}: {}'.format(new_cfg[WrapperCfg.WRAPPER_KEY_TAGNO], str(e)))
            return False

        return True


    def remove(self, tagno):
        logging.info('Deleting configuration for Q330 Tag # {}'.format(tagno))

        wcfg = self.find(tagno)
        if wcfg != None:
            self.merged_cfg.remove(wcfg)
            self.save()
            logging.info('Deleted configuration for Q330 Tag # {}'.format(tagno))

        else:
            logging.error('Error deleting configuration. Tag # {} not found.'.format(tagno))


    def update(self, orig_tagno, new_cfg):
        origwcfg = self.find(orig_tagno)
        if origwcfg != None:
            origwcfg.update(new_cfg)
            self.merged_cfg.sort()

            self.save()
            logging.info('Updated configuration for Q330 Tag #: {}'.format(new_cfg[WrapperCfg.WRAPPER_KEY_TAGNO]))

            return True
        else:
            logging.error('Error updating configuration for Q330 Tag #: {}'.format(new_cfg[WrapperCfg.WRAPPER_KEY_TAGNO]))
            return False

    def sensor_list(self):
        return self._config[self.ICAL_SENSOR_FILEKEY].SensorModelList()


    def find_calib(self, calib_key):
        return self._config[self.ICAL_CALIB_FILEKEY].find(calib_key)


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
        if self.iter_ndx > len(self.merged_cfg):
            raise StopIteration
        return self.merged_cfg[self.iter_ndx - 1]


    def find(self, key):
        """Returns the first WrapperCfg with TAGNO
        If none is found, returns None.
        """
        return next(filter(lambda s: s.data[WrapperCfg.WRAPPER_KEY_TAGNO] == key, self.merged_cfg), None)

