from ida.instruments import *
from numpy import pi

"""Methods and structures supporting construction of CTBTO IMS 2.0 messages"""

# Structure holding individual channel calibration results needed for CALIBRATE_RESULT message type
CTBTChannelResult = namedtuple('CTBTChannelResult', [
    'channel',
    'calib',
    'calper',
    'sample_rate',
    'in_spec',
    'paz',
    'A0'
])

def calibration_result_msg(sta, loc, seis_model, cal_timestamp, channel_results, dig2_msg_fn=None, fir2_msg_fn=None, msgfn=None):
    """
    High level function used to create IMS2.0 calibration result message. This is a CALIBRATE_RESULT message for
    each channel in the channels_results list with embedded DATA_TYPE RESPONSE information for each channel.

    :param sta: Staiuon code (blank ok for ctbto)
    :type sta: str
    :param loc: Location code
    :type loc: str
    :param seis_model: Seismometer model key
    :type seis_model: str
    :param cal_timestamp: Timestamp of calibration
    :type cal_timestamp: timestamp
    :param channel_results: List of CTBTChannelResult tuples
    :type channel_results: [CTBTOChannelResult...]
    :param dig2_msg_fn: filename of preformatted IMS2.0 digitizer stage 2 response info
    :type dig2_msg_fn: str
    :param fir2_msg_fn: filename of preformatted IMS2.0 digitizer FIR filter stage 3 coefficients
    :type fir2_msg_fn: str
    :param msgfn: Filename of option file to write IMS message text to. (Optional)
    :type msgfn: str
    :return: IMS 2.0 Message text
    :rtype: str
    """

    ts_str = cal_timestamp.strftime('%Y/%m/%d %H:%M:%S')

    dig2_msg = ''
    if dig2_msg_fn:
        with open(dig2_msg_fn, 'rt') as ifl:
            dig2_msg = ifl.read()

    fir2_msg = ''
    if fir2_msg_fn:
        with open(fir2_msg_fn, 'rt') as ifl:
            fir2_msg = ifl.read()

    msg = "BEGIN IMS2.0\n\n" \
          "MSG_TYPE COMMAND_RESPONSE\n" \
          "MSG_ID <REPLACE WITH VALUE>\n" \
          "REF_ID <REPLACE WITH VALUE>\n" \
          "TIME_STAMP {}\n".format(ts_str)

    for ndx, chn_res in enumerate(channel_results):

        assert isinstance(chn_res, CTBTChannelResult)

        msg = msg + \
            "\nSTA_LIST {}\n" \
            "CHAN_LIST {}\n" \
            "CALIBRATE_RESULT\n" \
            "IN_SPEC {}\n" \
            "CALIB {:<15.8f}\n" \
            "CALPER {}\n".format(sta, chn_res.channel, chn_res.in_spec, chn_res.calib, chn_res.calper)

        msg = msg + _sensor_response_msg(sta, loc, seis_model, cal_timestamp, chn_res)

        msg = msg + dig2_msg + fir2_msg

    msg = msg + "\nSTOP\n\n"

    if msgfn:
        with open(msgfn, 'wt') as mfl:
            mfl.write(msg)

    return msg


def _sensor_response_msg(sta, loc, seis_model, cal_timestamp, chn_res):
    """
    Creates DATA_TYPE RESPONSE portion channel response for IMS 2.0 messages.
    Results need to be in radians and diplacement.

    :param sta: Station code
    :type sta: str
    :param loc: Location code
    :type loc: str
    :param seis_model: Seismometer model key
    :type seis_model: str
    :param cal_timestamp: Time of calibration
    :type cal_timestamp: timestamp
    :param chn_res: CTBTOChannelResult tuple with cal results info
    :type chn_res:
    :return: Message text
    :rtype: str
    """

    date_str = cal_timestamp.strftime('%Y/%m/%d')
    time_str = cal_timestamp.strftime('%H:%M')

    msg = "DATA_TYPE RESPONSE\n"

    # CAL2 header record...
    msg = msg + '{:<4} {:<5} {:<3} {:<4} {:<6} {:<15.8e} {:<7.3f} {:<11.5f} {:<10} {:<5}\n'.format(
        'CAL2',
        sta,
        chn_res.channel,
        loc,
        seis_model[:6],
        chn_res.calib,
        chn_res.calper,
        chn_res.sample_rate,
        date_str,
        time_str)

    # PAZ2 header records...
    msg = msg + '{:<4} {:<2} {:1} {:<15.8e} {:<4} {:<8.3f} {:<3d} {:<3d} {:<25}\n'.format(
        'PAZ2',
        1,
        'V',
        chn_res.A0 * INSTRUMENT_NOMINAL_GAINS[seis_model] * 2 * pi/ 1e9,
        '',
        0,
        chn_res.paz.num_poles,
        len(chn_res.paz.zeros(mode='disp', units='hz')),
        '{} {} Disp; Rad'.format(seis_model[:9], chn_res.channel))

    # PAZ values - in displacement units and radians/sec
    poles = chn_res.paz.poles(units='rad')
    for pole in poles:
        msg = msg + ' {:15.8e} {:15.8e}\n'.format(pole.real, pole.imag)

    zeros = chn_res.paz.zeros(mode='disp', units='rad')
    for zero in zeros:
        msg = msg + ' {:15.8e} {:15.8e}\n'.format(zero.real, zero.imag)


    return msg