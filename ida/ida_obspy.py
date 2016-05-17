from numpy import require
from ida.obspy.io.mseed.core import _read_mseed, _is_mseed
from ida.signals.trace import IDATrace
from ida.signals.stream import IDAStream


def read_mseed(file_name_or_object, dtype=None):

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

