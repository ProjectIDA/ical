import abc
import os

class IcalConfigWriter(metaclass=abc.ABCMeta):

    def write(self):

        success = False

        self.msgs.clear()
        if (self.isdirty):
            success, self.msgs = super().write_data_file(self.fpath, self.items)

        return (success, self.msgs)
        

    @classmethod
    def write_data_file(cls, fpath, items):

        success = False
        msgs = []

        if cls.ensure_file(fpath):
            absfpath = os.path.abspath(fpath)

            try:

                with open(absfpath, mode='w') as fl:
                    for i in items:
                        fl.write(i.write())

                success = True

            except OSError as e:
                msgs.append('ERRORS: Error writing to file: ' + absfpath)

        return (success, errs)


    @classmethod
    def ensure_file(cls, fpath):

        if (type(fpath) == str) and \
            (len(fpath.strip()) > 0):
            absfpath = os.path.abspath(fpath)
            if not os.path.exists(absfpath):
                absdir = os.path.split(absfpath)[0]
                os.makedirs(absdir, exist_ok=True)

                with open(absfpath, 'w') as outf:
                    outf.write(cls.file_header())

                return True
            else:
                return False

        else:
            return False


    @classmethod
    @abc.abstractmethod
    def file_header():
        pass


    # @property
    # # @abc.abstractmethod
    # def items(self):
    #     return 'Should never see this'

    # @items.setter
    # # @abc.abstractmethod
    # def items(self, newvalue):
    #     return


    # @property
    # # @abc.abstractmethod
    # def isdirty(self):
    #     return 'Should never see this'

    # @isdirty.setter
    # # @abc.abstractmethod
    # def isdirty(self, newvalue):
    #     return


    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass


    @abc.abstractmethod
    def __delitem__(self, key):
        pass

