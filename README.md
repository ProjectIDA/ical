# ical
Calibration results reporting &amp; GUI front-end to IDA qcal program.

PyCal is a self contained Python application being developed for to be used on Apple computers running OS X version 10.10 or 10.11. PyCal utilizes the latest Python scientific computing and visualization libraries including NumPy, SciPy and Matplotlib (see http://scipy.org/). For seismic analysis it builds on ObsPy, a python-based framework for seismology (http://obspy.org/). PyCal makes use of a number of calibration utilities previously developed by Project IDA for calibrating the II network GSN stations.



## Build Dependencies
* Python 3.4.4
* Qt Libraries (v5.6; custom built form source)
  * qt-everywhere-opensource-src-5.6.0.tar.gz
* Qt Creator 3.6.1 (Used for form building, but not technically necessary)
* PyQt5 (v5.6) (w/ pyuic5)
  * PyQt5_gpl-5.6.tar.gz
* sip (v4.18; built from source)
  * sip-4.18.tar.gz
* matplotlib (v1.5.1; custom built from source)
  * matplotlib-1.5.1-cp34-cp34m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl.tar.gz
* PyInstaller (3.2, develop branch)
  * pyinstaller-pyinstaller-v3.2-47-g8c6332e.zip
* python-dateutil (2.4.2)
* pytz (2015.7)
* numpy
* scipy
* setuptools (v19.2; **must be v19.2**)