# -*- mode: python -*-
#######################################################################################################################
# Copyright (C) 2016  Regents of the University of California
#
# This is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License (GNU GPL) as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# A copy of the GNU General Public License can be found in LICENSE.TXT in the root of the source code repository.
# Additionally, it can be found at http://www.gnu.org/licenses/.
#
# NOTES: Per GNU GPLv3 terms:
#   * This notice must be kept in this source file
#   * Changes to the source must be clearly noted with date & time of change
#
# If you use this software in a product, an explicit acknowledgment in the product documentation of the contribution
# by Project IDA, Institute of Geophysics and Planetary Physics, UCSD would be appreciated but is not required.
#######################################################################################################################

block_cipher = None

a = Analysis(['PyCal.py'],
             pathex=['/Users/dauerbach/dev/ical/src'],
             binaries=[
              ('bin/qcal', 'IDA/bin'),
              ('bin/q330', 'IDA/bin'),
              ('bin/qverify', 'IDA/bin'),
              ('/usr/local/opt/libxml2/lib/libxml2.2.dylib', '.'),
              ('./ida/obspy/lib/libmseed_Darwin_64bit_py34.so', '.')
              ],
             datas=[
              ('data/*', 'IDA/data'),
              ('lic/*', 'LIC'),
              ('LICENSE.TXT', 'LIC'),
              ('etc', 'etc'),
              ],
             hiddenimports=[],
             hookspath=['pyinstaller_hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyCal',
          debug=True,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyCal')
app = BUNDLE(coll,
             name='PyCal.app',
             icon=None,
             bundle_identifier='edu.ucsd.ida.PyCal',
             info_plist={
                'CFBundleShortVersionString': '1.0.0'
             })
