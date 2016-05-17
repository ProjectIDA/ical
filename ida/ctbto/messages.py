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

def ctbto_cal_messages(sta, loc, seis_model, cal_timestamp, channel_results, calresultfn=None, responsefn=None):

    cal_result_txt = calibration_result_msg(sta, loc, seis_model, cal_timestamp, channel_results, calresultfn)
    cal_response_txt = response_msg(sta, loc, seis_model, cal_timestamp, channel_results, responsefn)

    return cal_result_txt, cal_response_txt


def calibration_result_msg(sta, loc, seis_model, cal_timestamp, channel_results, calresultfn=None):

    ts_str = cal_timestamp.strftime('%Y/%m/%d %H:%M:%S')

    msg = "Below is the IMS 2.0 CALIBRATE_RESULT message \n" \
        "for the [{}] at station [{}] and location [{}] calibrated on [{} UTC].\n\n".format(
        seis_model,
        sta.upper(),
        loc,
        cal_timestamp.isoformat()) + \
        "\n========================================\nBEGIN IMS2.0\n\n" \
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
            "CALPER {}\n\n".format(sta, chn_res.channel, chn_res.in_spec, chn_res.calib, chn_res.calper)

    msg = msg + "STOP\n========================================\n\n"

    if calresultfn:
        with open(calresultfn, 'wt') as mfl:
            mfl.write(msg)


    return msg


def response_msg(sta, loc, seis_model, cal_timestamp, channel_results, responsefn=None):

    date_str = cal_timestamp.strftime('%Y/%m/%d')
    time_str = cal_timestamp.strftime('%H:%M')

    msg = "Below is the IMS 2.0 RESPONSE message \n" \
        "for the [{}] at station [{}] and location [{}] calibrated on [{} UTC].\n\n".format(
        seis_model,
        sta.upper(),
        loc,
        cal_timestamp.isoformat()) + \
        "\n========================================\nBEGIN IMS2.0\n\n" \
        "MSG_TYPE DATA\n" \
        "DATA_TYPE RESPONSE\n" \
        "MSG_ID <REPLACE WITH VALUE>\n" \
        "REF_ID <REPLACE WITH VALUE>"

    for ndx, chn_res in enumerate(channel_results):
        assert isinstance(chn_res, CTBTChannelResult)

        # CAL2 header record...
        msg = msg + '\n\n{:<4} {:<5} {:<3} {:<4} {:<6} {:15.8e} {:7.3f} {:11.5f} {:<10} {:<5}\n'.format(
            'CAL2',
            sta,
            chn_res.channel,
            loc,
            seis_model,
            chn_res.calib,
            chn_res.calper,
            chn_res.sample_rate,
            date_str,
            time_str)

        # PAZ2 header records...
        msg = msg + '{:<4} {:>2} {:1} {:15.8e} {:<4} {:<8.3f} {:>3d} {:>3d} {:<25}\n'.format('PAZ2',
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
            '({} Resp: Disp, Hz)'.format(chn_res.channel))

        # PAZ values - in displacement units and radians/sec
        poles = chn_res.paz.poles(units='hz')
        for pole in poles:
            msg = msg + '{:15.8e} {:15.8e}\n'.format(pole.real, pole.imag)

        zeros = chn_res.paz.zeros(mode='disp', units='hz')
        for zero in zeros:
            msg = msg + '{:15.8e} {:15.8e}\n'.format(zero.real, zero.imag)

    msg = msg + "\nSTOP\n========================================\n\n"

    if responsefn:
        with open(responsefn, 'wt') as mfl:
            mfl.write(msg)

    return msg