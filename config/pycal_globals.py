import sys
from os.path import expanduser, join

def get_root():
    return expanduser('~/PyCal')

def get_bin_root():
    if hasattr(sys, '_MEIPASS'):  # assuming running from .app bundle in MacOS folder
        return join(sys._MEIPASS, 'IDA/bin')
    else:
        return './bin' # for when running outside of .app bundle
 

def get_config_root():
    return join(get_root(), '.etc')

def get_initial_config_root():
    if hasattr(sys, '_MEIPASS'):  # assuming running from .app bundle in MacOS folder
        return join(sys._MEIPASS, 'etc')
    else:
        return './etc' # for when running outside of .app bundle

def get_results_root():
    return join(get_root(), 'Results')

def get_log_filename():
    return join(get_root(), 'pycal.log')

def get_nom_resp_filename(seismometer_model='sts2.5'):
    if (seismometer_model == 'sts2.5'):
        return 'nom_resp_sts2_5.ida'
    else:
        return ''