import abc
import os
import functools

class IcalConfigReader(metaclass=abc.ABCMeta):


    def __iter__(self):
        self.iter_ndx = 0
        return self


    def __next__(self):
        self.iter_ndx += 1
        if self.iter_ndx > len(self.items):
            raise StopIteration
        return self.items[self.iter_ndx - 1]


    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError
        elif key >= len(self.items):
            raise IndexError
        else:
            return self.items[key]      
        

    def __str__(self):
        return functools.reduce(lambda s1, s2: '\n'.join([s1, str(s2)]), self.items, '').strip()


    @classmethod
    def read_data_file(cls, fpath):

        success = False

        with open(fpath, 'r') as f:
            data = f.read()
            success = True

        if success:
            data = data.strip()
            records = data.splitlines()

        return (success, records)


    @classmethod
    def parse_cfg_file(cls, fpath, parser):

        msgs = []
        success = False

        if os.path.exists(fpath):
            success, recs = cls.read_data_file(fpath)
            msgs.extend(parser(recs))
            success = True
        else:
            msgs.append('ERROR: File does not exist: [' + os.path.abspath(fpath) + ']')

        return (success, msgs)


    @abc.abstractmethod
    def find(self, key):
        pass


    @abc.abstractmethod
    def clear(self):
        pass


    @abc.abstractmethod
    def parse_cfg_records(self, recs):
        pass

