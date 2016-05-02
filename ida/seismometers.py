from collections import namedtuple
import numpy as np

SEISMOMETER_MODELS = [
    'STS1',
    'STS2',
    'STS2.5',
    'STS2.5-F',
    'STS-5A',
    'TRILLIUM',
]
CALIBRATION_TYPES = ['rbhf', 'rblf']
TRIAXIAL_SEISMOMETER_MODELS = [
    'STS2',
    'STS2.5',
    'STS2.5-F',
    'STS-5A',
    'STS1HB',
    'TRILLIUM',
    'TR360',
    'TR240'
]

SEIS_INVERT_CAL_CHAN = ['GS13', 'TRIL']
SEIS_INVERT_NORTH_CHAN = ['STS1']
SEIS_INVERT_EAST_CHAN = ['STS1']

STS2_5_XYZ2UVW = [
    [0,             -np.sqrt(6)/6,  np.sqrt(3)/6],
    [-np.sqrt(2)/4,  np.sqrt(6)/12, np.sqrt(3)/6],
    [ np.sqrt(2)/4,  np.sqrt(6)/12, np.sqrt(3)/6]
]

STS2_5_UVW2ENZ_ABS = [
    [0,            np.sqrt(2)/2, np.sqrt(2)/2],
    [np.sqrt(6)/3, np.sqrt(6)/6, np.sqrt(6)/6],
    [np.sqrt(3)/3, np.sqrt(3)/3, np.sqrt(3)/3]
]

ChanCodesTpl = namedtuple('ChanCodes', ['north', 'east', 'vertical'])

INSTRUMENT_NOMINAL_GAINS = {
    'STS2.5': 1500,
    'STS2.5-F': 1500,
    'Q330': 1.67e6
}