from PyQt5 import QtCore
import logging
import subprocess
import os.path
from os import getcwd, chdir

class PingThread(QtCore.QThread):

    pingResult = QtCore.pyqtSignal(str, bool, str) 

    def __init__(self, host):    
        super().__init__()
        self.host = host

    def run(self):
        result = self.ping_host(self.host)
        self.pingResult.emit(*result)

    def ping_host(self, host):
        proc = subprocess.Popen(
            ['ping', '-c', '1', '-t', '1', host],
            stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        retcode = proc.returncode
        ping_time = ''
        if retcode == 0:
            lines = str(stdout, 'utf-8').splitlines()
            time_line = lines[1]
            ping_time = time_line.split()[6].split('=')[1] + time_line.split()[7]
        return (host, proc.returncode == 0, ping_time)


class Q330Thread(QtCore.QThread):

    q330QueryResult = QtCore.pyqtSignal(str, bool, str) 

    def __init__(self, host, cmd, bin_root_path, cfg_root_path):    
        super().__init__()
        self.bin_path = os.path.join(bin_root_path, 'q330')
        self.host = host
        self.cmd = cmd
        self.cfg_path = cfg_root_path

    def run(self):
        result = self.q330_query(self.host, self.cmd)
        self.q330QueryResult.emit(*result)

    def q330_query(self, host, cmd):
        proc = subprocess.Popen(
            [self.bin_path, 'root='+self.cfg_path, host, cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        stdout, stderr = proc.communicate()
        retcode = proc.returncode
        if retcode == 0:
            infomsg = '\n'.join(stdout.splitlines())
        else:
            lines = stderr.splitlines()
            infomsg = ' '.join(lines)
        return (host, proc.returncode, infomsg)


class QCalThread(QtCore.QThread):

    qcalResult = QtCore.pyqtSignal(int, str) 

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
        self.qcalResult.emit(*result)

    def run_qcal(self):
        retcode = -666
        infomsg = ''
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
            logging.error('EXCEPTION: '+str(e))
        retcode = self.proc.returncode
        if retcode == 0:
            lines = stdout.splitlines()
            infomsg = lines[1] + '\n\n' + lines[2]
        else:
            lines = stderr.splitlines()
            infomsg = '\n'.join(lines)
        return (retcode, infomsg)


