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

import abc
import os

class IcalConfigWriter(metaclass=abc.ABCMeta):

    @classmethod
    def ensure_file(cls, fpath):

        if (type(fpath) == str) and \
            (len(fpath.strip()) > 0):
            absfpath = os.path.abspath(fpath)
            if not os.path.exists(absfpath):
                absdir = os.path.split(absfpath)[0]
                os.makedirs(absdir, exist_ok=True)

            return True

        else:
            return False


    @classmethod
    @abc.abstractmethod
    def file_header():
        pass


    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass


    @abc.abstractmethod
    def __delitem__(self, key):
        pass

