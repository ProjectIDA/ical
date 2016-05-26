from PyQt5 import QtCore
import logging
import subprocess
import os.path
from os import getcwd, chdir

class AnalysisThread(QtCore.QThread):

    completed = QtCore.pyqtSignal(str, str, str)

    def __init__(self, run_method, *args):
        super().__init__()
        self.run_method = run_method
        self.args = args

    def run(self):
        ims_calres_txt_fn, cal_amp_plot_fn, cal_pha_plot_fn = self.run_method(*self.args)
        self.completed.emit(ims_calres_txt_fn, cal_amp_plot_fn, cal_pha_plot_fn)

    def cancel(self):
        self.terminate()
        self.wait(2000)


class QVerifyThread(QtCore.QThread):

    qVerifyQueryResult = QtCore.pyqtSignal(str, str, bool, str)
    # qverify -v root=/ida/nrts/etc dec00 4
    def __init__(self, host, port, bin_root_path, cfg_root_path):
        super().__init__()
        self.bin_path = os.path.join(bin_root_path, 'qverify')
        self.host = host
        self.port = port
        self.cfg_path = cfg_root_path

    def run(self):
        result = self.qVerify_query()
        self.qVerifyQueryResult.emit(*result)

    def qVerify_query(self):
        proc = subprocess.Popen(
            [self.bin_path, '-v', 'root='+self.cfg_path, self.host, self.port],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        stdout, stderr = proc.communicate()
        ret_code = proc.returncode
        if ret_code == 0:
            infomsg = '\n'.join(str(stdout).splitlines())
            # print(infomsg)
        else:
            lines = str(stderr).splitlines()
            infomsg = ' '.join(lines)
            # print(infomsg)
        return (self.host, self.port, proc.returncode, infomsg)


class QCalThread(QtCore.QThread):

    completed = QtCore.pyqtSignal(int, str, str)

    def __init__(self, bin_root_path, cmdline, output_path):
        super().__init__()
        self.bin_path = os.path.join(bin_root_path, 'qcal')
        self.cmdline = cmdline
        self.output_path = output_path

    def cancel(self):
        self.proc.terminate()
        self.terminate()
        self.wait()

    def run(self):
        result = self.run_qcal()
        self.completed.emit(*result)

    def run_qcal(self):
        curdir = getcwd()
        chdir(self.output_path)
        logging.info('Spawning calibration subprocess: ' + ' '.join([self.bin_path] + self.cmdline.split()[1:]))
        logging.info('Output directory: ' + getcwd())
        try:
            self.proc = subprocess.Popen(
                [self.bin_path] + self.cmdline.split()[1:],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)
            stdout, stderr = self.proc.communicate()
        except Exception as e:
            stdout, stderr = '', ''
            logging.error('EXCEPTION: ' + str(e))
        ret_code = self.proc.returncode
        chdir(curdir)
        if ret_code == 0:
            lines = str(stdout).splitlines()
            infomsg = lines[1] + '\n\n' + lines[2]
            msfilename = lines[1].split()[-1]
            # print(lines)
        else:
            lines = str(stderr).splitlines()
            infomsg = '\n'.join(lines)
            msfilename = ''
        return ret_code, infomsg, msfilename
