import os

from config.ical_config_reader import IcalConfigReader
from config.ical_config_writer import IcalConfigWriter
from config.auth import Auth, AuthBadColumnCountExcept, AuthMalformedRecordExcept

class Auths(IcalConfigReader, IcalConfigWriter):

    @classmethod
    def file_header(cls):
        return \
'''################################################################################################################
# etc/auth
# 
# Configuration file for the IDA qcal calibration program.
# It contains, by Tag Number, the Q330 internal serial number and auth codes needed to run calibrations.
#
# !!! DO NOT EDIT THIS FILE MANUALLY UNLESS YOU REALLY REALLY ARE SURE YOU KNOW WHAT YOU'RE DOING !!!
#
#############
#
# The auth file gives the serial numbers and authorization
# codes for each Q330.
#
# It consists of 8 arguments:
#
#  1 - KMI property tag number
#  2 - internal serial number
#  3 - authorization code for configuration port
#  4 - authorization code for special functions port
#  5 - authorization code for data port 1
#  6 - authorization code for data port 2
#  7 - authorization code for data port 3
#  8 - authorization code for data port 4
#
# TagNo  Serial Number     cfg   sfn   dp1   dp2   dp3   dp4
################################################################################################################
'''

    def __init__(self, fpath):
        self.fpath = fpath
        self.items = []
        self.iter_ndx = 0
        self.isdirty = False

        # if file doesn't exist, create it
        super().ensure_file(fpath)

        # read & parse data
        self.parsed_ok = super().parse_cfg_file(self.fpath, self.parse_cfg_records)


    def clear(self):
        self.items = []


    def append(self, rec):
        rec = rec.strip()

        if not (rec.startswith('#') or (len(rec) == 0)):

            try:
                auth = Auth(rec)
            except AuthBadColumnCountExcept:
                logging.warning('Auth record should have at least ' + str(Auth.AUTH_COLCOUNT) + ' columns. [' + rec + ']. Record ignored.')
            except AuthMalformedRecordExcept:
                logging.warning('Auth record appears to be invalid: [' + rec + ']. Record ignored.')
            except Exception as e:
                logging.warning('Unknown error parsing Auth record: [' + rec + ']. Record ignored.' + '\n' + str(e))
            else:
                if next(filter(lambda a: a == auth, self.items), None) == None:
                    self.items.append(auth)
                else:
                    logging.warning('Duplicate Auth record: [' + rec + ']. Record ignored.')


    def sort(self):
        self.items.sort()


    def find(self, key):
        """Returns the first Auth with TAGNO
        If no Auth is found, returns None.
        """
        return next(filter(lambda s: s.data[Auth.AUTH_KEY_TAGNO] == key, self.items), None)


    def __setitem__(self, key, value):
        self.isdirty = True
        pass


    def __delitem__(self, key):
        self.isdirty = True
        pass


