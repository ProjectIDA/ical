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

from PyQt5 import QtCore, QtGui
from config.wrapper_cfg import WrapperCfg

class CfgDataModel(QtCore.QAbstractTableModel):

    COL_COUNT = 9
    NET_COL = 0
    STA_COL = 1
    TAGNO_COL = 2
    SN_COL = 3
    IP_COL = 4
    DESCR_A_COL = 5
    DESCR_B_COL = 6
    DP_COL = 7
    DPAUTH_COL = 8
    LOC_COL = 9
    CHANS_COL = 10


    def __init__(self, cfg):
        super(CfgDataModel, self).__init__()
        self.cfg = cfg

    def rowCount(self, parent):
        if self.cfg:
            return len(self.cfg.merged_cfg)
        else:
            return 0

    def columnCount(self, parent):
        if self.cfg:
            return CfgDataModel.COL_COUNT
        else:
            return 0


    def UpdateCfg(self, orig_tagno, new_cfg):

        if self.cfg.update(orig_tagno, new_cfg):
            self.endResetModel()
        else:
            raise Exception('Error saving configuration for Q330 with TAG NUM: ' + orig_tagno)


    def AddCfg(self, new_cfg):

        tagno = new_cfg[WrapperCfg.WRAPPER_KEY_TAGNO]
        if not self.cfg.find(tagno):
            if self.cfg.append(new_cfg):
                self.endResetModel()
            else:
                raise Exception('Error saving configuartion for Q330 with TAG NUM: ' + tagno)
        else:
            raise Exception('Error saving configuration. Config with TAG NUM: ' + tagno + ' already exists')


    def data(self, index, role):

        mrgcfg = self.cfg.merged_cfg[index.row()]
        col = index.column()
        if col == CfgDataModel.NET_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_NET, '')
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.STA_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_STA, '')
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.TAGNO_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_TAGNO, '')
            elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignRight + QtCore.Qt.AlignVCenter
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.SN_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_SN, '')
            elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignHCenter + QtCore.Qt.AlignVCenter
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.IP_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_IP, '')
            # elif role == QtCore.Qt.ForegroundRole:
            #     return QtGui.QBrush(QtGui.QColor(196,0,0,255))
            elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignHCenter + QtCore.Qt.AlignVCenter
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.DESCR_A_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_SENS_DESCR_A, '')
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.DESCR_B_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_SENS_DESCR_B, '')
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.DP_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_DATAPORT, '')
            else:
                return QtCore.QVariant()
        elif col == CfgDataModel.DPAUTH_COL:
            if role == QtCore.Qt.DisplayRole:
                return mrgcfg.data.get(WrapperCfg.WRAPPER_KEY_DP1_AUTH, '')
            else:
                return QtCore.QVariant()
        else:
            return QtCore.QVariant()


    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):

        if (orientation == QtCore.Qt.Horizontal):

            if section == CfgDataModel.NET_COL:
                if (role == QtCore.Qt.DisplayRole):
                    return QtCore.QVariant(WrapperCfg.WRAPPER_KEY_NET.upper())
                elif role == QtCore.Qt.TextAlignmentRole:
                    return QtCore.Qt.AlignLeft + QtCore.Qt.AlignVCenter
                else:
                    return QtCore.QVariant()
            if section == CfgDataModel.STA_COL:
                if (role == QtCore.Qt.DisplayRole):
                    return QtCore.QVariant(WrapperCfg.WRAPPER_KEY_STA.upper())
                elif role == QtCore.Qt.TextAlignmentRole:
                    return QtCore.Qt.AlignLeft + QtCore.Qt.AlignVCenter
                else:
                    return QtCore.QVariant()
            elif section == CfgDataModel.TAGNO_COL:
                if (role == QtCore.Qt.DisplayRole):
                    return QtCore.QVariant('Q330 Tag #')
                elif role == QtCore.Qt.TextAlignmentRole:
                    return QtCore.Qt.AlignRight + QtCore.Qt.AlignVCenter
                else:
                    return QtCore.QVariant()
            elif section == CfgDataModel.SN_COL:
                if (role == QtCore.Qt.DisplayRole):
                    return QtCore.QVariant('Q330 SN #')
                elif role == QtCore.Qt.TextAlignmentRole:
                    return QtCore.Qt.AlignHCenter + QtCore.Qt.AlignVCenter
                else:
                    return QtCore.QVariant()
            elif section == CfgDataModel.IP_COL:
                if (role == QtCore.Qt.DisplayRole):
                    return QtCore.QVariant('Q330 IP4')
                else:
                    return QtCore.QVariant()
            elif section == CfgDataModel.DESCR_A_COL:
                if (role == QtCore.Qt.DisplayRole):
                    return QtCore.QVariant('Sensor A')
                else:
                    return QtCore.QVariant()
            elif section == CfgDataModel.DESCR_B_COL:
                if (role == QtCore.Qt.DisplayRole):
                    return QtCore.QVariant('Sensor B')
                else:
                    return QtCore.QVariant()
            elif section == CfgDataModel.DP_COL:
                if role == QtCore.Qt.DisplayRole:
                    return QtCore.QVariant('Data Port')
                else:
                    return QtCore.QVariant()
            elif section == CfgDataModel.DPAUTH_COL:
                if role == QtCore.Qt.DisplayRole:
                    return QtCore.QVariant('DP Auth Code')
                else:
                    return QtCore.QVariant()
            else:
                return QtCore.QVariant()

        else:
            return QtCore.QVariant()
