import logging
import os.path
import sys
from numpy import pi, linspace, abs
import ida.calibration.plots
from ida.calibration.process import analyze_cal_component, \
    compare_component_response, \
    prepare_cal_data, \
    nominal_sys_sens_1hz
import ida.signals.paz
from ida.signals.utils import compute_response
import ida.ctbto.messages

"""Methods for performing CTBTO/Sandia specific calibration analysis and data processing"""

def process_qcal_data(sta, chancodes, loc, data_dir, lf_fnames, hf_fnames, seis_model, start_paz_fn, bl_paz_fn):
    """Main method for analyzing random binary calibration data for Sandia/CTBTO STS2.5 (w/Q330HR digi) sensors.
    It processes both low and high frequency frequency random binary data sets. Supplied timeseries files must
    contain all 3 components plus input cal signal.

    :param sta: Station code
    :type sta: str
    :param chancodes: ComponentsTpl tuple containing chan codes for each component.
    :type chancodes: ida.instruments.ComponentsTpl
    :param loc: Location code
    :type loc: str
    :param data_dir: Directory where miniseed and qcal log files are located
    :type data_dir: str
    :param lf_fnames: For Low frequency: (miniseed_filename, qcal_log_filemane)
    :type lf_fnames: (str, str)
    :param hf_fnames: For High frequency: (miniseed_filename, qcal_log_filemane)
    :type hf_fnames: (str, str)
    :param seis_model: Seismometer model key
    :type seis_model: str
    :param start_paz_fn: PAZ response
    :type start_paz_fn: PAZ
    :param bl_paz_fn: PAZ response
    :type bl_paz_fn: PAZ
    :return: Results: (IMS2.0_msg_filename, amp_plot_filename, pha_plot_filename)
    :rtype: (str, str, str)
    """

    logging.debug('Reading response files {} (start) and {} (baseline)'.format(start_paz_fn, bl_paz_fn))

    paz_start = ida.signals.paz.PAZ('vel', 'hz', pzfilename=start_paz_fn, fileformat='ida')
    paz_bl = ida.signals.paz.PAZ('vel', 'hz', pzfilename=bl_paz_fn, fileformat='ida')

    start_paz = paz_bl.copy()   # start fitting from this model
    bl_paz = paz_bl.copy()      # comparing fitting results with this model


    logging.debug('Reading responses complete.')

    logging.debug('Preparing cal data for coherence analysis...')
    # read, trim, transpose, invert and convolve input with response

    samp_rate_lf, lf_start_time, lfinput, lfeast, lfnorth, lfvert, \
    samp_rate_hf, hf_start_time, hfinput, hfeast, hfnorth, hfvert, \
    resp_lf, freqs_lf, \
    resp_hf, freqs_hf = prepare_cal_data(os.path.abspath(data_dir), lf_fnames, hf_fnames, seis_model, start_paz)

    logging.debug('Preparing cal data for coherence analysis complete.')
    logging.debug('Analyzing cal data and calculating new NORTH response...')

    n_paz = analyze_cal_component(start_paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfnorth, hfnorth, 'BH1')

    logging.debug('Analyzing cal data and calculating new NORTH response complete.')
    logging.debug('Analyzing cal data and calculating new EAST response...')

    e_paz = analyze_cal_component(start_paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfeast, hfeast, 'BH2')

    logging.debug('Analyzing cal data and calculating new EAST response complete.')
    logging.debug('Analyzing cal data and calculating new VERTICAL response...')

    v_paz = analyze_cal_component(start_paz, samp_rate_lf, samp_rate_hf, lfinput, hfinput, lfvert, hfvert, 'BHZ')

    logging.debug('Analyzing cal data and calculating new VERTICAL response complete.')

    # lets find "nice" number for resp length: i.e. a multiple of 20 * sample rate. So 0.05 and 1 hz in freqs exactly.
    operating_sample_rate = 40.0
    resp_len = ((hfinput.size * 2) // (20 * operating_sample_rate)) * (20 * operating_sample_rate)
    freqs = linspace(0, operating_sample_rate/2, resp_len+1)  # must start with 0hz
    # resp_len = ((hfinput.size * 2) // (20 * 20)) * (20 * 20)
    # freqs = linspace(0, 20, resp_len)  # must start with 0hz

    logging.debug('Comparing NORTH response with Nominal normed at 0.05...')

    bl_resp, n_resp, n_adev, n_pdev, n_adev_max, n_pdev_max = \
        compare_component_response(freqs, bl_paz, n_paz, norm_freq=0.05, mode='vel')

    logging.debug('Comparing NORTH response with Nominal complete.')
    logging.debug('Comparing EAST response with Nominal normed at 0.05...')

    bl_resp, e_resp, e_adev, e_pdev, e_adev_max, e_pdev_max = \
        compare_component_response(freqs, bl_paz, e_paz, norm_freq=0.05, mode='vel')

    logging.debug('Comparing EAST response nom_paz Nominal complete.')
    logging.debug('Comparing VERTICAL response with Nominal normed at 0.05...')

    bl_resp, v_resp, v_adev, v_pdev, v_adev_max, v_pdev_max = \
        compare_component_response(freqs, bl_paz, v_paz, norm_freq=0.05, mode='vel')

    logging.debug('Comparing VERTICAL response with Nominal complete.')
    logging.debug('Finding sensitivities @ 1hz...')

    # sens X_resp responses normed at 0.05hz, need to get resp at 1hz
    # find 1hz bin
    #todo: find the better way
    bin_1hz_ndx = min([freq[0] for freq in enumerate(freqs) if freq[1] >= 1.0])
    n_sys_sens = nominal_sys_sens_1hz(n_resp[bin_1hz_ndx], seis_model)
    e_sys_sens = nominal_sys_sens_1hz(e_resp[bin_1hz_ndx], seis_model)
    v_sys_sens = nominal_sys_sens_1hz(v_resp[bin_1hz_ndx], seis_model)

    # convert cts/(m/s) to cts/m to nm/ct
    n_sys_sens = 1 / (n_sys_sens * (2 * pi) / 1e9)
    e_sys_sens = 1 / (e_sys_sens * (2 * pi) / 1e9)
    v_sys_sens = 1 / (v_sys_sens * (2 * pi) / 1e9)

    logging.debug('Finding sensitivities @ 1hz... complete.')

    logging.debug('Finding A0 at 1hz...')
    resp_1hz = compute_response(1.0, v_paz)
    v_a0 = 1/abs(resp_1hz[0])
    resp_1hz = compute_response(1.0, n_paz)
    n_a0 = 1/abs(resp_1hz[0])
    resp_1hz = compute_response(1.0, e_paz)
    e_a0 = 1/abs(resp_1hz[0])
    logging.debug('Finding A0 at 1hz complete.')

    # logging.debug('Reprocessing with new response for snr analysis...')
    # # read, trim, transpose, invert and convolve input with response
    # samp_rate_lf, lf_start_time, lfinput, lfeast, lfnorth, lfvert, \
    # samp_rate_hf, hf_start_time, hfinput, hfeast, hfnorth, hfvert, \
    # resp_lf, freqs_lf, \
    # resp_hf, freqs_hf = prepare_cal_data(os.path.abspath(data_dir), lf_fnames, hf_fnames, seis_model, start_paz)
    # logging.debug('Reprocessing with new response for snr analysis complete.')

    logging.debug('Computing IN_SPEC status...')

    if ((n_adev_max <= 5.0) and (n_pdev_max <= 5)):
        north_inspec = 'YES'
    else:
        north_inspec = 'NO'
    if ((e_adev_max <= 5.0) and (e_pdev_max <= 5)):
        east_inspec = 'YES'
    else:
        east_inspec = 'NO'
    if ((v_adev_max <= 5.0) and (v_pdev_max <= 5)):
        vert_inspec = 'YES'
    else:
        vert_inspec = 'NO'

    logging.debug('Computing IN_SPEC status... complete')
    logging.debug('Creating result tuples...')

    north_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.north, calib=n_sys_sens, calper=1.0,
                                                             sample_rate=40.0,
                                                             in_spec=north_inspec, paz=n_paz, A0=n_a0)
    east_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.east, calib=e_sys_sens, calper=1.0,
                                                        sample_rate=40.0,
                                                        in_spec=east_inspec, paz=e_paz, A0=e_a0)
    vert_chan_result = ida.ctbto.messages.CTBTChannelResult(channel=chancodes.vertical, calib=v_sys_sens, calper=1.0,
                                                        sample_rate=40.0,
                                                        in_spec=vert_inspec, paz=v_paz, A0=v_a0)
    logging.debug('Creating result tuples... complete.')

    report_files_basename = os.path.splitext(lf_fnames[0])[0].replace('rblf-', '')

    logging.info('Generating Response plots...')
    amp_fn = os.path.join(data_dir, report_files_basename + '_AMP_Resp.png')
    pha_fn = os.path.join(data_dir, report_files_basename + '_PHA_Resp.png')

    ida.calibration.plots.save_response_comparison_plots(sta, chancodes, loc,
                                                         amp_fn, pha_fn,
                                                         seis_model,
                                                         lf_start_time, operating_sample_rate,
                                                         resp_len+1, 1.0,
                                                         bl_resp,
                                                         n_resp, n_adev, n_pdev,
                                                         e_resp, e_adev, e_pdev,
                                                         v_resp, v_adev, v_pdev)
    logging.info('Generating Response plots... complete.')

    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        dig2_msg_fn = os.path.abspath(os.path.join(bundle_dir, 'IDA', 'data', 'Q330_DIG2.txt'))
        fir2_msg_fn = os.path.abspath(os.path.join(bundle_dir, 'IDA', 'data', 'Q330_FIR2.txt'))
    else:
        # bundle_dir = os.path.dirname(os.path.abspath(__file__))
        dig2_msg_fn = os.path.abspath(os.path.join('.', 'data', 'Q330_DIG2.txt'))
        fir2_msg_fn = os.path.abspath(os.path.join('.', 'data', 'Q330_FIR2.txt'))

    ims_calres_txt_fn = os.path.join(data_dir, report_files_basename + '_CALRES_MSG.msgtxt')

    logging.info('Generating IMS 2.0 messages...')

    calres_msg = ida.ctbto.messages.calibration_result_msg(
        sta, loc, seis_model, hf_start_time,
        [north_chan_result, east_chan_result, vert_chan_result],
        dig2_msg_fn, fir2_msg_fn,
        msgfn=ims_calres_txt_fn)

    logging.debug(calres_msg)
    logging.info('Generating IMS 2.0 messages... complete.')

    return ims_calres_txt_fn, amp_fn, pha_fn



