import logging
import obspy.core.stream
import obspy.core.trace
from obspy.signal.invsim import paz_to_freq_resp
import scipy.signal
# import scipy.signal.ltisys
import numpy as np
import ida.calibration.qcal_utils
import ida.seismometers

TAPER_TYPES = [
    'tukey'
]

Q330_FIR_RESPONSE_AT_1HZ = 1.01

# def system

def check_and_fix_polarities(strm, seis_model):

    for tr in strm:
        if invert_signal(tr.stats.channel, seis_model):
            tr.data *= -1.0


def invert_signal(channel, seis_model):

    if len(channel) < 3:
        msg = "Invalid channel code '{}'".format(channel)
        logging.error(msg)
        raise Exception(msg)

    seis_model = seis_model.upper()
    component = channel[2].upper()

    invert = ((component in ['S', 'F']) and (seis_model in ida.seismometers.SEIS_INVERT_CAL_CHAN)) or \
             ((component in ['1', 'N']) and (seis_model in ida.seismometers.SEIS_INVERT_NORTH_CHAN)) or \
             ((component in ['2', 'E']) and (seis_model in ida.seismometers.SEIS_INVERT_EAST_CHAN))

    return invert


# def taper_trace(trace, taper_type, both_sides=True, fraction=0.1, remove=False):
#
#     if not isinstance(trace, obspy.core.trace.Trace):
#         msg = 'Invalid type for trace. Expected an ObsPy Trace object.'
#         logging.error(msg)
#         raise TypeError(msg)
#
#     if not isinstance(taper_type, str):
#         msg = 'Invalid value type for taper_type: taper_type must be a string.'
#         logging.error(msg)
#         raise TypeError(msg)
#
#     if taper_type == 'tukey':
#         taper = scipy.signal.tukey(trace.data.size, alpha=fraction*2, sym=both_sides)
#         taper_bin_cnt = trace.data.size * fraction
#     else:
#         msg = "Invalid Taper Type requested: '{}'. Valid values: {}".format(
#             taper_type,
#             TAPER_TYPES)
#         logging.error(msg)
#         raise ValueError(msg)
#
#     if not remove:
#         trace.data *= taper
#     else:
#         # will introduce NaN into trace data where taper == 0
#         trace.data /= taper
#
#     return taper_bin_cnt
#
#
def trim_stream(src_stream, left=0, right=0):

    for trace in src_stream:
        trace.trim(trace.stats.starttime + left, trace.stats.endtime - right)


def prepare_normalized_response(bin_cnt, samp_rate, paz, nom_freq):

    # read normative PAZ response and create FAP freq resp
    resp, resp_freqs = pz2fap(bin_cnt,
                             paz.poles('acc', 'rad'),
                             paz.zeros('acc', 'rad'),
                             1.0,
                             samp_rate)
    resp_freqs /= (2.0 * np.pi)
    resp_norm, scale, ndx = normalize(resp, resp_freqs, nom_freq)

    return resp_norm, resp_freqs


# def pz2fap(fft_len, poles, zeros, gain, sampling_freq):
#     """need to supply poles/zeros in rad/sec"""
#
#     resp, lin_freq_hz = paz_to_freq_resp(poles, zeros, gain, 1.0/sampling_freq, fft_len, freq=True)
#
#     # n = fft_len // 2
#     # b, a = scipy.signal.ltisys.zpk2tf(zeros, poles, gain)
#     # a has to be a list for the scipy.signal.freqs() call later but zpk2tf()
#     # strangely returns it as an integer.
#     # if not isinstance(a, np.ndarray) and a == 1.0:
#     #     a = [1.0]
#     # fy = 0.5 * sampling_freq
#     # start at zero to get zero for offset / DC of fft
#     # f = np.linspace(0, fy, n + 1)
#     # freq, resp = scipy.signal.freqs(b, a, f * 2 * np.pi)
#     #
#     # for r in nditer(resp, op_flags=['readwrite']):
#     #     r[...] = r.conjugate()
#
#     return resp, lin_freq_hz * 2 * np.pi


def normalize(freq_resp, freqs, norm_freq):

    normed = None
    # find the index in freqs of the frist freq >= nom_freq
    ndx = min([freq[0] for freq in enumerate(freqs) if freq[1] >= norm_freq])
    if not (ndx is None):
        scale = np.abs(freq_resp[ndx])
        normed = np.divide(freq_resp, scale)
    else:
        scale = 1.0

    return normed, scale, ndx



# def xyz2uvw(trace_tpl, xfrm=None):
#     # trace_tpl.plot()
#
#     # (X, Y, Z)
#
#     tr_X = trace_tpl[0]
#     tr_Y = trace_tpl[1]
#     tr_Z = trace_tpl[2]
#
#     stats = tr_X.stats.copy()
#
#     tr_u = obspy.core.Trace(
#         np.multiply(tr_X.data, xfrm[0][0]) + \
#         np.multiply(tr_Y.data, xfrm[0][1]) + \
#         np.multiply(tr_Z.data, xfrm[0][2])
#         )
#     tr_u.stats = stats.copy()
#     tr_u.stats['channel'] = tr_u.stats['channel'][0:2] + 'U'
#
#     tr_v = obspy.core.Trace(
#         np.multiply(tr_X.data, xfrm[1][0]) + \
#         np.multiply(tr_Y.data, xfrm[1][1]) + \
#         np.multiply(tr_Z.data, xfrm[1][2])
#     )
#     tr_v.stats = stats.copy()
#     tr_v.stats['channel'] = tr_v.stats['channel'][0:2] + 'V'
#
#     tr_w = obspy.core.Trace(
#         np.multiply(tr_X.data, xfrm[2][0]) + \
#         np.multiply(tr_Y.data, xfrm[2][1]) + \
#         np.multiply(tr_Z.data, xfrm[2][2])
#     )
#     tr_w.stats = stats.copy()
#     tr_w.stats['channel'] = tr_w.stats['channel'][0:2] + 'W'
#
#     # uvw_strm = obspy.core.stream.Stream(traces=[tr_u, tr_v, tr_w])
#     # tstart = obspy.core.UTCDateTime(tr_u.stats['starttime'] + 60*60)
#     # tend = obspy.core.UTCDateTime(tstart + 600)
#     # uvw_strm.slice(tstart, tend).plot()
#     #
#     uvw_trace_tpl = (tr_u, tr_v, tr_w)
#
#     return uvw_trace_tpl
#
# def uvw2enz(trace_tpl, xfrm=None):
#     # trace_tpl.plot()
#
#     # (U, V, W)
#
#     tr_U = trace_tpl[0]
#     tr_V = trace_tpl[1]
#     tr_W = trace_tpl[2]
#
#     stats = tr_U.stats.copy()
#
#     tr_E = obspy.core.Trace(
#         np.multiply(tr_U.data, xfrm[0][0]) + \
#         np.multiply(tr_V.data, xfrm[0][1]) + \
#         np.multiply(tr_W.data, xfrm[0][2])
#         )
#     tr_E.stats = stats.copy()
#     tr_E.stats['channel'] = tr_E.stats['channel'][0:2] + '2'
#
#     tr_N = obspy.core.Trace(
#         np.multiply(tr_U.data, xfrm[1][0]) + \
#         np.multiply(tr_V.data, xfrm[1][1]) + \
#         np.multiply(tr_W.data, xfrm[1][2])
#     )
#     tr_N.stats = stats.copy()
#     tr_N.stats['channel'] = tr_N.stats['channel'][0:2] + '1'
#
#     tr_Z = obspy.core.Trace(
#         np.multiply(tr_U.data, xfrm[2][0]) + \
#         np.multiply(tr_V.data, xfrm[2][1]) + \
#         np.multiply(tr_W.data, xfrm[2][2])
#     )
#     tr_Z.stats = stats.copy()
#     tr_Z.stats['channel'] = tr_Z.stats['channel'][0:2] + 'Z'
#
#     # strm = obspy.core.stream.Stream(traces=[tr_E, tr_N, tr_Z])
#     # tstart = obspy.core.UTCDateTime(tr_U.stats['starttime'] + 60*60)
#     # tend = obspy.core.UTCDateTime(tstart + 600)
#     # strm.slice(tstart, tend).plot()
#
#     enz_trace_tpl = (tr_E, tr_N, tr_Z)
#
#     return enz_trace_tpl

def channel_xform(trace_tpl, xfrm):

    #  traces and xfrms assumed to be ENZ (aka 21Z and XYZ for triaxial seis output) order
    stats = trace_tpl[0].stats.copy()

    tr_E = obspy.core.Trace(
        np.multiply(trace_tpl[0].data, xfrm[0][0]) + \
        np.multiply(trace_tpl[1].data, xfrm[0][1]) + \
        np.multiply(trace_tpl[2].data, xfrm[0][2])
    )
    tr_E.stats = stats.copy()
    tr_E.stats['channel'] = tr_E.stats['channel'][0:2] + '2'

    tr_N = obspy.core.Trace(
        np.multiply(trace_tpl[0].data, xfrm[1][0]) + \
        np.multiply(trace_tpl[1].data, xfrm[1][1]) + \
        np.multiply(trace_tpl[2].data, xfrm[1][2])
    )
    tr_N.stats = stats.copy()
    tr_N.stats['channel'] = tr_N.stats['channel'][0:2] + '1'

    tr_Z = obspy.core.Trace(
        np.multiply(trace_tpl[0].data, xfrm[2][0]) + \
        np.multiply(trace_tpl[1].data, xfrm[2][1]) + \
        np.multiply(trace_tpl[2].data, xfrm[2][2])
    )
    tr_Z.stats = stats.copy()
    tr_Z.stats['channel'] = tr_Z.stats['channel'][0:2] + 'Z'

    # if isinstance(trace_tpl, ida.calibration.qcal_utils.QCalData):
    #     output_trace_tpl = ida.calibration.qcal_utils.QCalData(east=tr_E, north=tr_N, vertical=tr_Z, input=trace_tpl.input.copy())
    # else:
    output_trace_tpl = (tr_E, tr_N, tr_Z)

    return output_trace_tpl

