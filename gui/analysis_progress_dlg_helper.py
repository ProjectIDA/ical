from PyQt5.QtWidgets import QMessageBox
from comms.ical_threads import AnalysisThread

class AnalysisProgressDlgHelper(object):

    def __init__(self, dlg, dlgUI):
        self.dlgUI = dlgUI
        self.qtDlg = dlg
        self.ims_calres_txt_fn = ''
        self.cal_amp_plot_fn = ''
        self.cal_pha_plot_fn = ''
        self.subthread = None

        self.dlgUI.cancelBtn.clicked.connect(self.cancel)


    def cancel(self):

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText('Do you wish to cancel this anaylsis?')
        msg_box.setInformativeText('If you cancel you will need to rerun the calibration from the beginning.')
        yes_btn = msg_box.addButton(QMessageBox.Yes)
        no_btn = msg_box.addButton(QMessageBox.No)
        msg_box.setDefaultButton(no_btn)

        msg_box.exec()

        if msg_box.clickedButton() == yes_btn:
            self.subthread.cancel()
            self.qtDlg.done(-1)


    def run_analysis(self, run_method, *args):

        self.subthread = AnalysisThread(run_method, *args)
        self.subthread.completed.connect(self.finished)
        self.subthread.start()

        return self.qtDlg.exec(), \
               self.ims_calres_txt_fn, \
               self.cal_amp_plot_fn, \
               self.cal_pha_plot_fn


    def finished(self, ims_calres_txt_fn, cal_amp_plot_fn, cal_pha_plot_fn):
        self.ims_calres_txt_fn = ims_calres_txt_fn
        self.cal_amp_plot_fn = cal_amp_plot_fn
        self.cal_pha_plot_fn = cal_pha_plot_fn
        self.qtDlg.done(0)