from os.path import join
from numpy import subtract, angle, pi, abs
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from numpy import linspace, ceil


def save_response_comparison_plots(sta, chancodes, loc, amp_fn, pha_fn, seis_model, timestamp,
                                   operating_sample_rate, num_freqs, nom_resp,
                                   n_resp, n_adev, n_pdev,
                                   e_resp, e_adev, e_pdev,
                                   v_resp, v_adev, v_pdev):

    freqs = linspace(0, operating_sample_rate/2, num_freqs)  # must start with 0hz
    nyquist = operating_sample_rate / 2.0
    nyq_90pct_freqndx = int(ceil(0.9 * len(freqs)))


    datestr = timestamp.strftime('%Y-%m-%d %H:%M UTC')

    f100 = plt.figure(100, figsize=(15, 20))
    plt.subplot(211)
    plt.tick_params(labelsize=13)
    plt.title('Amplitude Responses - ({:<} - {:<} - {:<} - {:<})\n(sampling rate: {} hz)'.format(sta,
                                                                                                     loc,
                                                                                                     seis_model,
                                                                                                     datestr,
                                                                                                     int(round(operating_sample_rate, 0))),
              fontsize=14,
              fontweight='bold')
    plt.ylabel('Amplitude (Normalized, V/m/s)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.loglog(freqs, abs(n_resp), 'g', linewidth=0.5)
    bh2, = plt.loglog(freqs, abs(e_resp), 'y', linewidth=0.75)
    bhz, = plt.loglog(freqs, abs(v_resp), 'r', linewidth=0.5)
    nom, = plt.loglog(freqs, abs(nom_resp), 'k', linewidth=0.5)
    plt.legend((bh1, bh2, bhz, nom), (chancodes.north, chancodes.east, chancodes.vertical, 'Nominal'), loc=0, handlelength=5, fontsize=12)
    #
    ax = plt.axis()
    plt.axis([1e-3, nyquist, ax[2], ax[3]])
    #
    ax = plt.subplot(212)
    plt.tick_params(labelsize=13)
    plt.title('Amplitude Deviations from Nominal - ({:<} - {:<} - {:<} - {:<})'.format(sta, loc, seis_model, datestr), fontsize=14, fontweight='bold')
    plt.ylabel('Amplitude Deviation (%)\n(up to 90% of Nyquist)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.semilogx(freqs[1:nyq_90pct_freqndx], n_adev[:nyq_90pct_freqndx-1], 'g', linewidth=0.75)
    bh2, = plt.semilogx(freqs[1:nyq_90pct_freqndx], e_adev[:nyq_90pct_freqndx-1], 'y', linewidth=0.75)
    bhz, = plt.semilogx(freqs[1:nyq_90pct_freqndx], v_adev[:nyq_90pct_freqndx-1], 'r', linewidth=0.75)
    plt.legend((bh1, bh2, bhz), (chancodes.north, chancodes.east, chancodes.vertical), loc=0, handlelength=5, fontsize=12)
    amp_toler_pcnt = 5.0
    plt.axis([1e-3, nyquist, -amp_toler_pcnt * 2, amp_toler_pcnt * 2])
    ax_lims = plt.axis()
    within_tolerance_verts = [(ax_lims[0], -amp_toler_pcnt),
                              (ax_lims[0], amp_toler_pcnt),
                              (ax_lims[1], amp_toler_pcnt),
                              (ax_lims[1], -amp_toler_pcnt)]
    poly = Polygon(within_tolerance_verts, facecolor='#D8FFD8', edgecolor='0.9', label='Acceptable Tolerance Band')
    ax.add_patch(poly)
    f100.savefig(amp_fn, dpi=400)
    plt.clf()

    f101 = plt.figure(101, figsize=(15, 20))
    plt.subplot(211)
    plt.tick_params(labelsize=13)
    plt.title('Phase Responses - ({:<} - {:<} - {:<} - {:<})\n(sampling rate: {} hz)'.format(sta,
                                                                                                 loc,
                                                                                                 seis_model,
                                                                                                 datestr,
                                                                                                 int(round(operating_sample_rate, 0))),
              fontsize=14,
              fontweight='bold')

    plt.ylabel('Phase (deg)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.semilogx(freqs, angle(n_resp) * 180 / pi, 'g', linewidth=0.5)
    bh2, = plt.semilogx(freqs, angle(e_resp) * 180 / pi, 'y', linewidth=0.75)
    bhz, = plt.semilogx(freqs, angle(v_resp) * 180 / pi, 'r', linewidth=0.5)
    nom, = plt.semilogx(freqs, angle(nom_resp) * 180 / pi, 'k', linewidth=0.5)
    plt.legend((bh1, bh2, bhz, nom), (chancodes.north, chancodes.east, chancodes.vertical, 'Nominal'), loc=0, handlelength=5, fontsize=12)
    ax = plt.axis()
    plt.axis([1e-3, nyquist, ax[2], ax[3]])

    ax = plt.subplot(212)
    plt.tick_params(labelsize=13)
    plt.title('Phase Deviations from Nominal - ({:<} - {:<} - {:<} - {:<})'.format(sta, loc, seis_model, datestr), fontsize=14, fontweight='bold')
    plt.ylabel('Phase Deviation (deg)\n(up to 90% of Nyquist)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.semilogx(freqs[1:nyq_90pct_freqndx], n_pdev[:nyq_90pct_freqndx-1], 'g', linewidth=0.75)
    bh2, = plt.semilogx(freqs[1:nyq_90pct_freqndx], e_pdev[:nyq_90pct_freqndx-1], 'y', linewidth=0.75)
    bhz, = plt.semilogx(freqs[1:nyq_90pct_freqndx], v_pdev[:nyq_90pct_freqndx-1], 'r', linewidth=0.75)
    plt.legend((bh1, bh2, bhz), (chancodes.north, chancodes.east, chancodes.vertical), loc=0, handlelength=5, fontsize=12)
    pha_toler_degs = 5.0
    plt.axis([1e-3, nyquist, -pha_toler_degs * 2, pha_toler_degs * 2])
    poly = Polygon(within_tolerance_verts, facecolor='#D8FFD8', edgecolor='0.9', label='Acceptable Tolerance Band')
    ax.add_patch(poly)
    #
    # plt.show()
    f101.savefig(pha_fn, dpi=400)
    plt.clf()


def apc_plot(sampling_freq, freqs, amp, pha, coh):

    freq_max = 0.4 * sampling_freq


    plt.subplot(311)
    plt.semilogx(freqs, amp)
    plt.grid(which='both')
    plt.xlim(1e-3, freq_max)
    plt.ylim()

    plt.subplot(312)
    plt.semilogx(freqs, pha)
    plt.grid(which='both')
    plt.xlim(1e-3, freq_max)

    plt.subplot(313)
    plt.semilogx(freqs, coh)
    plt.grid(which='both')
    plt.xlim(1e-3, freq_max)
    plt.ylim(0.95, 1.05)
    plt.show()

def plot_cal_output_with_residual(calout, calinp):

    resid = subtract(calout, calinp)
    snr = 1 / resid.std()

    plt.figure(1, figsize=(10,10))
    plt.plot(calout.data)
    # hold on
    plt.plot(resid.data, 'r')
    # hold off
    tstr = 'SNR = {}'.format(snr)
    plt.title(tstr)



