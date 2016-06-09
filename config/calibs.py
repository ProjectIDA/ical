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
"""Class for in-memory representation of qcal calib file"""

import logging
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


