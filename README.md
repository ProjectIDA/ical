# PyCal
GUI front-end and configuration management for IDA calibration utilities. Developed specifically for random binary calibration of Streckheisen STS 2.5 seismometers.

PyCal is a self contained Python application being developed and tested on Apple computers running OS X version 10.10 or 10.11.
PyCal utilizes the latest Python scientific computing and visualization libraries including NumPy, SciPy and Matplotlib (see http://scipy.org/).
PyCal also makes use of a number of utilities previously developed by Project IDA for calibrating the II network GSN stations.
For the reading of raw miniseed data it utilizes source code from ObsPy, a python-based framework for seismology (http://obspy.org/).

## Build Dependencies
* Python 3.4.4
* Qt User Interface Framework (v5.6; built from source)
* PyQt5 (v5.6; w/ pyuic5)
* sip (v4.18; built from source)
* matplotlib (v1.5.1; built from source with custom configuration set via setup.cfg.matplotlib_build)
* PyInstaller (v3.2, develop branch v3.2-47-g8c6332e)
* python-dateutil (2.4.2)
* pytz (2015.7)
* NumPy (v1.11.0)
* SciPy (v0.17.0)
* setuptools (v19.2; due to conflicts with PyInstaller, this must be v19.2)

## Other Tools Utilized
* Qt Creator 3.6.1 (Used for form building, but not technically necessary)

## Source Code
Open Source source code used in Version 1.0 of PyCal can be found here: http://ida.ucsd.edu/web/pickup/sandia/

## Licensing
PyCal python source code is made available under the GNU GPLv3 license. See LICENSE.TXT.

PyCal utilizes functionality provided by other open source projects under the following licenses:

#### Qt v5.6 (LGPLv3, LGPLv2.1):
* https://www.qt.io/faq/
* https://www.qt.io/qt-licensing-terms/
* See lic/Qt directory in source for license details

#### PyQt v5.6 and SIP 4.18 (GNU GPL v3):
* https://www.riverbankcomputing.com
* https://www.riverbankcomputing.com/commercial/license-faq

#### Matplotlib 1.5.1 (Based on PSF (Python lic)):
* http://matplotlib.org
* http://matplotlib.org/users/license.html
* See lic/matplotlib-1.5.1 directory in source for license details

#### NumPy (v1.11.0) and SciPy (v0.17.0)
* http://scipy.org/
* See lic/SciPy directory in source for license details/

#### ObsPy v1.0.1 (LGPL v3):
* https://github.com/obspy/obspy
* http://dx.doi.org/10.5281/zenodo.48254

### Additional Licensing Resources:
* https://opensource.org/licenses/LGPL-3.0
* http://www.gnu.org/licenses/licenses.html
* http://www.gnu.org/licenses/quick-guide-gplv3.html
