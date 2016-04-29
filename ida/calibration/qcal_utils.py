from collections import namedtuple
import logging
import os.path
import numpy as np
import obspy.core.stream
# import ida.response.paz

INPUT_CHANNELS = ['CCF', 'CCS']
INPUT_CHANNEL_WILDCARD = 'CC*'

QCalData = namedtuple('QCalData', ['north', 'east', 'vertical', 'input'])
QCalFiles = namedtuple('QCalFiles', ['ms_filename', 'log_filename'])


def read_qcal_files(qcal_ms_filename, qcal_log_filename):

    qcal_ms_filename = os.path.abspath(qcal_ms_filename)
    if not os.path.exists(qcal_ms_filename):
        msg = "QCal Miniseed file not found '{}'".format(qcal_ms_filename)
        logging.error(msg)
        raise Exception(msg)

    qcal_log_filename = os.path.abspath(qcal_log_filename)
    if not os.path.exists(qcal_log_filename):
        msg = "QCal Log file not found '{}'".format(qcal_log_filename)
        logging.error(msg)
        raise Exception(msg)

    cal_strm = obspy.core.stream.read(qcal_ms_filename, dtype=np.float64)

    if len(cal_strm) < 4:
        msg = "Fewer than 4 traces found in qcal miniseed file '{}'".format(qcal_ms_filename)
        logging.error(msg)
        raise Exception(msg)

    # check for cal signal channel INPUT_CHANNELS
    inp_strm = cal_strm.select(channel=INPUT_CHANNEL_WILDCARD)
    if len(inp_strm) != 1:
        msg = "Invalid number of input traces: {} found in qcal miniseed file '{}'".format(
            len(inp_strm),
            qcal_ms_filename
        )
        logging.error(msg)
        raise Exception(msg)

    log_info = read_qcal_log(qcal_log_filename)

    return cal_strm, log_info


def read_qcal_log(logfilename):
    """parse qcal v 2.1 log file"""

    LOG_KEY_INFO = [
        ('settling time', 'settling_time', 3),
        ('trailer time', 'trailing_time', 3)
        ]

    cal_log = {}
    logfilename = os.path.abspath(logfilename)

    if not os.path.exists(logfilename):
        msg = "File not found: '{}'".format(logfilename)
        logging.error(msg)
        raise Exception(msg)

    with open(logfilename, 'rt') as logfl:
        lines = logfl.readlines()

        for file_key, dict_key, val_pos in LOG_KEY_INFO:
            matches = [line.strip() for line in lines if line.find(file_key + ' =') > -1]
            if len(matches) != 1:
                raise Exception("Zero or multiple '{}' lines in qcal log file '{}'".format(file_key, logfilename))
            val = matches[0].split()[val_pos]
            cal_log[dict_key] = float(val)

    if len(cal_log) != len(LOG_KEY_INFO):
        raise Exception("Error parsing file: '{}'. Expected {} keys to be found".format(logfilename, len(LOG_KEY_INFO)))

    return cal_log


class QCalLog(object):

    def __init__(self, filename):
        self.filename = filename
        self.start_time = None
        self.waveform = None
        self.amplitude = None
        self.duration = None
        self.settling_time = None
        self.trailer_time = None
        self.calibrate_chans = None
        self.monitor_chans = None
        self.frequency_hz = None
        self.control_bitmap = None
        self.data_port = None


