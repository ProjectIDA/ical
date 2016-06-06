from collections import namedtuple
from numpy import sqrt

"""Instrument properties and related application constants and structures"""

# making these match existing instrument abbreviations in DataScope ABBREV table
# only include seismometer models deployed by IDA on 2016-05-26, plus TR360
SEISTYPE_STS1E3 = 'STS1E3'
SEISTYPE_STS1HB = 'STS1HB'
SEISTYPE_STS1VB = 'STS1VB'
SEISTYPE_STS2 = 'STS2'
SEISTYPE_STS2_6 = 'sts2-6'
SEISTYPE_STS2_12 = 'sts2-12'
SEISTYPE_STS2_18 = 'sts2-18'
SEISTYPE_STS25 = 'STS2_5'
SEISTYPE_STS25F = 'STS2_5F'
SEISTYPE_STS5A = 'STS-5A'
SEISTYPE_TRILL = 'TRI_PH'
SEISTYPE_TR240 = 'TR240'
SEISTYPE_TR360 = 'TR360'
SEISTYPE_GS13 = 'GS13'
SEISTYPE_3ESPC = '3ESPC'
SEISTYPE_KS54000 = 'K54000'
SEISTYPE_CMG3T = 'CMG3T'
SEISTYPE_FBAEST = 'FBAEST'
SEISTYPE_FBA23 = 'FBA23'
SEISTYPE_M2166V = 'M2166V'
SEISTYPE_M2166H = 'M2166H'

DIGITYPE_Q330 = 'Q330HR'

SEISMOMETER_MODELS = [
    SEISTYPE_STS1E3,
    SEISTYPE_STS1HB,
    SEISTYPE_STS1VB,
    SEISTYPE_STS2,
    SEISTYPE_STS2_6,
    SEISTYPE_STS2_12,
    SEISTYPE_STS2_18,
    SEISTYPE_STS25,
    SEISTYPE_STS25F,
    SEISTYPE_STS5A,
    SEISTYPE_TRILL,
    SEISTYPE_TR240,
    SEISTYPE_TR360,
    SEISTYPE_GS13,
    SEISTYPE_3ESPC,
    SEISTYPE_KS54000,
    SEISTYPE_CMG3T,
    SEISTYPE_FBAEST,
    SEISTYPE_FBA23,
    SEISTYPE_M2166V,
    SEISTYPE_M2166H,
]

# only include currently supported triaxial list
# There are others. Need to define transforms
# as done with STS 2.5 below before adding addl seismometers
TRIAXIAL_SEIS_MODELS = [
    SEISTYPE_STS2,
    SEISTYPE_STS2_6,
    SEISTYPE_STS2_12,
    SEISTYPE_STS2_18,
    SEISTYPE_STS25,
    SEISTYPE_STS25F,
    # SEISTYPE_STS5A,
    # SEISTYPE_STS1HB,
    # SEISTYPE_TRILL,
    # SEISTYPE_TR240,
    # SEISTYPE_TR360
]

# need set of these transform for each supported triaxial sensor
STS2_5_XYZ2UVW = [
    [0,             -sqrt(6)/6,  sqrt(3)/6],
    [-sqrt(2)/4,  sqrt(6)/12, sqrt(3)/6],
    [ sqrt(2)/4,  sqrt(6)/12, sqrt(3)/6]
]
# from UVW back to ENZ, but ABS values, so all going in same direction at same time
STS2_5_UVW2ENZ_ABS = [
    [0,            sqrt(2)/2, sqrt(2)/2],
    [sqrt(6)/3, sqrt(6)/6, sqrt(6)/6],
    [sqrt(3)/3, sqrt(3)/3, sqrt(3)/3]
]

XFRM_TYPE_XYZ2UVW = 'XYZ2UVW'
XFRM_TYPE_UVW2ENZ_ABS = 'UVW2ENZ_ABS'

TRIAXIAL_TRANSFORMS = {
    SEISTYPE_STS25: {
        XFRM_TYPE_XYZ2UVW: STS2_5_XYZ2UVW,
        XFRM_TYPE_UVW2ENZ_ABS : STS2_5_UVW2ENZ_ABS
    },
    SEISTYPE_STS25F: {
        XFRM_TYPE_XYZ2UVW: STS2_5_XYZ2UVW,
        XFRM_TYPE_UVW2ENZ_ABS : STS2_5_UVW2ENZ_ABS
    },
}

CTBTO_SEIS_MODELS = [
    SEISTYPE_STS2_6,
    SEISTYPE_STS2_12,
    SEISTYPE_STS2_18,

    SEISTYPE_STS25,
    SEISTYPE_STS25F
]

SEIS_INVERT_CAL_CHAN = [SEISTYPE_GS13, SEISTYPE_TRILL]
SEIS_INVERT_NORTH_CHAN = [SEISTYPE_STS1E3, SEISTYPE_STS1HB]
SEIS_INVERT_EAST_CHAN = [SEISTYPE_STS1E3, SEISTYPE_STS1HB]

CALTYPE_RBHF = 'rbhf'
CALTYPE_RBLF = 'rblf'
CALIBRATION_TYPES = [CALTYPE_RBHF, CALTYPE_RBLF]

INSTRUMENT_NOMINAL_GAINS = {
    SEISTYPE_STS25: 1500,
    SEISTYPE_STS25F: 1500,
    DIGITYPE_Q330: 1.67e6
}

# obtained from IDA filter file q330.40 May 2016
Q330_40_FIR_COEFFS = [
 4.18952E-13, 3.30318E-04, 1.02921E-03,-3.14123E-03, 2.05709E-04, 1.52521E-03,-6.23193E-03, 1.04801E-02,-1.31202E-02,
 1.07821E-02,-1.44455E-03,-1.58729E-02, 3.95074E-02,-6.51036E-02, 8.53716E-02,-8.91913E-02, 5.00619E-02, 8.37233E-01,
 2.66723E-01,-1.66693E-01, 9.52840E-02,-5.09218E-02, 1.61458E-02, 7.06362E-03,-1.83877E-02, 1.99414E-02,-1.54895E-02,
 8.52735E-03,-2.55789E-03,-1.81103E-03, 2.42649E-03,-3.75769E-03, 4.67293E-04, 6.33072E-04,-1.56874E-06,-1.25480E-05,
 3.21041E-07,-2.63324E-08,-5.09997E-08
]

# obtained from IDA filter file q330.40 May 2016
Q330_40_FIR_FILTER_DELAY = 17.218

# obtained from IDA database. This value is specific to each Q330-Seis_Model combination
# and is in the IDA database as gcalib
Q330_GCALIB_FOR_SENSER = {
    SEISTYPE_STS25: .9911,  # value for Q330/STS2.5 combination
    SEISTYPE_STS25F: .9911,  # value for Q330/STS2.5 combination
}


# compute_response_fir(Q330_40_FIR_COEFFS,...)
# normalize_response() at 0Hz

# can be obtained by computing response of FIR filter in file q330.40
#   1) taking FFT of coefficients ==> Freq Resp
#   2) normalize on bin 0 (0 hz) value
#   3) Below is response amplitude value at 1Hz
Q330_40HZ_NOMINAL_FIR_GAIN_1HZ = 1.00666915769
Q330_NOMINAL_GAIN = INSTRUMENT_NOMINAL_GAINS[DIGITYPE_Q330]

ComponentsTpl = namedtuple('Components', ['north', 'east', 'vertical'])
