# import os.path
import logging
# import numpy as np
# from scipy import signal
# from obspy.core import *
# import obspy.imaging
# import matplotlib.pyplot as plt
import ida.cal.qcal_utils as qcal
import ida.obspy_utils as op


def prepare_for_cross(seis_model, input_strm, output_strm, paz, cal_log):

    # invert qcal signals if needed
    for tr in input_strm + output_strm:
        if qcal.invert_signal(tr.stats.channel, seis_model):
            tr.data *= -1.0

    # trim settling and trailing times from traces
    op.trim(input_strm, left=cal_log['settling_time'], right=cal_log['trailing_time'])
    op.trim(output_strm, left=cal_log['settling_time'], right=cal_log['trailing_time'])

