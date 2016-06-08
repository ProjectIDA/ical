import os
import logging

from config.ical_config_reader import IcalConfigReader
from config.ical_config_writer import IcalConfigWriter
from config.icalcfg import Icalcfg, IcalcfgBadColumnCountExcept, IcalcfgMalformedRecordExcept

class Icalcfgs(IcalConfigReader, IcalConfigWriter):

    @classmethod
    def file_header(cls):
        return \
'''################################################################################################################
# ical.cfg
#
# Configuration file for the IDA ICAL calibration program.
#
# It contains values additional to those in the other qcal cfg files
# that are needed to run qcal in the wild at non-II stations.
#
# !!! DO NOT EDIT THIS FILE MANUALLY UNLESS YOU REALLY REALLY ARE SURE YOU KNOW WHAT YOU'RE DOING !!!
#
#############
# It contains 1 record per configured Q330, and has the following columns that are separated with 1+ spaces:
# 
#   NETWORK_CODE    : Network code. (alphanumeric string of length 2-10)
#   STATION_CODE    : Station code. (alphanumeric string of length 3-6)
#   TAGNO           : The Tag number of the Q330. (Positive integer)
#   DATA_PORT       : The Q330 Data Port to use for calibrations ([1-4])
#   MONITOR_CHAN_A  : The Q330 monitoring port for calibrations on sensor A (should be '0' if no sensor present, else [4-6])
#   MONITOR_CHAN_B  : The Q330 monitoring port for calibrations on sensor B (should be '0' if no sensor present, else [1-3])
#   LAST_CAL_A      : A timestamp indicating the previous  Low Frequency calibration of sensor A.
#   LAST_CAL_B      : A timestamp indicating the previous High Frequency calibration of sensor B.
#                     Above 4 timestamps are UTC in iso format: 'YYYY-MM-DDTHH:MM:SS.mmmmmm+00:00'.
#                     Should be 'none' until after first calibration or if sensor not installed
#   LOC_A           : Location code for sensor A.
#   LOC_B           : Location code for sensor B.
#   CHANNELS_A      : Channel codes, comma separated in vertical, nort, east order for sensor A.
#   CHANNELS_B      : Channel codes, comma separated in vertical, nort, east order for sensor B.
#
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
        self.items.clear()
        self.iter_ndx = 0


    def append(self, rec):
        rec = rec.strip()

        if not (rec.startswith('#') or (len(rec) == 0)):

            try:
                icalcfg = Icalcfg(rec)
            except IcalcfgBadColumnCountExcept:
                logging.warning('Ical.cfg record should have at least ' + str(Icalcfg.ICALCFG_COLCOUNT) + ' columns. [' + rec + ']. Record REMOVED.')
            except IcalcfgMalformedRecordExcept:
                logging.warning('Ical.cfg record appears to be invalid: [' + rec + ']. Record REMOVED.')
            except Exception as e:
                logging.warning('Unknown error parsing Ical.cfg record: [' + rec + ']. Record REMOVED.' + '\n' + str(e))
            else:
                if next(filter(lambda a: a == icalcfg, self.items), None) == None:
                    self.items.append(icalcfg)
                else:
                    logging.warning('Duplicate Ical.cfg record: [' + rec + ']. Record REMOVED.')


    def sort(self):
        self.items.sort()


    def find(self, key):
        """Returns the first Icalcfg with TAGNO
        If no Icalcfg is found, returns None.
        """
        return next(filter(lambda s: s.data[Icalcfg.ICALCFG_KEY_TAGNO] == key, self.items), None)


    def __setitem__(self, key, value):
        self.isdirty = True

    def __delitem__(self, key):
        self.isdirty = True

