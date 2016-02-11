import glob
from obspy.core import read

strm = read('CAL-172.16.4.8-sts1-rbhf-2016-0208-1325.ms')

print(strm)

tr = strm[0]
msg = "%s %s %f %f" % (tr.stats.station, str(tr.stats.starttime),
                       tr.data.mean(), tr.data.std())
strm.plot()