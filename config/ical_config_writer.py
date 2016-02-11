import abc
import os
import logging

class IcalConfigWriter(metaclass=abc.ABCMeta):

    @classmethod
    def ensure_file(cls, fpath):

        if (type(fpath) == str) and \
            (len(fpath.strip()) > 0):
            absfpath = os.path.abspath(fpath)
            if not os.path.exists(absfpath):
                absdir = os.path.split(absfpath)[0]
                os.makedirs(absdir, exist_ok=True)

            return True

        else:
            return False


    @classmethod
    @abc.abstractmethod
    def file_header():
        pass


    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass


    @abc.abstractmethod
    def __delitem__(self, key):
        pass

