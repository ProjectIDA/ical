import os
from pathlib import Path
import shutil

SEP = os.sep

DB_file_struct = {
    'q330': {
        'path': SEP.join(['.', 'etc']),
        'file': 'q330.cfg'
    },
    'auth': {
        'path': SEP.join(['.', 'etc', 'q330']),
        'file': 'auth'
    },
    'lcq': {
        'path': SEP.join(['.', 'etc', 'q330']),
        'file': 'lcq'
    },
    'calib': {
        'path': SEP.join(['.', 'etc', 'q330']),
        'file': 'calib'
    },
    'sensor': {
        'path': SEP.join(['.', 'etc', 'q330']),
        'file': 'sensor'
    },
    'detector': {
        'path': SEP.join(['.', 'etc', 'q330']),
        'file': 'detector'
    },

}

class IcalFileKeyEmpty(Exception):
    """docstring for IcalFileKeyEmpty"""
    def __init__(self, message):
        super(IcalFileKeyEmpty, self).__init__(message)


class IcalFileKeyUnknown(Exception):
    """docstring for IcalFileKeyUnknown"""
    def __init__(self, message):
        super(IcalFileKeyUnknown, self).__init__(message)


class IcalFileNotFound(Exception):
    """docstring for IcalFileNotFound"""
    def __init__(self, message):
        super(IcalFileNotFound, self).__init__(message)



def read_file(dbpathloc='.', file_key=None):

    if (file_key == '') | (file_key == None ):
        raise IcalFileKeyEmpty('')

    if file_key not in DB_file_struct.keys():
        raise IcalFileKeyUnknown('')

    # Add path sep after dbpathloc cause don't know if passed dbpathlov value has trailing slash or not
    pathobj = Path(SEP.join([dbpathloc, DB_file_struct[file_key]['path'], DB_file_struct[file_key]['file']]))
    fpath = pathobj.__str__()
    print('fpath w/file:',fpath)
    if not Path(fpath).exists():
        raise IcalFileNotFound('')

    f = open(fpath)
    data = f.read()

    return data