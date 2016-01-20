from PyQt5 import QtCore, QtGui

from config.ical_config import Icalcfg
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
            return 9 # just for testing
        else:
            return 0


    def UpdateCfg(self, ndx, new_cfg):
        self.cfg.merged_cfg[ndx].data.update(new_cfg)
        # self.


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
            elif role == QtCore.Qt.ForegroundRole:
                return QtGui.QBrush(QtGui.QColor(196,0,0,255))
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
