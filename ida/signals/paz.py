import numpy as np
import os.path
import logging
import ida.signals.utils


class PAZ(object):
    FILE_FORMATS = ['ida']
    MODE_ZEROS = {
        'acc': 0,
        'vel': 1,
        'disp': 2
    }
    UNITS = ['hz', 'rad']
    PAZ_HEADER_IDA = '0x8001  # type 0x8001 = analog'

    def __init__(self, mode, units, pzfilename=None, fileformat=None):

        """
        :type pzfilename: str
        :type fileformat: str
        :type mode: str
        :type units: object
        """

        self._filename = pzfilename
        self.fileformat = fileformat
        self._mode = mode
        self._units = units
        self._h0 = 1
        self._poles = np.zeros(0, dtype=np.complex128)
        self._zeros = np.zeros(0, dtype=np.complex128)

        if mode not in PAZ.MODE_ZEROS.keys():
            raise ValueError("Invalid MODE requested: '{}'. Valid values: {}".format(mode, PAZ.MODE_ZEROS.keys()))

        if units not in PAZ.UNITS:
            raise ValueError("Invalid units specified: '{}'. Valid values: {}".format(units, PAZ.UNITS))

        if pzfilename and fileformat:

            if not isinstance(self._filename, str):
                raise TypeError("Str type expected for filename: '{}'".format(self._filename))
            else:
                self._filename = os.path.abspath(os.path.expanduser(self._filename))

            if not os.path.exists(self._filename):
                raise Exception("File not found: '{}'".format(self._filename))

            if fileformat not in PAZ.FILE_FORMATS:
                raise ValueError("Unsupported fileformat requested: '{}'.  Supported values: {}".format(
                    fileformat,
                    PAZ.FILE_FORMATS))

            self._load_paz_file()


    def _load_paz_file(self):

        with open(self._filename, 'rt') as pzfl:
            pzlines = pzfl.readlines()
            if self.fileformat == 'ida':
                self._parse_ida_paz(pzlines)

    def _parse_ida_paz(self, pzlines):

        if ' # type ' in pzlines[0]:

            # get num zeros
            (num, _, _) = pzlines[1].partition('#')
            z_num = int(num)

            # get num poles
            (num, _, _) = pzlines[2].partition('#')
            p_num = int(num)

            ndx = 3
            while 'zeros' not in pzlines[ndx]:
                ndx += 1

            ndx += 1
            for z_ndx in range(0, z_num):  # skip first zero, so one less to process
                vals = [val.strip() for val in pzlines[ndx].split(',')]
                self.add_zero(complex(float(vals[0]), float(vals[1])))
                ndx += 1

            while 'poles' not in pzlines[ndx]:
                ndx += 1

            ndx += 1
            for p_ndx in range(0, p_num):
                vals = [val.strip() for val in pzlines[ndx].split(',')]
                self.add_pole(complex(float(vals[0]), float(vals[1])))
                ndx += 1

            # dbl check we got the num of values we expected
            if (z_num != self.num_zeros) or (p_num != self.num_poles):
                msg = "Error reading correct number of poles and zeros in file '{}'".format(self._filename)
                logging.error(msg)
                raise Exception(msg)


    def save(self, filename):

        with open(filename, 'wt') as ofl:
            ofl.write(self.PAZ_HEADER_IDA + '\n')
            ofl.write('{:<3} # number of zeros\n'.format(self.num_zeros))
            ofl.write('{:<3} # number of poles\n'.format(self.num_poles))
            ofl.write('\n')
            ofl.write('# zeros\n')
            for zero in self._zeros:
                ofl.write('{:>12.5E}, {:>12.5E}\n'.format(zero.real, zero.imag))
            ofl.write('\n')
            ofl.write('# poles\n')
            for pole in self._poles:
                ofl.write('{:>12.5E}, {:>12.5E}\n'.format(pole.real, pole.imag))


    @property
    def h0(self):
        return self._h0

    @h0.setter
    def h0(self, h0):
        self._h0 = h0

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        self._units = units

    @property
    def num_poles(self):
        return self._poles.size

    @property
    def num_zeros(self):
        return self._zeros.size

    def add_pole(self, pole):
        ndx = len(self._poles)
        self._poles.resize((ndx + 1,))
        self._poles[ndx] = np.complex128(pole)

    def add_zero(self, zero):
        ndx = len(self._zeros)
        self._zeros.resize((ndx + 1,))
        self._zeros[ndx] = np.complex128(zero)

    def zeros(self, mode=None, units=None):
        if mode:
            zero_cnt_dif = PAZ.MODE_ZEROS[mode] - PAZ.MODE_ZEROS[self.mode]
            if zero_cnt_dif > 0:
                zeros = np.concatenate((np.zeros(zero_cnt_dif, dtype=np.complex128), self._zeros))
            elif zero_cnt_dif < 0:
                if self._zeros.size >= abs(zero_cnt_dif):
                    zeros = self._zeros[abs(zero_cnt_dif):self._zeros.size].copy()
                else:
                    raise Exception("Can't convert PAZ with mode '{}' to mode '{}'".format(self.mode, mode))
            else:
                zeros = self._zeros.copy()
        else:
            zeros = self._zeros.copy()

        if (units == 'hz') and (self.units == 'rad'):
            zeros /= 2 * np.pi
        elif (units == 'rad') and (self.units == 'hz'):
            zeros *= 2 * np.pi

        return zeros

    def poles(self, mode=None, units=None):
        poles = self._poles.copy()
        if (units == 'hz') and (self.units == 'rad'):
            poles /= 2 * np.pi
        elif (units == 'rad') and (self.units == 'hz'):
            poles *= 2 * np.pi

        return poles


    def merge_paz_partial(self, paz_partial, paz_map, norm_freq):

        if len(paz_map[0]) > 0:
            self._poles[paz_map[0]] = paz_partial._poles

        if len(paz_map[1]) > 0:
            self._zeros[paz_map[1]] = paz_partial._zeros

        resp = ida.signals.utils.compute_response(np.array([norm_freq]), self, mode=self.mode)
        self.h0 = 1.0 / abs(resp)


    def make_partial(self, paz_map, norm_freq):

        newpaz = PAZ(mode=self.mode, units=self.units, fileformat=self.fileformat)
        newpaz.h0 = self.h0
        newpaz._poles = self._poles[paz_map[0]]
        newpaz._zeros = self._zeros[paz_map[1]]

        resp = ida.signals.utils.compute_response(np.array([norm_freq]), newpaz, mode=self.mode)
        newpaz.h0 = 1.0 / abs(resp)

        return newpaz


    def copy(self):

        newpaz = PAZ(mode=self.mode, units=self.units, fileformat=self.fileformat)
        newpaz.h0 = self.h0
        newpaz._poles = self._poles.copy()
        newpaz._zeros = self._zeros.copy()

        return newpaz