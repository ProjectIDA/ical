import os

from config.ical_config_reader import IcalConfigReader
from config.sensor import Sensor, SensorBadColumnCountExcept, SensorMalformedRecordExcept

class Sensors(IcalConfigReader):

    def __init__(self, fpath):
        self.fpath = fpath
        self.items = []
        self.iter_ndx = 0

        # read & parse data
        self.parsed_ok = super().parse_cfg_file(self.fpath, self.parse_cfg_records)


    def clear(self):
        self.items = []


    def SensorModelList(self):
        resl = []
        for sensor in self.items:
            resl.append((sensor.data[Sensor.SENSOR_KEY_SHORTNAME], sensor.data[Sensor.SENSOR_KEY_DESCR]))
        return resl




    def append(self, rec):
        rec = rec.strip()

        if not (rec.startswith('#') or (len(rec) == 0)):

            try:
                sensor = Sensor(rec)
            except SensorBadColumnCountExcept:
                logging.warning('Sensor record should have at least ' + str(Sensor.SENSOR_COLCOUNT) + ' columns. [' + rec + ']. Record ignored.')
            except SensorMalformedRecordExcept:
                logging.warning('Sensor record appears to be invalid: [' + rec + ']. Record ignored.')
            except Exception as e:
                logging.warning('Unknown error parsing Sensor record: [' + rec + ']. Record ignored.' + '\n' + str(e))
            else:
                if next(filter(lambda s: s == sensor, self.items), None) == None:
                    self.items.append(sensor)
                else:
                    logging.warning('Duplicate Sensor record: [' + rec + ']. Record ignored.')


    def sort(self):
        self.items.sort()


    def find(self, key):
        """Returns the first Sensor with SHORT_NAME of key.
        If no Sensor is found, returns None.
        """
        return next(filter(lambda s: s.data[Sensor.SENSOR_KEY_SHORTNAME] == key, self.items), None)


