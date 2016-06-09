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
"""PyCal configuration reader superclass"""

import abc
import os
import functools
import logging

class IcalConfigReader(metaclass=abc.ABCMeta):


    def __iter__(self):
        self.iter_ndx = 0
        return self


    def __next__(self):
        self.iter_ndx += 1
        if self.iter_ndx > len(self.items):
            raise StopIteration
        return self.items[self.iter_ndx - 1]


    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError
        elif key >= len(self.items):
            raise IndexError
        else:
            return self.items[key]      
        

    def __str__(self):
        return functools.reduce(lambda s1, s2: '\n'.join([s1, str(s2)]), self.items, '').strip()


    @classmethod
    def read_data_file(cls, fpath):

        success = False

        with open(fpath, 'r') as f:
            data = f.read()
            success = True

        if success:
            data = data.strip()
            records = data.splitlines()

        return (success, records)


    @classmethod
    def parse_cfg_file(cls, fpath, parser):

        msgs = []
        success = False

        if os.path.exists(fpath):
            success, recs = cls.read_data_file(fpath)
            parser(recs)
        else:
            logging.error('File does not exist: [' + os.path.abspath(fpath) + ']')

        return success


    @abc.abstractmethod
    def find(self, key):
        pass


    @abc.abstractmethod
    def clear(self):
        pass


    @abc.abstractmethod
    def append(self, rec):
        pass


    def parse_cfg_records(self, recs):

        self.clear()

        for lineno, rec in enumerate(recs):
            self.append(rec)

        self.sort()

