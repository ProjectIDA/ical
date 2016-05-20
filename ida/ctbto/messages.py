from collections import namedtuple
import datetime
import logging

import ida.seismometers

# CTBTSensorResult = namedtuple('CTBTSensorResult', [
#     'station',
#     'location',
#     'cal_timestamp',
#     'seis_model',
#     'north_res',
#     'east_res',
#     'vertical_res'])
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
        chn_res.A0 * \
        ida.seismometers.INSTRUMENT_NOMINAL_GAINS[
         seis_model.upper()] * \
        ida.seismometers.INSTRUMENT_NOMINAL_GAINS[
         'Q330'],
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