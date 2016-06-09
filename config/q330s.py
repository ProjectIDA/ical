#######################################################################################################################
# Copyright (C) 2016  Regents of the University of California
#
# This is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License (GNU GPL) as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# A copy of the GNU General Public License can be found in LICENSE.TXT in the root of the source code repository.
# Additionally, it can be found at http://www.gnu.org/licenses/.
#
# NOTES: Per GNU GPLv3 terms:
#   * This notice must be kept in this source file
#   * Changes to the source must be clearly noted with date & time of change
#
# If you use this software in a product, an explicit acknowledgment in the product documentation of the contribution
# by Project IDA, Institute of Geophysics and Planetary Physics, UCSD would be appreciated but is not required.
#######################################################################################################################
"""Class for in-memory representation of q330.cfg file"""

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
                q330 = Q330(rec)
            except Q330BadColumnCountExcept:
                logging.warning('q330.cfg record should have at least ' + str(Q330.Q330_COLCOUNT) + ' columns. [' + rec + ']. Record REMOVED.')
            except Q330MalformedRecordExcept:
                logging.warning('q330.cfg record appears to be invalid: [' + rec + ']. Record REMOVED.')
            except Exception as e:
                logging.warning('Unknown error parsing q330.cfg record: [' + rec + ']. Record REMOVED.' + str(e))
            else:
                if next(filter(lambda a: a == q330, self.items), None) == None:
                    self.items.append(q330)
                else:
                    logging.warning('Duplicate q330.cfg record: [' + rec + ']. Record REMOVED.')


    def sort(self):
        self.items.sort()


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


