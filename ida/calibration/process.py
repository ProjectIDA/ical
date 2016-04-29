import os.path
from datetime import datetime
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from obspy.signal.invsim import paz_to_freq_resp
# import ida.obspy_utils as op
# import ida.response.paz
# import ida.response.utils
import ida.calibration.qcal_utils
import ida.calibration.plots
from ida.calibration.cross import cross_correlate
import ida.signals.paz
import ida.signals.utils
import ida.seismometers
import ida.ctbto.messages
import logging


def process_qcal_data(sta, chancodes, loc, data_dir, lf_fnames, hf_fnames, seis_model, resp_fpath):

    logging.debug('Reading nominal response...')

    paz = ida.signals.paz.PAZ('vel', 'hz', pzfilename=resp_fpath, fileformat='ida')

    logging.debug('Reading nominal response complete.')

    logging.debug('Preparing cal data for coherence analysis...')
    # read, trim, transpose, invert and convolve input with response

    samp_rate_lf, lf_start_time, lfinput, lfeast, lfnorth, lfvert, \
    samp_rate_hf, hf_start_time, hfinput, hfeast, hfnorth, hfvert, \
    resp_lf, freqs_lf, \
    resp_hf, freqs_hf = prepare_cal_data(os.path.abspath(data_dir), lf_fnames, hf_fnames, seis_model, paz)

    logging.debug('Preparing cal data for coherence analysis complete.')

    logging.debug('Analyzing cal data and calculating new NORTH response...')

    n_paz = analyze_cal_component(data_dir, paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfnorth, hfnorth)
    n_paz = fit_component_north(paz)

    logging.debug('Analyzing cal data and calculating new NORTH response complete.')
    logging.debug('Analyzing cal data and calculating new EASTresponse...')

    e_paz = analyze_cal_component(data_dir, paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfeast, hfeast)
    e_paz = fit_component_east(paz)

    logging.debug('Analyzing cal data and calculating new EAST response complete.')
    logging.debug('Analyzing cal data and calculating new VERTICAL response...')

    v_paz = analyze_cal_component(data_dir, paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfvert, hfvert)
    v_paz = fit_component_vert(paz)

    logging.debug('Analyzing cal data and calculating new VERTICAL response complete.')

    # lets find "nice" number for resp length: i.e. a multiple of 20 * sample rate. So 0.05 and 1 hz in freqs exactly.
    resp_len = ((hfinput.size * 2) // (20 * samp_rate_hf)) * (20 * samp_rate_hf)

    logging.debug('Comparing NORTH response with Nominal...')
    freqs, nom_resp, n_resp, n_a0, n_adev, n_pdev, n_adev_max, n_pdev_max, \
    = compare_component_response(samp_rate_hf, resp_len, paz, n_paz, mode='vel')
    logging.debug('Comparing NORTH response with Nominal complete.')

    logging.debug('Comparing EAST response with Nominal...')
    freqs, nom_resp, e_resp, e_a0, e_adev, e_pdev, e_adev_max, e_pdev_max, \
    = compare_component_response(samp_rate_hf, resp_len, paz, e_paz, mode='vel')
    logging.debug('Comparing EAST response with Nominal complete.')

    logging.debug('Comparing VERTICAL response with Nominal...')
    freqs, nom_resp, v_resp, v_a0, v_adev, v_pdev, v_adev_max, v_pdev_max, \
    = compare_component_response(samp_rate_hf, resp_len, paz, v_paz, mode='vel')
    logging.debug('Comparing VERTICAL response with Nominal complete.')

    n_sys_sens = system_sensitivity_at_1hz(freqs, n_resp, seis_model)
    e_sys_sens = system_sensitivity_at_1hz(freqs, e_resp, seis_model)
    v_sys_sens = system_sensitivity_at_1hz(freqs, v_resp, seis_model)

    # convert cts/(m/s) to cts/m to nm/ct
    n_sys_sens = 1 / (n_sys_sens * (2 * np.pi * 1) / 1e9)
    e_sys_sens = 1 / (e_sys_sens * (2 * np.pi * 1) / 1e9)
    v_sys_sens = 1 / (v_sys_sens * (2 * np.pi * 1) / 1e9)

    north_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.north, calib=n_sys_sens, calper=1.0,
                                                             sample_rate=40.0,
                                                             in_spec=(n_adev_max <= 5.0) and (n_pdev_max <= 5),
                                                             paz=n_paz, A0=n_a0)


    east_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.east, calib=e_sys_sens, calper=1.0,
                                                        sample_rate=40.0,
                                                        in_spec=(e_adev_max <= 5.0) and (e_pdev_max <= 5), paz=e_paz,
                                                        A0=e_a0)
    vert_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.vertical, calib=v_sys_sens, calper=1.0,
                                                        sample_rate=40.0,
                                                        in_spec=(v_adev_max <= 5.0) and (v_pdev_max <= 5), paz=v_paz,
                                                        A0=v_a0)

    ida.calibration.plots.save_response_comparison_plots(sta, chancodes, loc,
                                                         data_dir, os.path.splitext(lf_fnames[0])[0],
                                                         seis_model,
                                                         lf_start_time, freqs, nom_resp,
                                                         n_resp, n_adev, n_pdev,
                                                         e_resp, e_adev, e_pdev,
                                                         v_resp, v_adev, v_pdev)

    cal_txt_fn = os.path.join(data_dir, os.path.splitext(lf_fnames[0])[0] + '_IMS20_MSG.txt')
    ims_msg = ida.ctbto.messages.calibration_result_msg(sta, loc, seis_model, hf_start_time,
                                                        [north_chan_result, east_chan_result, vert_chan_result],
                                                        filename=cal_txt_fn)
    # print(north_chan_result)
    # print(east_chan_result)
    # print(vert_chan_result)
    # print(ims_msg)

    return ims_msg


def system_sensitivity_at_1hz(freqs, resp, seis_model):

    # resp in velocity
    # freqs linear (maybe not necessary)
    # returns cts/(m/s)

    Q330_40HZ_NOMINAL_FIR_GAIN_1HZ = 1.00666915769  # from q330.40 fir filter used by IDA. Normed at freq = 0

    bin_ndx_1hz = int(np.ceil(1.0 / freqs[1])) # assumes [0] is 0
    resp_gain_1hz = abs(resp[bin_ndx_1hz])
    seis_nom_gain = ida.seismometers.INSTRUMENT_NOMINAL_GAINS[seis_model.upper()]
    q330_nom_gain_1hz = ida.seismometers.INSTRUMENT_NOMINAL_GAINS['Q330'] * Q330_40HZ_NOMINAL_FIR_GAIN_1HZ

    sys_sens = resp_gain_1hz * seis_nom_gain * q330_nom_gain_1hz

    # print('bin_ndx_1hz:{};  freq:{};   sens:{}'.format(bin_ndx_1hz, freqs[bin_ndx_1hz], abs(resp[bin_ndx_1hz])))
    return sys_sens



def analyze_cal_component(data_dir, nom_paz, lf_sr, hf_sr, lfinput, hfinput, lfmeas, hfmeas):

    # generate coherence info for each component
    # lfmeas_f, lfmeas_amp, lfmeas_pha, lfmeas_coh     = ida.calibration.cross.cross_correlate(lf_sr, lfinput, lfmeas)
    # hfmeas_f, hfmeas_amp, hfmeas_pha, hfmeas_coh     = ida.calibration.cross.cross_correlate(hf_sr, hfinput, hfmeas)

    #todo fitting code
    # pass PAZ and tf/coh info to fitting routine
    # receive new PAZ and TF for each channel
    # BLACK BOX END

    # DUMMY TESTING
    # revised PAZ for plot and IMS msg testing
    meas_paz  = fit_component_vert(nom_paz) #, lfmeas_f, lfmeas_amp, lfmeas_pha, lfmeas_coh, hfmeas_f, hfmeas_amp, hfmeas_pha, hfmeas_coh)

    #todo TF analysis,
    #todo MOVE THIS OUTSIDE
    #   check if < 5% amp and 5 deg pha for IN_SPEC flag for each component
    # f, nadev, npdev, eadev, epdev, vadev, vpdev = compare_responses(samp_rate_hf, resp_hf.size * 2,
    #                                                                 paz, north_paz, east_paz, vert_paz)

    #todo RESPONSE Plots (through 18HZ)
    #   AMP: LogLog: Nom + 3 components
    #   PHA: semilogx: Nom + 3 components
    #   save plots to png

    #todo Residual PLots
    #   AMP: +/- % residual for each with green band
    #   PHA: +/- deg residual for each comp with green band
    #   save plots to png

    #todo Construct CTBT results for IMS messaging

    #todo Save IMS text msg

    return meas_paz


def fit_component_east(paz): #, lfeast_f, lfeast_amp, lfeast_pha, lfeast_coh, hfeast_f, hfeast_amp, hfeast_pha, hfeast_coh):

    new_paz = ida.signals.paz.PAZ('vel', 'hz')
    new_paz._poles = paz._poles.copy()
    new_paz._zeros = paz._zeros.copy()
    new_paz._poles[2] -= complex(.05, 0)
    new_paz._poles[3] -= complex(.05, 0)

    return new_paz


def fit_component_north(paz): #, lfeast_f, lfeast_amp, lfeast_pha, lfeast_coh, hfeast_f, hfeast_amp, hfeast_pha, hfeast_coh):

    new_paz = ida.signals.paz.PAZ('vel', 'hz')
    new_paz._poles = paz._poles.copy()
    new_paz._zeros = paz._zeros.copy()

    return new_paz


def fit_component_vert(paz): #, lfeast_f, lfeast_amp, lfeast_pha, lfeast_coh, hfeast_f, hfeast_amp, hfeast_pha, hfeast_coh):

    new_paz = ida.signals.paz.PAZ('vel', 'hz')
    new_paz._poles = paz._poles.copy()
    new_paz._zeros = paz._zeros.copy()
    new_paz._poles[2] += complex(.1, 0)
    new_paz._poles[3] += complex(.1, 0)
    new_paz._poles[4] -= complex(.1, 0)
    new_paz._poles[5] -= complex(.1, 0)

    return new_paz


def compare_component_response(samp_rate, resp_len, nom_paz, meas_paz, mode='vel'):

    """
    :param mode:
    :type samp_rate: float sample rate in Hz
    :type resp_len: int
    :type nom_paz: ida.signals.paz.PAZ
    :type meas_paz: ida.signals.paz.PAZ
    :type mode: str
    """
    if (nom_paz == None):
        msg = 'You must supply a nominal PAZ to compare.'
        logging.error(msg)
        raise Exception(msg)

    if (meas_paz == None):
        msg = 'You must supply a measured component PAZ to compare.'
        logging.error(msg)
        raise Exception(msg)

    if isinstance(nom_paz, ida.signals.paz.PAZ):
        resp_tmp, freqs = paz_to_freq_resp(nom_paz.poles(units='hz'),
                                           nom_paz.zeros(mode=mode, units='hz'),
                                           nom_paz.h0,
                                           1.0 / samp_rate,
                                           resp_len,
                                           freq=True)
        nom_resp, _, nndx = ida.signals.utils.normalize(resp_tmp, freqs, 0.05)
    else:
        msg = 'nom_paz must be specified as an ida.signals.paz.PAZ object'
        logging.error(msg)
        raise Exception(msg)

    # generate response based on HF time series size
    if isinstance(meas_paz, ida.signals.paz.PAZ):
        resp_tmp, freqs = paz_to_freq_resp(meas_paz.poles(units='hz'),
                                           meas_paz.zeros(mode=mode, units='hz'),
                                           meas_paz.h0,
                                           1.0 / samp_rate,
                                           resp_len,
                                           freq=True)
        meas_resp, meas_scale, ndx = ida.signals.utils.normalize(resp_tmp, freqs, 0.05)
        meas_a0 = 1/meas_scale
        meas_a_dev = (np.divide(abs(meas_resp[1:]), abs(nom_resp[1:])) - 1.0) * 100.0
        meas_p_dev = np.subtract(np.angle(meas_resp[1:])*180/np.pi, np.angle(nom_resp[1:])*180/np.pi)

        meas_a_dev_max = abs(meas_a_dev).max()
        meas_p_dev_max = abs(meas_p_dev).max()
    else:
        msg = 'meas_paz must be specified as an ida.signals.paz.PAZ object'
        logging.error(msg)
        raise Exception(msg)



    return freqs, nom_resp, meas_resp, meas_a0, meas_a_dev, meas_p_dev, meas_a_dev_max, meas_p_dev_max


def prepare_cal_data(data_dir, lf_fnames, hf_fnames, seis_model, paz):

    ms_fpath_lf = os.path.join(data_dir, lf_fnames[0])
    log_fpath_lf = os.path.join(data_dir, lf_fnames[1])
    ms_fpath_hf = os.path.join(data_dir, hf_fnames[0])
    log_fpath_hf = os.path.join(data_dir, hf_fnames[1])

    logging.debug('Reading HF cal data...')
    strm_lf, log_lf = ida.calibration.qcal_utils.read_qcal_files(ms_fpath_lf, log_fpath_lf)
    logging.debug('Reading HF cal data complete.')
    logging.debug('Reading LF cal data... ')
    strm_hf, log_hf = ida.calibration.qcal_utils.read_qcal_files(ms_fpath_hf, log_fpath_hf)
    logging.debug('Reading LF cal data complete.')


    # trim settling and trailing times from traces
    logging.debug('Trimming and checking polarity of LF data...')
    ida.signals.utils.trim_stream(strm_lf, left=log_lf['settling_time'], right=log_lf['trailing_time'])
    # for those seismometers that are funky...
    ida.signals.utils.check_and_fix_polarities(strm_lf, seis_model)
    logging.debug('Trimming and checking polarity of LF data complete.')

    logging.debug('Trimming and checking polarity of HF data...')
    ida.signals.utils.trim_stream(strm_hf, left=log_hf['settling_time'], right=log_hf['trailing_time'])
    # for those seismometers that are funky...
    ida.signals.utils.check_and_fix_polarities(strm_hf, seis_model)
    logging.debug('Trimming and checking polarity of HF data complete.')


    # split cal data into enzi, 21zi (east, north, vert, input)
    trs_lf = split_cal_traces(strm_lf)
    trs_hf = split_cal_traces(strm_hf)

    samp_rate_lf = trs_lf.input.stats['sampling_rate']
    start_time_lf = trs_lf.input.stats['starttime']
    samp_rate_hf = trs_hf.input.stats['sampling_rate']
    start_time_hf = trs_lf.input.stats['starttime']
    npts_lf = trs_lf.input.stats['npts']
    # npts_lf = (npts_lf // 20 * samp_rate_lf) * (20 * samp_rate_lf)
    npts_hf = trs_hf.input.stats['npts']
    # npts_hf = (npts_hf // 400) * 400

    fraction = 0.1  # each side
    logging.debug('Creating tapers...')
    taper_lf = scipy.signal.tukey(npts_lf, alpha=fraction * 2, sym=True)
    taper_bin_cnt_lf = int(np.ceil(npts_lf * fraction))
    taper_hf = scipy.signal.tukey(npts_hf, alpha=fraction * 2, sym=True)
    taper_bin_cnt_hf = int(np.ceil(npts_hf * fraction))
    logging.debug('Creating tapers complete.')

    logging.debug('Generating nominal  LF (acc) response...')
    resp_tmp, freqs_lf = paz_to_freq_resp(paz.poles(units='hz'),
                                         paz.zeros(mode='acc', units='hz'),
                                         paz.h0,
                                         1.0 / samp_rate_lf,
                                         npts_lf,
                                         freq=True)

    resp_lf, scale, ndx = ida.signals.utils.normalize(resp_tmp, freqs_lf, 0.05)

    logging.debug('Generating nominal  HF (acc) response...')
    resp_tmp, freqs_hf = paz_to_freq_resp(paz.poles(units='hz'),
                                          paz.zeros(mode='acc', units='hz'),
                                          paz.h0,
                                          1.0 / samp_rate_hf,
                                          npts_hf,
                                          freq=True)


    resp_hf, scale, ndx = ida.signals.utils.normalize(resp_tmp, freqs_hf, 0.05)
    logging.debug('Generating nominal L/HF responses complete.')

    # prep input signal: taper, fft, conv resp, ifft
    logging.debug('Convolving LF input with nominal response...')
    input_fft           = np.fft.rfft(np.multiply(trs_lf.input.data, taper_lf))
    inp_freqs_cnv_resp  = np.multiply(input_fft, resp_lf)
    lf_inp_wth_resp     = np.fft.irfft(inp_freqs_cnv_resp, npts_lf)
    lf_inp_wth_resp     = lf_inp_wth_resp[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_inp_wth_resp.__itruediv__(lf_inp_wth_resp.std())
    lf_inp_wth_resp.__isub__(lf_inp_wth_resp.mean())
    logging.debug('Convolving LF input with nominal response complete')

    logging.debug('Convolving HF input with nominal response...')
    input_fft           = np.fft.rfft(np.multiply(trs_hf.input.data, taper_hf))
    inp_freqs_cnv_resp  = np.multiply(input_fft, resp_hf)
    hf_inp_wth_resp     = np.fft.irfft(inp_freqs_cnv_resp, npts_hf)
    hf_inp_wth_resp     = hf_inp_wth_resp[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_inp_wth_resp.__itruediv__(hf_inp_wth_resp.std())
    hf_inp_wth_resp.__isub__(hf_inp_wth_resp.mean())
    logging.debug('Convolving LF input with nominal response complete')

    logging.debug('Input signals ready for coherence analysis.')

    # prep output channels
    logging.debug('Preparing LF output for coherence analysis...')
    lf_out_eas = trs_lf.east.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_eas.__itruediv__(lf_out_eas.std())
    lf_out_eas.__isub__(lf_out_eas.mean())
    lf_out_nor = trs_lf.north.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_nor.__itruediv__(lf_out_nor.std())
    lf_out_nor.__isub__(lf_out_nor.mean())
    lf_out_ver = trs_lf.vertical.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_ver.__itruediv__(lf_out_ver.std())
    lf_out_ver.__isub__(lf_out_ver.mean())
    logging.debug('Preparing LF output for coherence analysis complete.')

    logging.debug('Preparing HF output for coherence analysis...')
    hf_out_eas = trs_hf.east.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_out_eas.__itruediv__(hf_out_eas.std())
    hf_out_eas.__isub__(hf_out_eas.mean())
    hf_out_nor = trs_hf.north.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_out_nor.__itruediv__(hf_out_nor.std())
    hf_out_nor.__isub__(hf_out_nor.mean())
    hf_out_ver = trs_hf.vertical.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_out_ver.__itruediv__(hf_out_ver.std())
    hf_out_ver.__isub__(hf_out_ver.mean())
    logging.debug('Preparing HF output for coherence analysis complete.')

    return samp_rate_lf, start_time_lf, lf_inp_wth_resp, lf_out_eas, lf_out_nor, lf_out_ver, \
           samp_rate_hf, start_time_hf, hf_inp_wth_resp, hf_out_eas, hf_out_nor, hf_out_ver, \
           resp_lf, freqs_lf, resp_hf, freqs_hf


def split_cal_traces(cal_strm):

    tr_e, tr_n, tr_z, tr_input = None, None, None, None

    for tr in cal_strm:
        comp = tr.stats.channel[2]
        if comp in ['S', 'F']:
            tr_input = tr.copy()
        elif comp in ['N', '1']:
            tr_n = tr.copy()
        elif comp in ['E', '2']:
            tr_e = tr.copy()
        elif comp in ['Z']:
            tr_z = tr.copy()

    if not tr_e:
        msg = 'Calibration stream missing east/west channel. Contains {}'.format([tr.stats.channel for tr in cal_strm])
        logging.error(msg)
        raise Exception(msg)
    if not tr_n:
        msg = 'Calibration stream missing north/south channel. Contains {}'.format([tr.stats.channel for tr in cal_strm])
        logging.error(msg)
        raise Exception(msg)
    if not tr_z:
        msg = 'Calibration stream missing vertical channel. Contains {}'.format([tr.stats.channel for tr in cal_strm])
        logging.error(msg)
        raise Exception(msg)
    if not tr_input:
        msg = 'Calibration stream missing cal input channel. Contains {}'.format([tr.stats.channel for tr in cal_strm])
        logging.error(msg)
        raise Exception(msg)

    cal_traces = ida.calibration.qcal_utils.QCalData(east=tr_e, north=tr_n, vertical=tr_z, input=tr_input)

    return cal_traces


def triaxial_horizontal_magnitudes(cal_tpl, seis_model):

    seis_model = seis_model.upper()
    if seis_model in ida.seismometers.TRIAXIAL_SEISMOMETER_MODELS:
        if seis_model == 'STS2.5':
            uvw = ida.signals.utils.channel_xform((cal_tpl.east, cal_tpl.north, cal_tpl.vertical), ida.seismometers.STS2_5_XYZ2UVW)
            enz = ida.signals.utils.channel_xform(uvw, ida.seismometers.STS2_5_UVW2ENZ_ABS)
            new_cal_tpl = ida.calibration.qcal_utils.QCalData(east=enz[0], north=enz[1], vertical=enz[2], input=cal_tpl.input)
            success = True
        else:
            msg = 'The Triaxial seismomemter model {} is not supported at this time.'.format(seis_model)
            logging.error(msg)
            raise Exception(msg)
    else:
        msg = 'The seismomemter model {} is not a triaxial instrument.'.format(seis_model)
        logging.error(msg)
        raise Exception(msg)

    return new_cal_tpl


