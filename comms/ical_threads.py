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
        self.proc = None

    def run(self):
        result = self.qVerify_query()
        self.qVerifyQueryResult.emit(*result)

    def qVerify_query(self):
        self.proc = subprocess.Popen(
            [self.bin_path, '-v', 'root='+self.cfg_path, self.host, self.port],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        stdout, stderr = self.proc.communicate()
        ret_code = self.proc.returncode
        if ret_code == 0:
            infomsg = '\n'.join(str(stdout).splitlines())
            # print(infomsg)
        else:
            lines = str(stderr).splitlines()
            infomsg = ' '.join(lines)
            # print(infomsg)
        return (self.host, self.port, ret_code, infomsg)


    def cancel(self):
        if self.proc:
            self.proc.terminate()
            self.terminate()
            self.wait()


class QCalThread(QtCore.QThread):

    completed = QtCore.pyqtSignal(int, str, str)

    def __init__(self, bin_root_path, cmdline, output_path):
        super().__init__()
        self.bin_path = os.path.join(bin_root_path, 'qcal')
        self.cmdline = cmdline
        self.output_path = output_path
        self.proc = None

    def cancel(self):
        if self.proc:
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
