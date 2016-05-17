# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 15:49:51 2016
@author: http://stackoverflow.com/questions/35478526/
pyinstaller-numpy-intel-mkl-fatal-error-cannot-load-mkl-intel-thread-dll
"""

from PyInstaller import log as logging 
from PyInstaller import compat
from os import listdir

try:
    libdir = compat.base_prefix + "/lib"
    mkllib = [x for x in listdir(libdir) if x.startswith('libmkl_')]
    mkllib = ['libmkl_avx2.dylib']  # Just need this one for now, so leaving other bloatware out
    if mkllib != []:
        logger = logging.getLogger(__name__)
        logger.info("MKL installed as part of numpy, importing that!")
        binaries = [(libdir + "/" + l, '') for l in mkllib]
except FileNotFoundError:
    pass