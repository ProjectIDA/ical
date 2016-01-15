import abc
import os
from pathlib import Path

class IcalConfigItemReader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, record_str):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass


    @abc.abstractmethod
    def __eq__(self, other):
        pass
  

    @abc.abstractmethod
    def __lt__(self, other):
        pass
