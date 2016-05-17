import os.path
import numpy as np
import scipy.signal
from scipy.optimize import least_squares
import ida.calibration.qcal_utils
import ida.calibration.plots
from ida.calibration.cross import cross_correlate
import ida.signals.paz
import ida.signals.utils
import ida.seismometers
import ida.ctbto.messages
import logging


def process_qcal_data(sta, chancodes, loc, data_dir, lf_fnames, hf_fnames, seis_model, resp_fpath):

    logging.debug('Reading nominal response file: ' + resp_fpath)

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

    logging.debug('Analyzing cal data and calculating new NORTH response complete.')
    logging.debug('Analyzing cal data and calculating new EASTresponse...')

    e_paz = analyze_cal_component(data_dir, paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfeast, hfeast)

    logging.debug('Analyzing cal data and calculating new EAST response complete.')
    logging.debug('Analyzing cal data and calculating new VERTICAL response...')

    v_paz = analyze_cal_component(data_dir, paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfvert, hfvert)

    logging.debug('Analyzing cal data and calculating new VERTICAL response complete.')

    # lets find "nice" number for resp length: i.e. a multiple of 20 * sample rate. So 0.05 and 1 hz in freqs exactly.
    resp_len = ((hfinput.size * 2) // (20 * samp_rate_hf)) * (20 * samp_rate_hf)
    freqs = np.linspace(1e-3, samp_rate_hf/2, resp_len)

    logging.debug('Comparing NORTH response with Nominal...')

    nom_resp, n_resp, n_adev, n_pdev, n_adev_max, n_pdev_max, n_a0 = \
        compare_component_response(freqs, paz, n_paz, norm_freq=1.0, mode='vel')

    logging.debug('Comparing NORTH response with Nominal complete.')

    logging.debug('Comparing EAST response with Nominal...')
    nom_resp, e_resp, e_adev, e_pdev, e_adev_max, e_pdev_max, e_a0 = \
        compare_component_response(freqs, paz, e_paz, norm_freq=1.0, mode='vel')
    logging.debug('Comparing EAST response with Nominal complete.')

    logging.debug('Comparing VERTICAL response with Nominal...')
    nom_resp, v_resp, v_adev, v_pdev, v_adev_max, v_pdev_max, v_a0= \
        compare_component_response(freqs, paz, v_paz, norm_freq=1.0, mode='vel')
    logging.debug('Comparing VERTICAL response with Nominal complete.')

    n_sys_sens = system_sensitivity_at_1hz(freqs, n_resp, seis_model)
    e_sys_sens = system_sensitivity_at_1hz(freqs, e_resp, seis_model)
    v_sys_sens = system_sensitivity_at_1hz(freqs, v_resp, seis_model)

    # convert cts/(m/s) to cts/m to nm/ct
    n_sys_sens = 1 / (n_sys_sens * (2 * np.pi * 1) / 1e9)
    e_sys_sens = 1 / (e_sys_sens * (2 * np.pi * 1) / 1e9)
    v_sys_sens = 1 / (v_sys_sens * (2 * np.pi * 1) / 1e9)

    north_inspec = 'YES' if ((n_adev_max <= 5.0) and (n_pdev_max <= 5)) else 'NO'
    east_inspec = 'YES'  if ((e_adev_max <= 5.0) and (e_pdev_max <= 5)) else 'NO'
    vert_inspec = 'YES'  if ((v_adev_max <= 5.0) and (v_pdev_max <= 5)) else 'NO'

    north_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.north, calib=n_sys_sens, calper=1.0,
                                                             sample_rate=40.0,
                                                             in_spec=north_inspec, paz=n_paz, A0=n_a0)


    east_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.east, calib=e_sys_sens, calper=1.0,
                                                        sample_rate=40.0,
                                                        in_spec=east_inspec, paz=e_paz, A0=e_a0)
    vert_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.vertical, calib=v_sys_sens, calper=1.0,
                                                        sample_rate=40.0,
                                                        in_spec=vert_inspec, paz=v_paz, A0=v_a0)

    report_files_basename = os.path.splitext(lf_fnames[0])[0].replace('rblf-', '')

    amp_fn = os.path.join(data_dir, report_files_basename + '_AMP_Resp.png')
    pha_fn = os.path.join(data_dir, report_files_basename + '_PHA_Resp.png')
    ida.calibration.plots.save_response_comparison_plots(sta, chancodes, loc,
                                                         amp_fn, pha_fn,
                                                         seis_model,
                                                         lf_start_time, freqs, nom_resp,
                                                         n_resp, n_adev, n_pdev,
                                                         e_resp, e_adev, e_pdev,
                                                         v_resp, v_adev, v_pdev)

    ims_calres_txt_fn = os.path.join(data_dir, report_files_basename + '_CALRES_MSG.txt')
    ims_resp_txt_fn = os.path.join(data_dir, report_files_basename + '_RESP_MSG.txt')

    calres_msg, resp_msg = ida.ctbto.messages.ctbto_cal_messages(
        sta, loc, seis_model, hf_start_time,
        [north_chan_result, east_chan_result, vert_chan_result],
        calresultfn=ims_calres_txt_fn, responsefn=ims_resp_txt_fn)

    return ims_calres_txt_fn, ims_resp_txt_fn, amp_fn, pha_fn


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
    logging.debug('Cross_correlate for LF time series...')
    lfmeas_f, lfmeas_amp, lfmeas_pha, lfmeas_coh     = ida.calibration.cross.cross_correlate(lf_sr, lfinput, lfmeas)
    logging.debug('Cross_correlate for LF time series... complete.')
    hfmeas_f, hfmeas_amp, hfmeas_pha, hfmeas_coh     = ida.calibration.cross.cross_correlate(hf_sr, hfinput, hfmeas)

    lfmeas_pha_rad = lfmeas_pha * np.pi / 180
    hfmeas_pha_rad = hfmeas_pha * np.pi / 180

    # create complex TF
    hfmeas_tf = np.multiply(hfmeas_amp, (np.cos(hfmeas_pha_rad) + 1j * np.sin(hfmeas_pha_rad)))
    lfmeas_tf = np.multiply(lfmeas_amp, (np.cos(lfmeas_pha_rad) + 1j * np.sin(lfmeas_pha_rad)))

    # trim freqs and norm freqs
    lflo = 1e-04
    lfhi = 0.3
    hflo = 0.3
    hfhi = 18
    lf_norm_freq = 0.05
    hf_norm_freq = 1.0

    lf_range = np.logical_and(lfmeas_f <= lfhi, lfmeas_f > lflo)
    hf_range = np.logical_and(hfmeas_f <= hfhi, hfmeas_f > hflo)
    lfmeas_f_t = lfmeas_f[lf_range]
    hfmeas_f_t = hfmeas_f[hf_range]
    lfmeas_tf = lfmeas_tf[lf_range]
    hfmeas_tf = hfmeas_tf[hf_range]

    hfmeas_tf_norm, _, _ = ida.signals.utils.normalize(hfmeas_tf, hfmeas_f_t, hf_norm_freq)
    lfmeas_tf_norm, _, _ = ida.signals.utils.normalize(lfmeas_tf, lfmeas_f_t, lf_norm_freq)

    hf_paz_pert_map = ([4, 5], [2, 3])  # for sts2.5 ONLY
    lf_paz_pert_map = ([0,1], [])

    hf_paz_pert = nom_paz.make_partial(hf_paz_pert_map, hf_norm_freq)
    lf_paz_pert = nom_paz.make_partial(lf_paz_pert_map, lf_norm_freq)

    hf_paz_pert_flat, hf_paz_pert_flags = ida.signals.utils.unpack_paz(hf_paz_pert,
                                                                       (list(range(0, hf_paz_pert.num_poles)),
                                                                        list(range(0, hf_paz_pert.num_zeros))))

    lf_paz_pert_flat, lf_paz_pert_flags = ida.signals.utils.unpack_paz(lf_paz_pert,
                                                                       (list(range(0, lf_paz_pert.num_poles)),
                                                                        list(range(0, lf_paz_pert.num_zeros))))

    hf_pazpert_lb = hf_paz_pert_flat - 0.5 * np.abs(hf_paz_pert_flat)
    hf_pazpert_ub = hf_paz_pert_flat + 0.5 * np.abs(hf_paz_pert_flat)
    lf_pazpert_lb = lf_paz_pert_flat - 0.5 * np.abs(lf_paz_pert_flat)
    lf_pazpert_ub = lf_paz_pert_flat + 0.5 * np.abs(lf_paz_pert_flat)

    # initial response of paz_pert over freq_band of interest
    hf_resp0 = ida.signals.utils.compute_response(hfmeas_f_t, hf_paz_pert)
    lf_resp0 = ida.signals.utils.compute_response(lfmeas_f_t, lf_paz_pert)

    def resp_cost(p, paz_partial_flags, freqs, normfreq, tf_target, resp_pert0):

        # pack up into PAZ instances
        paz_pert = ida.signals.utils.pack_paz(p, paz_partial_flags)

        # compute response across freqs band and normalize
        resp = ida.signals.utils.compute_response(freqs, paz_pert)
        resp_norm, scale, ndx = ida.signals.utils.normalize(resp, freqs, normfreq)

        # calc new TF
        new_tf = np.divide(resp_norm, resp_pert0)

        # compare new_tf with old TF, real to real and imag to imag
        resid = np.sqrt(np.power(new_tf.real - tf_target.real, 2) +
                        np.power(new_tf.imag - tf_target.imag, 2))
        return resid

    logging.info('Fitting new HF response...')

    hf_res = least_squares(resp_cost,
                           hf_paz_pert_flat,
                           bounds=(hf_pazpert_lb,
                                   hf_pazpert_ub),  # lb, ub for each parameter
                           method='trf',
                           jac='3-point',  # I think this matches MATLAB FiniteDifferenceType='central'
                           xtol=1e-6,
                           ftol=1e-4,
                           diff_step=0.001,
                           max_nfev=300,  # max number of function evaluations
                           # list addl args to fittung fun
                           args=(hf_paz_pert_flags,
                                 hfmeas_f_t,
                                 hf_norm_freq,
                                 hfmeas_tf_norm,
                                 hf_resp0
                                 ),
                        verbose=0)
    logging.info('HF fitting termination: ' + hf_res.message)

    logging.info('Fitting new LF response...')
    lf_res = least_squares(resp_cost,  # cost function
                           lf_paz_pert_flat,  # initial values
                           bounds=(lf_pazpert_lb,
                                   lf_pazpert_ub),  # lb, ub for each parameter
                           method='trf',
                           jac='3-point',  # I think this matches MATLAB FiniteDifferenceType='central'
                           xtol=1e-6,
                           ftol=1e-4,
                           diff_step=0.001,
                           max_nfev=300,  # max number of function evaluations
                           # list addl args to fittung fun
                           args=(lf_paz_pert_flags,
                                 lfmeas_f_t,
                                 lf_norm_freq,
                                 lfmeas_tf_norm,
                                 lf_resp0
                                 ),
                           verbose=0)
    logging.info('HF fitting termination: ' + lf_res.message)

    new_hf_paz_pert = ida.signals.utils.pack_paz(hf_res.x, hf_paz_pert_flags)
    new_lf_paz_pert = ida.signals.utils.pack_paz(lf_res.x, lf_paz_pert_flags)
    new_paz = nom_paz.copy()
    new_paz.merge_paz_partial(new_hf_paz_pert, hf_paz_pert_map, hf_norm_freq)
    new_paz.merge_paz_partial(new_lf_paz_pert, lf_paz_pert_map, hf_norm_freq)

    return new_paz


def compare_component_response(freqs, paz1, paz2, norm_freq=1.0, mode='vel'):

    if (paz1 == None):
        msg = 'You must supply a nominal PAZ to compare.'
        logging.error(msg)
        raise Exception(msg)

    if (paz2 == None):
        msg = 'You must supply a measured component PAZ to compare.'
        logging.error(msg)
        raise Exception(msg)

    resp1 = ida.signals.utils.compute_response(freqs, paz1, mode=mode)
    resp1_norm, scale, _ = ida.signals.utils.normalize(resp1, freqs, norm_freq)

    resp2 = ida.signals.utils.compute_response(freqs, paz2, mode=mode)
    resp2_norm, resp2_inv_a0, _ = ida.signals.utils.normalize(resp2, freqs, norm_freq)

    # calcualte percentage deviations
    resp2_a_dev = (np.divide(abs(resp2_norm[1:]), abs(resp1_norm[1:])) - 1.0) * 100.0
    resp2_p_dev = np.subtract(np.angle(resp2_norm[1:])*180/np.pi, np.angle(resp2_norm[1:])*180/np.pi)

    resp2_a_dev_max = abs(resp2_a_dev).max()
    resp2_p_dev_max = abs(resp2_p_dev).max()


    return resp1_norm, resp2_norm, resp2_a_dev, resp2_p_dev, resp2_a_dev_max, resp2_p_dev_max, 1/resp2_inv_a0


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
    trs_lf = ida.calibration.qcal_utils.split_qcal_traces(strm_lf)
    trs_hf = ida.calibration.qcal_utils.split_qcal_traces(strm_hf)

    trs_lf_xfrm = triaxial_horizontal_magnitudes(trs_lf, 'STS2.5')
    trs_hf_xfrm = triaxial_horizontal_magnitudes(trs_hf, 'STS2.5')

    samp_rate_lf = trs_lf_xfrm.input.sampling_rate
    start_time_lf = trs_lf_xfrm.input.starttime
    samp_rate_hf = trs_hf_xfrm.input.sampling_rate
    start_time_hf = trs_lf_xfrm.input.starttime
    npts_lf = trs_lf_xfrm.input.npts
    # npts_lf = (npts_lf // 20 * samp_rate_lf) * (20 * samp_rate_lf)
    npts_hf = trs_hf_xfrm.input.npts
    # npts_hf = (npts_hf // 400) * 400

    fraction = 0.1  # each side
    logging.debug('Creating tapers...')
    taper_lf = scipy.signal.tukey(npts_lf, alpha=fraction * 2, sym=True)
    taper_bin_cnt_lf = int(np.ceil(npts_lf * fraction))
    taper_hf = scipy.signal.tukey(npts_hf, alpha=fraction * 2, sym=True)
    taper_bin_cnt_hf = int(np.ceil(npts_hf * fraction))
    logging.debug('Creating tapers complete.')

    logging.debug('Generating nominal  LF (acc) response...')
    freqs_lf = np.linspace(1e-3, samp_rate_lf/2, npts_lf//2 + 1)  # count is to match behavior of np.fft.rfft below
    resp_tmp_lf = ida.signals.utils.compute_response(freqs_lf, paz, mode='acc')

    resp_lf, scale, ndx = ida.signals.utils.normalize(resp_tmp_lf, freqs_lf, 0.05)

    logging.debug('Generating nominal  HF (acc) response...')
    freqs_hf = np.linspace(1e-3, samp_rate_hf/2, npts_hf//2 + 1)  # count is to match behavior of np.fft.rfft below
    resp_tmp_hf = ida.signals.utils.compute_response(freqs_hf, paz, mode='acc')


    resp_hf, scale, ndx = ida.signals.utils.normalize(resp_tmp_hf, freqs_hf, 0.05)
    logging.debug('Generating nominal L/HF responses complete.')

    # prep input signal: taper, fft, conv resp, ifft
    logging.debug('Convolving LF input with nominal response...')
    input_fft           = np.fft.rfft(np.multiply(trs_lf_xfrm.input.data, taper_lf))
    inp_freqs_cnv_resp  = np.multiply(input_fft, resp_lf)
    lf_inp_wth_resp     = np.fft.irfft(inp_freqs_cnv_resp, npts_lf)
    lf_inp_wth_resp     = lf_inp_wth_resp[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    stddev = lf_inp_wth_resp.std()
    lf_inp_wth_resp.__itruediv__(stddev)
    mean = lf_inp_wth_resp.mean()
    lf_inp_wth_resp.__isub__(mean)
    logging.debug('Convolving LF input with nominal response complete')

    logging.debug('Convolving HF input with nominal response...')
    input_fft           = np.fft.rfft(np.multiply(trs_hf_xfrm.input.data, taper_hf))
    inp_freqs_cnv_resp  = np.multiply(input_fft, resp_hf)
    hf_inp_wth_resp     = np.fft.irfft(inp_freqs_cnv_resp, npts_hf)
    hf_inp_wth_resp     = hf_inp_wth_resp[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    stddev = hf_inp_wth_resp.std()
    hf_inp_wth_resp.__itruediv__(hf_inp_wth_resp.std())
    mean = hf_inp_wth_resp.mean()
    hf_inp_wth_resp.__isub__(hf_inp_wth_resp.mean())
    logging.debug('Convolving HF input with nominal response complete')

    logging.debug('Input signals ready for coherence analysis.')

    # prep output channels
    logging.debug('Preparing LF output for coherence analysis...')
    lf_out_eas = trs_lf_xfrm.east.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_eas.__itruediv__(lf_out_eas.std())
    lf_out_eas.__isub__(lf_out_eas.mean())
    lf_out_nor = trs_lf_xfrm.north.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_nor.__itruediv__(lf_out_nor.std())
    lf_out_nor.__isub__(lf_out_nor.mean())
    lf_out_ver = trs_lf_xfrm.vertical.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    stddev = lf_out_ver.std()
    lf_out_ver.__itruediv__(stddev)
    mean = lf_out_ver.mean()
    lf_out_ver.__isub__(mean)
    logging.debug('Preparing LF output for coherence analysis complete.')

    logging.debug('Preparing HF output for coherence analysis...')
    hf_out_eas = trs_hf_xfrm.east.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    stddev = hf_out_eas.std()
    hf_out_eas.__itruediv__(hf_out_eas.std())
    mean = hf_out_eas.mean()
    hf_out_eas.__isub__(hf_out_eas.mean())
    hf_out_nor = trs_hf_xfrm.north.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_out_nor.__itruediv__(hf_out_nor.std())
    hf_out_nor.__isub__(hf_out_nor.mean())
    hf_out_ver = trs_hf_xfrm.vertical.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    stddev = hf_out_ver.std()
    hf_out_ver.__itruediv__(hf_out_ver.std())
    mean = hf_out_ver.mean()
    hf_out_ver.__isub__(hf_out_ver.mean())
    logging.debug('Preparing HF output for coherence analysis complete.')

    return samp_rate_lf, start_time_lf, lf_inp_wth_resp, lf_out_eas, lf_out_nor, lf_out_ver, \
           samp_rate_hf, start_time_hf, hf_inp_wth_resp, hf_out_eas, hf_out_nor, hf_out_ver, \
           resp_lf, freqs_lf, resp_hf, freqs_hf


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


