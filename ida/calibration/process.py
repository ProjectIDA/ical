#######################################################################################################################
# Copyright (C) 2016  Regents of the University of California
#
# This is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License (GNU GPL) as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# A copy of the GNU General Public License can be found in LICENSE.TXT in the root of the source code repository.
# Additionally, it can be found at http://www.gnu.org/licenses/.
#
# NOTES: Per GNU GPLv3 terms:
#   * This notice must be kept in this source file
#   * Changes to the source must be clearly noted with date & time of change
#
# If you use this software in a product, an explicit acknowledgment in the product documentation of the contribution
# by Project IDA, Institute of Geophysics and Planetary Physics, UCSD would be appreciated but is not required.
#######################################################################################################################

import logging
import os.path
from numpy import ndarray, complex128, pi, ceil, sin, cos, angle, abs, linspace, multiply, \
    logical_and, less_equal, polyfit, polyval, \
    divide, subtract, median, concatenate
from numpy.fft import rfft, irfft
from scipy.signal import tukey
from scipy.optimize import least_squares
import ida.calibration.qcal_utils
from ida.calibration.cross import cross_correlate
import ida.signals.paz
import ida.signals.utils
from ida.instruments import *

"""utility functions for processing of IDA Random Binary calibration data"""

def nominal_sys_sens_1hz(sens_resp_at_1hz, seis_model):
    """Compute system sensitivity in velocity units at 1hz given sensor response (in vel), sensor model and
    assuming a Q330 digitizer. This calculation DOES NOT include absolute gcalib adjustment for sensor,
    but does account for digitizer FIR response at 1hz and sensor specific Q330 gcalib value.

    :param sens_resp_at_1hz: complex sensor response at 1hz (velovity units)
    :type sens_resp_at_1hz: complex128
    :param seis_model: seismometer model key
    :type seis_model: str
    :return: system sensitivity in cts/(m/s)
    :rtype: float
    """

    seis_model = seis_model.upper()

    resp_gain_at_nom_freq = abs(sens_resp_at_1hz)
    sens_nom_gain = INSTRUMENT_NOMINAL_GAINS[seis_model]
    digi_nom_gain_1hz = Q330_NOMINAL_GAIN * \
                        Q330_40HZ_NOMINAL_FIR_GAIN_1HZ * \
                        Q330_GCALIB_FOR_SEIS[seis_model]

    return resp_gain_at_nom_freq * sens_nom_gain * digi_nom_gain_1hz


def compare_component_response(freqs, paz1, paz2, norm_freq=0.05, mode='vel', phase_detrend=False):
    """Compute amp and pha response of paz1 against paz2.

    :param freqs: Frequencies at which to compare responses. phase_detrend assumes freqs go to Nyquist.
    :type freqs: ndarray
    :param paz1: First PAZ repsonse
    :type paz1: PAZ instance
    :param paz2: Second PAZ response
    :type paz2: PAZ instance
    :param norm_freq: Frequency at which to normalize the two responses
    :type norm_freq: float
    :param mode: Units to use when computing responses
    :type mode: str ['disp', 'vel', 'acc']
    :param phase_detrend: Boolean indicating whether to remove linear trend from phase. Assumes nyquist in freqs[-1]
    :type phase_detrend: Bool
    :return: Normalized responses of paz1,
         Normalized responses of paz2,
         Amplitude deviation of paz2 from paz1 in percent,
         Phase deviation of paz2 from paz1 in degrees,
         Absolute max Amplitutde deviation,
         Absolute max Phase deviation,
    :rtype: ndarray, ndarray, ndarray, ndarray, float, float, float
    """

    if (paz1 == None):
        msg = 'You must supply a nominal PAZ to compare.'
        logging.error(msg)
        raise Exception(msg)

    if (paz2 == None):
        msg = 'You must supply a measured component PAZ to compare.'
        logging.error(msg)
        raise Exception(msg)

    resp1 = ida.signals.utils.compute_response(freqs, paz1, mode=mode)
    resp1_norm, _, _ = ida.signals.utils.normalize_response(resp1, freqs, norm_freq)

    resp2 = ida.signals.utils.compute_response(freqs, paz2, mode=mode)
    resp2_norm, _, _ = ida.signals.utils.normalize_response(resp2, freqs, norm_freq)

    if phase_detrend:
        freq_range = less_equal(freqs, 0.9 * freqs[-1])  # 90% of nyquist

        lin_trend_coeff = polyfit(freqs[freq_range], angle(resp1_norm[freq_range]), 1)
        trend_vals = polyval(lin_trend_coeff, freqs)
        amp = abs(resp1_norm)
        pha = angle(resp1_norm) - trend_vals
        resp1_norm = amp * complex128(cos(pha) + 1j*sin(pha))

        lin_trend_coeff = polyfit(freqs[freq_range], angle(resp2_norm[freq_range]), 1)
        trend_vals = polyval(lin_trend_coeff, freqs)
        amp = abs(resp2_norm)
        pha = angle(resp2_norm) - trend_vals
        resp2_norm = amp * complex128(cos(pha) + 1j*sin(pha))


    # calculate percentage deviations
    resp2_a_dev = (divide(abs(resp2_norm[1:]), abs(resp1_norm[1:])) - 1.0) * 100.0
    resp2_p_dev = subtract(angle(resp2_norm[1:])*180/pi, angle(resp1_norm[1:])*180/pi)

    resp2_a_dev_max = abs(resp2_a_dev).max()
    resp2_p_dev_max = abs(resp2_p_dev).max()

    return resp1_norm, resp2_norm, resp2_a_dev, resp2_p_dev, resp2_a_dev_max, resp2_p_dev_max


def analyze_cal_component(full_paz, lf_paz_pert_map, hf_paz_pert_map,
                          lf_sr, hf_sr, operating_sr, lfinput, hfinput, lfmeas, hfmeas):
    """Analyze both high and low frequency calibration component timeseries output with calibration input
    using starting paz fitting_paz.

    Find improved PAZ fit to reduce transfer function based on fitting_paz between input/output time series using a least_squares minimization
    approach.

    :param full_paz: Full model response for fitting (note: may be different then resp used to convolve w/input)
    :type full_paz: PAZ
    :param lf_paz_pert_map: paz map of which LF poles/zeros to perturb for fitting
    :type ([], [])
    :param hf_paz_pert_map: paz map of which HF poles/zeros to perturb for fitting
    :type ([], [])
    :param lf_sr: Low frequency sampling rate
    :type lf_sr: float
    :param hf_sr: High frequency sampling rate
    :type hf_sr: float
    :param operating_sr: Operational Sampling rate of channels
    :type operating_sr: float
    :param lfinput: Low frequency calibration input signal timeseries
    :type lfinput: ndarray
    :param hfinput: High frequency calibration input signal timeseries
    :type hfinput: ndarray
    :param lfmeas: Low frequency measured component output timeseries
    :type lfmeas: ndarray
    :param hfmeas: High frequency measured component output timeseries
    :type hfmeas: ndarray
    :return: New PAZ with improved response fit
    :rtype: PAZ
    """

    # generate coherence info for each component
    logging.debug('Compute coherence for LF time series...')
    lfmeas_f, lfmeas_amp, lfmeas_pha, lfmeas_coh     = ida.calibration.cross.cross_correlate(lf_sr, lfinput, lfmeas)
    logging.debug('Compute coherence for LF time series... complete.')

    logging.debug('Compute coherence for HF time series...')
    hfmeas_f, hfmeas_amp, hfmeas_pha, hfmeas_coh     = ida.calibration.cross.cross_correlate(hf_sr, hfinput, hfmeas)
    logging.debug('Compute coherence for HF time series... complete.')

    lfmeas_pha_rad = lfmeas_pha * pi / 180
    hfmeas_pha_rad = hfmeas_pha * pi / 180

    # create complex TF
    hfmeas_tf = multiply(hfmeas_amp, (cos(hfmeas_pha_rad) + 1j * sin(hfmeas_pha_rad)))
    lfmeas_tf = multiply(lfmeas_amp, (cos(lfmeas_pha_rad) + 1j * sin(lfmeas_pha_rad)))

    # trim freqs and norm freqs
    lflo = 1e-04
    lfhi = 0.3
    hflo = 0.3
    hfhi = operating_sr * 0.45  # e.g. 18hz for 40hz channels
    lf_norm_freq = 0.05
    hf_norm_freq = 1.0

    lf_range = logical_and(lfmeas_f <= lfhi, lfmeas_f > lflo)
    hf_range = logical_and(hfmeas_f <= hfhi, hfmeas_f > hflo)
    lfmeas_f_t = lfmeas_f[lf_range]
    hfmeas_f_t = hfmeas_f[hf_range]
    lfmeas_tf = lfmeas_tf[lf_range]
    hfmeas_tf = hfmeas_tf[hf_range]
    lfmeas_coh = lfmeas_coh[lf_range]
    hfmeas_coh = hfmeas_coh[hf_range]

    logging.debug('LF TF Amp Max:' + str(abs(lfmeas_tf).max()))
    logging.debug('LF TF Amp Min:' + str(abs(lfmeas_tf).min()))
    logging.debug('LF TF Pha Max:' + str(angle(lfmeas_tf).max()))
    logging.debug('LF TF Pha Min:' + str(angle(lfmeas_tf).min()))
    logging.debug('HF TF Amp Max:' + str(abs(hfmeas_tf).max()))
    logging.debug('HF TF Amp Min:' + str(abs(hfmeas_tf).min()))
    logging.debug('HF TF Pha Max:' + str(angle(hfmeas_tf).max()))
    logging.debug('HF TF Pha Min:' + str(angle(hfmeas_tf).min()))

    hfmeas_tf_norm, _, _ = ida.signals.utils.normalize_response(hfmeas_tf, hfmeas_f_t, hf_norm_freq)
    lfmeas_tf_norm, _, _ = ida.signals.utils.normalize_response(lfmeas_tf, lfmeas_f_t, lf_norm_freq)

    logging.debug('LF TF Amp Max (normed):' + str(abs(lfmeas_tf_norm).max()))
    logging.debug('LF TF Amp Min (normed):' + str(abs(lfmeas_tf_norm).min()))
    logging.debug('LF TF Pha Max (normed):' + str(angle(lfmeas_tf_norm).max()))
    logging.debug('LF TF Pha Min (normed):' + str(angle(lfmeas_tf_norm).min()))
    logging.debug('HF TF Amp Max (normed):' + str(abs(hfmeas_tf_norm).max()))
    logging.debug('HF TF Amp Min (normed):' + str(abs(hfmeas_tf_norm).min()))
    logging.debug('HF TF Pha Max (normed):' + str(angle(hfmeas_tf_norm).max()))
    logging.debug('HF TF Pha Min (normed):' + str(angle(hfmeas_tf_norm).min()))

    logging.debug('LF Coh2 Median:' + str(median(lfmeas_coh)))
    logging.debug('HF Coh2 Median:' + str(median(hfmeas_coh)))

    #TODO need to move this to be sensor dependent in instruments.py
    # for sts2.5 ONLY
    logging.debug('Setting paz perturbation map and splitting...')
    hf_paz_pert = full_paz.make_partial(hf_paz_pert_map, hf_norm_freq)
    lf_paz_pert = full_paz.make_partial(lf_paz_pert_map, lf_norm_freq)

    logging.debug('Computing response of perturbed paz...')
    # initial response of paz_pert over freq_band of interest
    hf_resp0 = ida.signals.utils.compute_response(hfmeas_f_t, hf_paz_pert)
    lf_resp0 = ida.signals.utils.compute_response(lfmeas_f_t, lf_paz_pert)
    logging.debug('Computing response of perturbed paz... complete.')

    logging.debug('Setting paz perturbation map and splitting... complete.')
    hf_paz_pert_flat, hf_paz_pert_flags = ida.signals.utils.unpack_paz(hf_paz_pert,
                                                                       (list(range(0, hf_paz_pert.num_poles)),
                                                                        list(range(0, hf_paz_pert.num_zeros))))

    lf_paz_pert_flat, lf_paz_pert_flags = ida.signals.utils.unpack_paz(lf_paz_pert,
                                                                       (list(range(0, lf_paz_pert.num_poles)),
                                                                        list(range(0, lf_paz_pert.num_zeros))))

    hf_pazpert_lb = hf_paz_pert_flat - 0.5 * abs(hf_paz_pert_flat)
    hf_pazpert_ub = hf_paz_pert_flat + 0.5 * abs(hf_paz_pert_flat)
    lf_pazpert_lb = lf_paz_pert_flat - 0.5 * abs(lf_paz_pert_flat)
    lf_pazpert_ub = lf_paz_pert_flat + 0.5 * abs(lf_paz_pert_flat)


    def resp_cost(p, paz_partial_flags, freqs, normfreq, tf_target, resp_pert0):

        # pack up into PAZ instances
        paz_pert = ida.signals.utils.pack_paz(p, paz_partial_flags)

        # compute perturbed response andnormalize
        resp = ida.signals.utils.compute_response(freqs, paz_pert)
        resp_norm, scale, ndx = ida.signals.utils.normalize_response(resp, freqs, normfreq)

        # calc new TF
        new_tf = divide(resp_norm, resp_pert0)
        # simple dif for residuals array. Assuems tf_target is np.concatenate((tf_target.real, tf_target.imag))
        new_real_imag_tf = concatenate((new_tf.real, new_tf.imag))
        resid = subtract(new_real_imag_tf, tf_target)

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
                                 concatenate((hfmeas_tf_norm.real, hfmeas_tf_norm.imag)),
                                 hf_resp0
                                 ),
                           verbose=0)
    logging.info('HF fitting termination: ' + hf_res.message)
    logging.debug('HF fitting paz results: ' + str(hf_res.x))

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
                                  concatenate((lfmeas_tf_norm.real, lfmeas_tf_norm.imag)),
                                  lf_resp0
                                  ),
                           verbose=0)
    logging.info('LF fitting termination: ' + lf_res.message)
    logging.debug('LF fitting paz results: ' + str(lf_res.x))

    new_hf_paz_pert = ida.signals.utils.pack_paz(hf_res.x, hf_paz_pert_flags)
    new_lf_paz_pert = ida.signals.utils.pack_paz(lf_res.x, lf_paz_pert_flags)
    new_paz = full_paz.copy()
    new_paz.merge_paz_partial(new_hf_paz_pert, hf_paz_pert_map, hf_norm_freq)
    new_paz.merge_paz_partial(new_lf_paz_pert, lf_paz_pert_map, hf_norm_freq)

    return new_paz


def prepare_cal_data(data_dir, lf_fnames, hf_fnames, seis_model, lf_paz_tpl, hf_paz_tpl):
    """Prepare low and high frequency miniseed files produced by qcal for analysis.
    It assumes all three observed Z12 coponents plus input signal will exist in each miniseed file.
    Each components is:
        - trimmed to remove settling and trailing portions of time series
        - corrected for polarity
        - If triaxial seismometer, UVW components are transformed to get horizontal signals
        - Input timeseries are:
            - tapered
            - xformed to frequency space
            - convolved with paz response
            - inverse xformed
            - taper portions trimmed off
            - normed and de-meaned
        - each observed compopnent output time series is then:
            - trimmed just as input timeseries
            - normed and de-meaned

    The algorithm follows the Matlab scripts previously used for calibration processing with the following exceptions:
        1) All 3 components are handled at once
        2) Components for triaxial seismometer are transformed to UVW and then to abs() values for each XYZ component

    NOTE: This is uses the SAME PAZ response for all 3 components.
    TODO: This should be generalized for to accommodate different strating paz for each component

    :param data_dir: Directory path where miniseed and qcal log fiels are found
    :type data_dir:  str
    :param lf_fnames: Tuple containing low frequency miniseed and log filenames
    :type lf_fnames:  (str, str)
    :param hf_fnames: Tuple containing high frequency miniseed and log filenames
    :type hf_fnames: (str, str)
    :param seis_model: Seismometermodel key
    :type seis_model: str
    :param lf_paz_tpl: ComponentTpl with starting LF model with which to convolve the calibration input signal.
    :type lf_paz_tpl: ComponentTpl
    :param hf_paz_tpl: ComponentTpl with starting HF model with which to convolve the calibration input signal.
    :type hf_paz_tpl: ComponentTpl
    :return:
        low freq sampling rate,
        low freq time series start_time,
        low freq convolved input timeseries, in ComponentTpl
        low freq measured east, north, vertical timeseries, in ComponentTpl
        high freq sampling rate,
        high freq time series start_time,
        high freq convolved input timeseries, in ComponentTpl
        high freq measured east, north, vertical timeseries, in ComponentTpl
        complex paz response in low freq band in ComponentTpl, list of low freq frequencies,
        complex paz response in high freq band in ComponentTpl, list of high freq frequencies
    :rtype: float, timestamp, ComponentTpl, ComponentTpl
            float, timestamp, ComponentTpl, ComponentTpl
            ComponentTpl, ndarray, ComponentTpl, ndarray
    """

    if not isinstance(lf_paz_tpl, ComponentsTpl):
        msg = 'lf_paz_tpl must be a ComponentsTpl with LF PAZ (for fitting) responses for each component'
        raise TypeError(msg)

    if not isinstance(hf_paz_tpl, ComponentsTpl):
        msg = 'hf_paz_tpl must be a ComponentsTpl with HF PAZ (for fitting) responses for each component'
        raise TypeError(msg)

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
    cal_lf = ida.calibration.qcal_utils.split_qcal_traces(strm_lf)
    cal_hf = ida.calibration.qcal_utils.split_qcal_traces(strm_hf)

    if seis_model in TRIAXIAL_SEIS_MODELS:
        cal_lf_tpl = triaxial_horizontal_magnitudes(cal_lf, seis_model)
        cal_hf_tpl = triaxial_horizontal_magnitudes(cal_hf, seis_model)
    else:
        cal_lf_tpl = cal_lf
        cal_hf_tpl = cal_hf

    samp_rate_lf = cal_lf_tpl.input.sampling_rate
    start_time_lf = cal_lf_tpl.input.starttime
    samp_rate_hf = cal_hf_tpl.input.sampling_rate
    start_time_hf = cal_hf_tpl.input.starttime
    npts_lf = cal_lf_tpl.input.npts
    npts_hf = cal_hf_tpl.input.npts

    fraction = 0.1  # each side
    logging.debug('Creating tapers...')
    taper_lf = tukey(npts_lf, alpha=fraction * 2, sym=True)
    taper_bin_cnt_lf = int(ceil(npts_lf * fraction))
    taper_hf = tukey(npts_hf, alpha=fraction * 2, sym=True)
    taper_bin_cnt_hf = int(ceil(npts_hf * fraction))
    logging.debug('Creating tapers complete.')

    logging.debug('Generating starting LF (mode=acc) response...')

    freqs_lf = linspace(0, samp_rate_lf/2, npts_lf//2 + 1)  # count is to match behavior of np.fft.rfft below
    resp_tmp_lf = ida.signals.utils.compute_response(freqs_lf, lf_paz_tpl.vertical, mode='acc')
    resp_lf_v, _, _ = ida.signals.utils.normalize_response(resp_tmp_lf, freqs_lf, 0.05)
    resp_tmp_lf = ida.signals.utils.compute_response(freqs_lf, lf_paz_tpl.north, mode='acc')
    resp_lf_n, _, _ = ida.signals.utils.normalize_response(resp_tmp_lf, freqs_lf, 0.05)
    resp_tmp_lf = ida.signals.utils.compute_response(freqs_lf, lf_paz_tpl.east, mode='acc')
    resp_lf_e, _, _ = ida.signals.utils.normalize_response(resp_tmp_lf, freqs_lf, 0.05)

    logging.debug('Generating starting  HF (acc) response...')

    freqs_hf = linspace(0, samp_rate_hf/2, npts_hf//2 + 1)  # count is to match behavior of np.fft.rfft below
    resp_tmp_hf = ida.signals.utils.compute_response(freqs_hf, hf_paz_tpl.vertical, mode='acc')
    resp_hf_v, _, _ = ida.signals.utils.normalize_response(resp_tmp_hf, freqs_hf, 0.05)
    resp_tmp_hf = ida.signals.utils.compute_response(freqs_hf, hf_paz_tpl.north, mode='acc')
    resp_hf_n, _, _ = ida.signals.utils.normalize_response(resp_tmp_hf, freqs_hf, 0.05)
    resp_tmp_hf = ida.signals.utils.compute_response(freqs_hf, hf_paz_tpl.east, mode='acc')
    resp_hf_e, _, _ = ida.signals.utils.normalize_response(resp_tmp_hf, freqs_hf, 0.05)

    logging.debug('Generating starting L/HF responses complete.')

    resp_lf = ComponentsTpl(vertical=resp_lf_v, north=resp_lf_n, east=resp_lf_e)
    resp_hf = ComponentsTpl(vertical=resp_hf_v, north=resp_hf_n, east=resp_hf_e)

    #TODO: This should be generalized for to accommodate different strating paz for each component
    # prep input signal: taper, fft, conv resp, ifft
    logging.debug('Convolving LF input with nominal response...')
    input_fft           = rfft(multiply(cal_lf_tpl.input.data[:npts_lf], taper_lf))
    inp_freqs_cnv_resp  = multiply(input_fft, resp_lf_v)
    lf_inp_wth_resp_v     = irfft(inp_freqs_cnv_resp, npts_lf)
    lf_inp_wth_resp_v     = lf_inp_wth_resp_v[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_inp_wth_resp_v.__itruediv__(lf_inp_wth_resp_v.std())
    lf_inp_wth_resp_v.__isub__(lf_inp_wth_resp_v.mean())
    inp_freqs_cnv_resp  = multiply(input_fft, resp_lf_n)
    lf_inp_wth_resp_n     = irfft(inp_freqs_cnv_resp, npts_lf)
    lf_inp_wth_resp_n     = lf_inp_wth_resp_n[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_inp_wth_resp_n.__itruediv__(lf_inp_wth_resp_n.std())
    lf_inp_wth_resp_n.__isub__(lf_inp_wth_resp_n.mean())
    inp_freqs_cnv_resp  = multiply(input_fft, resp_lf_e)
    lf_inp_wth_resp_e     = irfft(inp_freqs_cnv_resp, npts_lf)
    lf_inp_wth_resp_e     = lf_inp_wth_resp_e[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_inp_wth_resp_e.__itruediv__(lf_inp_wth_resp_e.std())
    lf_inp_wth_resp_e.__isub__(lf_inp_wth_resp_e.mean())
    logging.debug('Convolving LF input with nominal response complete')

    logging.debug('Convolving HF input with nominal response...')
    input_fft           = rfft(multiply(cal_hf_tpl.input.data, taper_hf))
    inp_freqs_cnv_resp  = multiply(input_fft, resp_hf_v)
    hf_inp_wth_resp_v     = irfft(inp_freqs_cnv_resp, npts_hf)
    hf_inp_wth_resp_v     = hf_inp_wth_resp_v[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_inp_wth_resp_v.__itruediv__(hf_inp_wth_resp_v.std())
    hf_inp_wth_resp_v.__isub__(hf_inp_wth_resp_v.mean())
    inp_freqs_cnv_resp  = multiply(input_fft, resp_hf_n)
    hf_inp_wth_resp_n     = irfft(inp_freqs_cnv_resp, npts_hf)
    hf_inp_wth_resp_n     = hf_inp_wth_resp_n[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_inp_wth_resp_n.__itruediv__(hf_inp_wth_resp_n.std())
    hf_inp_wth_resp_n.__isub__(hf_inp_wth_resp_n.mean())
    inp_freqs_cnv_resp  = multiply(input_fft, resp_hf_e)
    hf_inp_wth_resp_e     = irfft(inp_freqs_cnv_resp, npts_hf)
    hf_inp_wth_resp_e     = hf_inp_wth_resp_e[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_inp_wth_resp_e.__itruediv__(hf_inp_wth_resp_e.std())
    hf_inp_wth_resp_e.__isub__(hf_inp_wth_resp_e.mean())
    logging.debug('Convolving HF input with nominal response complete')

    lf_inp_with_resp = ComponentsTpl(vertical=lf_inp_wth_resp_v, north=lf_inp_wth_resp_n, east=lf_inp_wth_resp_e)
    hf_inp_with_resp = ComponentsTpl(vertical=hf_inp_wth_resp_v, north=hf_inp_wth_resp_n, east=hf_inp_wth_resp_e)

    logging.debug('Input signals ready for coherence analysis.')

    # prep output channels
    logging.debug('Preparing LF output for coherence analysis...')
    lf_out_e = cal_lf_tpl.east.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_e.__itruediv__(lf_out_e.std())
    lf_out_e.__isub__(lf_out_e.mean())
    lf_out_n = cal_lf_tpl.north.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_n.__itruediv__(lf_out_n.std())
    lf_out_n.__isub__(lf_out_n.mean())
    lf_out_v = cal_lf_tpl.vertical.data.copy()[taper_bin_cnt_lf:-taper_bin_cnt_lf]
    lf_out_v.__itruediv__(lf_out_v.std())
    lf_out_v.__isub__(lf_out_v.mean())
    logging.debug('Preparing LF output for coherence analysis complete.')

    logging.debug('Preparing HF output for coherence analysis...')
    hf_out_e = cal_hf_tpl.east.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_out_e.__itruediv__(hf_out_e.std())
    hf_out_e.__isub__(hf_out_e.mean())
    hf_out_n = cal_hf_tpl.north.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_out_n.__itruediv__(hf_out_n.std())
    hf_out_n.__isub__(hf_out_n.mean())
    hf_out_v = cal_hf_tpl.vertical.data.copy()[taper_bin_cnt_hf:-taper_bin_cnt_hf]
    hf_out_v.__itruediv__(hf_out_v.std())
    hf_out_v.__isub__(hf_out_v.mean())
    logging.debug('Preparing HF output for coherence analysis complete.')

    lf_meas = ComponentsTpl(vertical=lf_out_v, north=lf_out_n, east=lf_out_e)
    hf_meas = ComponentsTpl(vertical=hf_out_v, north=hf_out_n, east=hf_out_e)

    logging.debug('SNR LF VER: {}'.format(1/subtract(lf_inp_wth_resp_v, lf_out_v).std()))
    logging.debug('SNR LF NOR: {}'.format(1/subtract(lf_inp_wth_resp_n, lf_out_n).std()))
    logging.debug('SNR LF EAS: {}'.format(1/subtract(lf_inp_wth_resp_e, lf_out_e).std()))
    logging.debug('SNR HF VER: {}'.format(1/subtract(hf_inp_wth_resp_v, hf_out_v).std()))
    logging.debug('SNR HF NOR: {}'.format(1/subtract(hf_inp_wth_resp_n, hf_out_n).std()))
    logging.debug('SNR HF EAS: {}'.format(1/subtract(hf_inp_wth_resp_e, hf_out_e).std()))

    return samp_rate_lf, start_time_lf, lf_inp_with_resp, lf_meas, \
           samp_rate_hf, start_time_hf, hf_inp_with_resp, hf_meas, \
           resp_lf, freqs_lf, resp_hf, freqs_hf


def triaxial_horizontal_magnitudes(cal_tpl, seis_model):
    """Transform XYZ components to UVW, then to absolute values for ENZ.
    This obtains the true absolute value time series for each horizontal component

    :param cal_tpl: QCal Tuple with component output teimseries plus input
    :type cal_tpl: ida.calibration.qcal_utils.QCalData
    :param seis_model: Seismometer model key
    :type seis_model: str
    :return: New, transformed QCal tuple
    :rtype: ida.calibration.qcal_utils.QCalData
    """

    if seis_model in TRIAXIAL_SEIS_MODELS:
        uvw = ida.signals.utils.channel_xform((cal_tpl.east,
                                               cal_tpl.north,
                                               cal_tpl.vertical),
                                              TRIAXIAL_TRANSFORMS[seis_model][XFRM_TYPE_XYZ2UVW])
        enz = ida.signals.utils.channel_xform(uvw, TRIAXIAL_TRANSFORMS[seis_model][XFRM_TYPE_UVW2ENZ_ABS])
        new_cal_tpl = ida.calibration.qcal_utils.QCalData(east=enz[0],
                                                          north=enz[1],
                                                          vertical=enz[2],
                                                          input=cal_tpl.input)
        success = True
    else:
        msg = 'The seismomemter model {} is unsupported or not a triaxial instrument.'.format(seis_model)
        logging.error(msg)
        raise Exception(msg)

    return new_cal_tpl


