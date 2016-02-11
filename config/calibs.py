import os

from config.ical_config_reader import IcalConfigReader
from config.calib import Calib, CalibBadColumnCountExcept, CalibMalformedRecordExcept

class Calibs(IcalConfigReader):

    def __init__(self, fpath):
        self.fpath = fpath
        self.items = []
        self.iter_ndx = 0

        # read & parse data
        self.parsed_ok = super().parse_cfg_file(self.fpath, self.parse_cfg_records)


    def clear(self):
        self.items = []


    def append(self, rec):
        rec = rec.strip()

        if not (rec.startswith('#') or (len(rec) == 0)):

            try:
                calib = Calib(rec)
            except CalibBadColumnCountExcept:
                logging.warning('Calib record should have at least ' + str(Calib.CALIB_COLCOUNT) + ' columns. [' + rec + ']. Record ignored.')
            except CalibMalformedRecordExcept:
                logging.warning('Calib record appears to be invalid: [' + rec + ']. Record ignored.')
            except Exception as e:
                logging.warning('Unknown error parsing Calib record: [' + rec + ']. Record ignored.' + '\n' + str(e))
            else:
                if next(filter(lambda c: c == calib, self.items), None) == None:
                    self.items.append(calib)
                else:
                    logging.warning('Duplicate Calib record: [' + rec + ']. Record ignored.')


    def sort(self):
        self.items.sort()


    def find(self, compound_key):
        """Returns the first Calib where SENSOR_NAME + '|'+ CALTPYE == key.
        If no Calib is found, returns None.
        """
        keyparts = compound_key.split('|')
        if len(keyparts) != 2:
            return None
        else:
            return next(filter(
                lambda s: (s.data[Calib.CALIB_KEY_SENSNAME] == keyparts[0]) and 
                          (s.data[Calib.CALIB_KEY_CALTYPE] == keyparts[1]), 
                self.items), None)


