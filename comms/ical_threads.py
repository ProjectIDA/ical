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
""" Classes for threading long running calibration processes"""

from PyQt5 import QtCore
import logging
import subprocess
import os.path
from os import getcwd, chdir

class AnalysisThread(QtCore.QThread):
    """QThread class for running the data analysis after acquisition"""

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
    """QThread class for checking communication with Q330 via qverify binary"""

    qVerifyQueryResult = QtCore.pyqtSignal(str, str, bool, str)
    # qverify -v root=/ida/nrts/etc dec00 4
    def __init__(self, host, port, bin_root_path, cfg_root_path):
        super().__init__()
        self.bin_path = os.path.join(bin_root_path, 'qverify')
        self.host = host
        self.port = port
        self.cfg_path = cfg_root_path
        self.proc = None
        self.cancelling = False

    def run(self):
        result = self.qVerify_query()
        if not self.cancelling:
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
        else:
            lines = str(stderr).strip().splitlines()
            infomsg = ' '.join(lines)
        logging.debug('qverify output ' + infomsg)

        return (self.host, self.port, ret_code, infomsg)


    def cancel(self):
        self.cancelling = True
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait()
            except Exception as e:
                logging.debug('Exception while terminating subprocess: ' + str(e))


class QCalThread(QtCore.QThread):
    """QThread class for running calibration data acquisition"""

    completed = QtCore.pyqtSignal(int, str, str)

    def __init__(self, bin_root_path, cmdline, output_path):
        super().__init__()
        self.bin_path = os.path.join(bin_root_path, 'qcal')
        self.cmdline = cmdline
        self.output_path = output_path
        self.orig_dir = None
        self.proc = None

    def cancel(self):
        if self.proc:
            if self.orig_dir:
                chdir(self.orig_dir)
            self.proc.terminate()
            try:
                self.proc.wait()
            except Exception as e:
                logging.debug('Exception while terminating subprocess: ' + str(e))

        # if self.proc:
        #     self.proc.terminate()
        #     self.terminate()
        #     self.wait()

    def run(self):
        result = self.run_qcal()
        self.completed.emit(*result)

    def run_qcal(self):
        self.orig_dir = getcwd()
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
        finally:
            chdir(self.orig_dir)
            ret_code = self.proc.returncode

        if ret_code == 0:
            lines = str(stdout).splitlines()
            infomsg = lines[1] + '\n\n' + lines[2]
            msfilename = lines[1].split()[-1]
        else:
            lines = str(stderr).splitlines()
            infomsg = '\n'.join(lines)
            msfilename = ''
        logging.debug('qcal output ' + infomsg)

        return ret_code, infomsg, msfilename


class PingThread(QtCore.QThread):
    """QThread class for checking network connection to given host using Ping"""

    completed = QtCore.pyqtSignal(str, bool, str)

    def __init__(self, host):
        super().__init__()
        self.host = host

    def run(self):
        result = self.ping_host(self.host)
        self.completed.emit(*result)

    def cancel(self):
        self.terminate()
        self.wait()

    def ping_host(self, host):
        proc = subprocess.Popen(
            ['ping', '-c', '1', '-t', '1', host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        ret_code = proc.returncode
        if ret_code == 0:
            lines = str(stdout, 'utf-8').splitlines()
            time_line = lines[1]
            res = time_line.split()[6].split('=')[1] + time_line.split()[7]
        else:
            res = str(stderr, 'utf-8')
        return (host, proc.returncode == 0, res)

