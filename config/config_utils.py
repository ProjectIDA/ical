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
"""Configuration utility functions"""
import sys
from os.path import expanduser, join, abspath, dirname

def get_root():
    return expanduser('~/PyCal')

def get_bin_root():
    if getattr(sys, 'frozen', False):  # assuming running from .app bundle in MacOS folder
        return join(sys._MEIPASS, 'IDA/bin')
    else:
        return './bin'  # for when running outside of .app bundle

def get_data_root():
    if getattr(sys, 'frozen', False):  # assuming running from .app bundle in MacOS folder
        return join(sys._MEIPASS, 'IDA/data')
    else:
        return './data'  # for when running outside of .app bundle


def get_config_root():
    return join(get_root(), '.etc')


def get_initial_config_root():
    if getattr(sys, 'frozen', False):  # assuming running from .app bundle in MacOS folder
        return join(sys._MEIPASS, 'etc')
    else:
        return './etc' # for when running outside of .app bundle

def get_results_root():
    return join(get_root(), 'Results')

def get_log_filename():
    return join(get_root(), 'pycal.log')

def user_guide_filename():
    return 'PyCal_User_Guide.pdf'

def get_user_guide_fullpath():
    return join(get_root(), user_guide_filename())