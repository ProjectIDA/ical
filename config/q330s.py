import os

from config.ical_config_reader import IcalConfigReader
from config.ical_config_writer import IcalConfigWriter
from config.q330 import Q330, Q330BadColumnCountExcept, Q330MalformedRecordExcept

class Q330s(IcalConfigReader, IcalConfigWriter):

    @classmethod
    def file_header(cls):
        return \
'''#############################################################################
# The q330.cfg file describes system and sensor assignments and consists
# of 4 arguments:
#
#   1 - The /etc/hosts name of the digitizer.
#   2 - The digitizer property tag number
#   3 - Complex name describing sensor A input
#   4 - Complex name describing sensor B input
#
# The complex input names must exactly match the complex input names
# in the 'calib' configuration file.  These names consist of up to
# three ':' delimited strings in the form sensor[:e300[:x]] where only
# 'sensor' is required and must exactly match a name from the 'sensor'
# config file.
#
# For most sensors, the complex name will normally be just the name
# from the sensor file.  For the STS-1, if an E300 is present then the
# /etc/hosts name of the Digi which is connected to the E300 console
# should follow (eg, 'sts1:e300').  An optional third parameter can
# be specified for all sensors, if there is a need to differentiate
# between instruments with similiar control lines but different amplitude
# response.  No other significance is given to this argument... it is
# used solely for constructing unique complex names for the 'calib' table.
#
# For instance, an STS-1 with a SIB that has resistors on the calib
# input should be represented with the tag 'r' in the final field.  A
# high-gain STS-2 should be represented with the tag 'hi'.  Other tags
# can be assigned as desired.  Some examples:
#
# sts1:e300:r - STS-1 with an E330 and resistors in the SIB
# sts1::r     - STS-1 with old feedback boxes and resistors in the SIB
# sts2::hi    - high gain STS-2
#
#  Name      TagNo  Sensor A     Sensor B
#############################################################################

'''


    def __init__(self, fpath):
        self.fpath = fpath
        self.items = []
        self.iter_ndx = 0
        self.parsed_ok = False
        self.isdirty = False

        # if file doesn't exist, create it
        super().ensure_file(fpath)

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
                    q330 = Q330(rec)
                except Q330BadColumnCountExcept:
                    msgs.append('ERROR: q330.cfg record should have at least ' + str(Q330.SENSOR_COLCOUNT) + ' columns. [' + rec + ']. Record REMOVED.')
                except Q330MalformedRecordExcept:
                    msgs.append('ERROR: q330.cfg record appears to be invalid: [' + rec + ']. Record REMOVED.')
                except Exception as e:
                    msgs.append('ERROR: Unknown error parsing q330.cfg record: [' + rec + ']. Record REMOVED.' + str(e))
                else:
                    if next(filter(lambda a: a == q330, self.items), None) == None:
                        self.items.append(q330)
                    else:
                        msgs.append('WARN: Duplicate q330.cfg record: [' + rec + ']. Record REMOVED.')

        self.items.sort()

        return msgs


    def find(self, key):
        """Returns the first Q330 with TAGNO
        If no Q330 is found, returns None.
        """
        return next(filter(lambda s: s.data[Q330.Q330_KEY_TAGNO] == key, self.items), None)


    def __setitem__(self, key, value):
        self.isdirty = True
        pass


    def __delitem__(self, key):
        self.isdirty = True
        pass


