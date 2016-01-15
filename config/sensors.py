import os

from config.utils import configresult
from config.dbparse import *

from config.ical_config_reader import IcalConfigReader
from config.sensor import Sensor, SensorBadColumnCountExcept, SensorMalformedRecordExcept

class Sensors(IcalConfigReader):

    def __init__(self, fpath):
        self.fpath = fpath
        self.items = []
        self.iter_ndx = 0
        self.parsed_ok = False

        # read & parse data
        self.parsed_ok, self.msgs = super().parse_cfg_file(self.fpath, self.parse_cfg_records)

        if not self.parsed_ok:
            for m in self.msgs:
                print(m)


    def clear(self):
        self.items = []


    def parse_cfg_records(self, recs):

        msgs = []
        self.clear()

        for lineno, rec in enumerate(recs):

            rec = rec.strip()

            if not (rec.startswith('#') or (len(rec) == 0)):

                try:
                    sensor = Sensor(rec)
                except SensorBadColumnCountExcept:
                    msgs.append('ERROR: Sensor record should have at least ' + str(Sensor.SENSOR_COLCOUNT) + ' columns. [' + rec + ']. Record ignored.')
                except SensorMalformedRecordExcept:
                    msgs.append('ERROR: Sensor record appears to be invalid: [' + rec + ']. Record ignored.')
                except Exception as e:
                    msgs.append('ERROR: Unknown error parsing Sensor record: [' + rec + ']. Record ignored.' + '\n' + str(e))
                else:
                    if next(filter(lambda s: s == sensor, self.items), None) == None:
                        self.items.append(sensor)
                    else:
                        msgs.append('WARN: Duplicate Sensor record: [' + rec + ']. Record ignored.')

        self.items.sort()

        return msgs


    def find(self, key):
        """Returns the first Sensor with SHORT_NAME of key.
        If no Sensor is found, returns None.
        """
        return next(filter(lambda s: s.data[Sensor.SENSOR_KEY_SHORTNAME] == key, self.items), None)


