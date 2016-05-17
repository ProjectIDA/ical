from os.path import join
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def save_response_comparison_plots(sta, chancodes, loc, amp_fn, pha_fn, seis_model, timestamp, freqs, nom_resp,
                                   n_resp, n_adev, n_pdev,
                                   e_resp, e_adev, e_pdev,
                                   v_resp, v_adev, v_pdev):
    # pass
    # lets construct output filenames
    datestr = timestamp.strftime('%Y-%m-%d %H:%M UTC')

    f100 = plt.figure(100, figsize=(15, 20))
    plt.subplot(211)
    plt.tick_params(labelsize=13)
    plt.title('Amplitude Responses - ({:<} - {:<} - {:<} - {:<})'.format(sta, loc, seis_model, datestr), fontsize=14, fontweight='bold')
    plt.ylabel('Amplitude (Normalized, V/m/s)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.loglog(freqs, abs(n_resp), 'g', linewidth=0.5)
    bh2, = plt.loglog(freqs, abs(e_resp), 'y', linewidth=0.75)
    bhz, = plt.loglog(freqs, abs(v_resp), 'r', linewidth=0.5)
    nom, = plt.loglog(freqs, abs(nom_resp), 'k', linewidth=0.5)
    plt.legend((bh1, bh2, bhz, nom), (chancodes.north, chancodes.east, chancodes.vertical, 'Nominal'), loc=0, handlelength=5, fontsize=12)

    ax = plt.axis()
    # ax[0] = 1e-3
    # ax[1] = 18
    plt.axis([1e-3, 20, ax[2], ax[3]])

    ax = plt.subplot(212)
    plt.tick_params(labelsize=13)
    plt.title('Amplitude Deviations from Nominal - ({:<} - {:<} - {:<} - {:<})'.format(sta, loc, seis_model, datestr), fontsize=14, fontweight='bold')
    plt.ylabel('Amplitude Deviation (%)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.semilogx(freqs[1:], n_adev, 'g', linewidth=0.75)
    bh2, = plt.semilogx(freqs[1:], e_adev, 'y', linewidth=0.75)
    bhz, = plt.semilogx(freqs[1:], v_adev, 'r', linewidth=0.75)
    plt.legend((bh1, bh2, bhz, nom), (chancodes.north, chancodes.east, chancodes.vertical, 'Nominal'), loc=0, handlelength=5, fontsize=12)
    amp_toler_pcnt = 5.0
    plt.axis([1e-3, 20, -amp_toler_pcnt * 2, amp_toler_pcnt * 2])
    ax_lims = plt.axis()
    within_tolerance_verts = [(ax_lims[0], -amp_toler_pcnt),
                              (ax_lims[0], amp_toler_pcnt),
                              (ax_lims[1], amp_toler_pcnt),
                              (ax_lims[1], -amp_toler_pcnt)]
    poly = Polygon(within_tolerance_verts, facecolor='#D8FFD8', edgecolor='0.9', label='Acceptable Tolerance Band')
    ax.add_patch(poly)

    f100.savefig(amp_fn, dpi=400)

    f101 = plt.figure(101, figsize=(15, 20))
    plt.subplot(211)
    plt.tick_params(labelsize=13)
    plt.title('Phase Responses - ({:<} - {:<} - {:<} - {:<})'.format(sta, loc, seis_model, datestr), fontsize=14, fontweight='bold')
    plt.ylabel('Phase (deg)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.semilogx(freqs, np.angle(n_resp) * 180 / np.pi, 'g', linewidth=0.5)
    bh2, = plt.semilogx(freqs, np.angle(e_resp) * 180 / np.pi, 'y', linewidth=0.75)
    bhz, = plt.semilogx(freqs, np.angle(v_resp) * 180 / np.pi, 'r', linewidth=0.5)
    nom, = plt.semilogx(freqs, np.angle(nom_resp) * 180 / np.pi, 'k', linewidth=0.5)
    plt.legend((bh1, bh2, bhz, nom), (chancodes.north, chancodes.east, chancodes.vertical, 'Nominal'), loc=0, handlelength=5, fontsize=12)
    ax = plt.axis()
    plt.axis([1e-3, 20, ax[2], ax[3]])

    ax = plt.subplot(212)
    plt.tick_params(labelsize=13)
    plt.title('Phase Deviations from Nominal - ({:<} - {:<} - {:<} - {:<})'.format(sta, loc, seis_model, datestr), fontsize=14, fontweight='bold')
    plt.ylabel('Phase Deviation (deg)', fontsize=12, fontweight='bold')
    plt.xlabel('Frequency (hz)', fontsize=12, fontweight='bold')
    plt.grid(which='both')
    bh1, = plt.semilogx(freqs[1:], n_pdev, 'g', linewidth=0.75)
    bh2, = plt.semilogx(freqs[1:], e_pdev, 'y', linewidth=0.75)
    bhz, = plt.semilogx(freqs[1:], v_pdev, 'r', linewidth=0.75)
    plt.legend((bh1, bh2, bhz, nom), (chancodes.north, chancodes.east, chancodes.vertical, 'Nominal'), loc=0, handlelength=5, fontsize=12)
    pha_toler_degs = 5.0
    plt.axis([1e-3, 20, -pha_toler_degs * 2, pha_toler_degs * 2])
    poly = Polygon(within_tolerance_verts, facecolor='#D8FFD8', edgecolor='0.9', label='Acceptable Tolerance Band')
    ax.add_patch(poly)

    f101.savefig(pha_fn, dpi=400)


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

    resid = np.subtract(calout, calinp)
    snr = 1 / resid.std()

    plt.figure(1, figsize=(10,10))
    plt.plot(calout.data)
    # hold on
    plt.plot(resid.data, 'r')
    # hold off
    tstr = 'SNR = {}'.format(snr)
    plt.title(tstr)



