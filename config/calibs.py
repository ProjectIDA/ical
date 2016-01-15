import os

from config.ical_config_reader import IcalConfigReader
from config.calib import Calib, CalibBadColumnCountExcept, CalibMalformedRecordExcept

class Calibs(IcalConfigReader):

    def __init__(self, fpath):
        self.fpath = fpath
        self.items = []
        self.iter_ndx = 0
        self.parsed_ok = False

        # read & parse data
        self.parsed_ok, self.msgs = super().parse_cfg_file(self.fpath, self.parse_cfg_records)

        if not self.parsed_ok:
            for m in msgs:
                print(m)


    def clear(self):
        self.items = []


    def parse_cfg_records(self, recs):

        msgs = []
        self.clear()

        for lineno, rec in enumerate(recs):

            rec = rec.strip()

            if not (rec.startswith('#') or (len(rec) == 0)):

                try:

                    calib = Calib(rec)

                except CalibBadColumnCountExcept:
                    msgs.append('ERROR: Calib record should have at least ' + str(Calib.SENSOR_COLCOUNT) + ' columns. [' + rec + ']. Record ignored.')
                except CalibMalformedRecordExcept:
                    msgs.append('ERROR: Calib record appears to be invalid: [' + rec + ']. Record ignored.')
                except Exception as e:
                    msgs.append('ERROR: Unknown error parsing Calib record: [' + rec + ']. Record ignored.' + '\n' + str(e))
                else:
                    if next(filter(lambda c: c == calib, self.items), None) == None:
                        self.items.append(calib)
                    else:
                        msgs.append('WARN: Duplicate Calib record: [' + rec + ']. Record ignored.')

        self.items.sort()

        return msgs


    def find(self, compound_key):
        """Returns the first Calib where SENSOR_NAME + '|'+ CALTPYE == key.
        If no Calib is found, returns None.
        """
        keyparts = re.split('|', key)
        if len(keyparts) != 2:
            return None
        else:
            return next(filter(
                lambda s: (s.data[Calib.CALIB_KEY_SENSNAME] == keyparts[0]) and 
                          (s.data[Calib.CALIB_KEY_CALTYPE] == keyparts[1]), 
                self.items), None)


