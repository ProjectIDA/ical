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


def calibration_result_msg(sta, loc, seis_model, cal_timestamp, channel_results, filename=None):

    # msg_id = 'RB_CAL_' + sta + '_' + cal_timestamp.strftime('%Y-%m-%d')
    # ref_id = 'RB_CAL_' + sta + '_' + cal_timestamp.strftime('%Y-%m-%d')
    msg_id = 'VALUE'
    ref_id = 'VALUE'
    ts_str = cal_timestamp.strftime('%Y/%m/%d %H:%M:%S')

    msg = \
    "\n========================================\nBEGIN IMS2.0\n\n" \
    "MSG_TYPE command_response\n" \
    "MSG_ID {}\n" \
    "REF_ID {}\n" \
    "TIME_STAMP {}\n".format(msg_id, ref_id, ts_str)

    for ndx, chn_res in enumerate(channel_results):

        assert isinstance(chn_res, CTBTChannelResult)

        msg = msg + \
            "\nSTA_LIST {}\n" \
            "CHAN_LIST {}\n" \
            "CALIBRATE_RESULT\n" \
            "IN_SPEC {}\n" \
            "CALIB {:<15.8f}\n" \
            "CALPER {}\n\n".format(sta, chn_res.channel, chn_res.in_spec, chn_res.calib, chn_res.calper)

        msg = msg + response_msg(sta, loc, seis_model, cal_timestamp, chn_res)

    msg = msg + "STOP\n========================================\n\n"

    if filename:
        with open(filename, 'wt') as mfl:
            mfl.write(msg)

    return msg


def response_msg(sta, loc, seis_model, cal_timestamp, channel_result):

    assert isinstance(channel_result, CTBTChannelResult)

    # msg_id = 'RB_CAL_' + sta + '_' + cal_timestamp.strftime('%Y-%m-%d')
    msg_id = 'VALUE'
    date_str = cal_timestamp.strftime('%Y/%m/%d')
    time_str = cal_timestamp.strftime('%H:%M')

    # "BEGIN IMS2.0\n\n" \
    msg = \
        "MSG_TYPE DATA\n" \
        "DATA_TYPE RESPONSE\n" \
        "MSG_ID {}\n\n".format(msg_id)


    # CAL2 header record...
    msg = msg + '{:<4} {:<5} {:<3} {:<4} {:<6} {:15.8e} {:7.3f} {:11.5f} {:<10} {:<5}\n'.format(
                                            'CAL2',
                                             sta,
                                             channel_result.channel,
                                             '',
                                             seis_model,
                                             channel_result.calib,
                                             channel_result.calper,
                                             channel_result.sample_rate,
                                             date_str,
                                             time_str)
    # PAZ2 header records...
    msg = msg + '{:<4} {:>2} {:1} {:15.8e} {:<4} {:<8.3f} {:>3d} {:>3d} {:<25}\n'.format('PAZ2',
                                                                           1,
                                                                           'V',
                                                                           channel_result.A0 * \
                                                                                         ida.seismometers.INSTRUMENT_NOMINAL_GAINS[
                                                                                             seis_model.upper()] * \
                                                                                         ida.seismometers.INSTRUMENT_NOMINAL_GAINS[
                                                                                             'Q330'],
                                                                           '',
                                                                           0,
                                                                           channel_result.paz.num_poles,
                                                                           len(channel_result.paz.zeros(mode='disp', units='hz')),
                                                                           '({} Resp: Disp, Hz)'.format(channel_result.channel))

    # PAZ values - in displacement units and radians/sec
    poles = channel_result.paz.poles(units='hz')
    for pole in poles:
        msg = msg + '{:15.8e} {:15.8e}\n'.format(pole.real, pole.imag)

    zeros = channel_result.paz.zeros(mode='disp', units='hz')
    for zero in zeros:
        msg = msg + '{:15.8e} {:15.8e}\n'.format(zero.real, zero.imag)

    # msg = msg + 'STOP\n'
    msg = msg + '\n'

    return msg