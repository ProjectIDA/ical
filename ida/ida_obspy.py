from numpy import require
from ida.obspy.io.mseed.core import _read_mseed, _is_mseed
from ida.signals.trace import IDATrace
from ida.signals.stream import IDAStream

"""IDA Wrapper around subset of Obspy functionality"""

def read_mseed(file_name_or_object, dtype=None):
    """Read miniseed data from specified file and optionally cast to type dtype.

    :param file_name_or_object: filename or stream to read from
    :type file_name_or_object: str, file
    :param dtype: numpy datatype to cast raw sample values to
    :type dtype: np.dtype
    :return: IDAStream instance consting of IDATraces with miniseed raw data
    :rtype: IDAStream
    """

    if _is_mseed(file_name_or_object):

        tracelist = _read_mseed(file_name_or_object)

        idatracelist = []
        for trace in tracelist:
            header = trace[0]
            data = trace[1]
            if dtype:
                data = require(data, dtype)

            idatracelist.append(IDATrace(header, data=data))
    else:
        raise TypeError('File is not a valid miniseed object.')

    return IDAStream(traces=idatracelist)

