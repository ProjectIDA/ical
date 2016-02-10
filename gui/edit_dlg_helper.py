import copy
import re

from PyQt5 import QtGui, QtCore, QtWidgets

from config.wrapper_cfg import WrapperCfg

from gui.edit_dlg import Ui_EditDlg


class EditDlgHelper(object):

    EDIT_MODE = 1
    ADD_MODE = 2

    def __init__(self): 
        self.is_dirty = False

    @property
    def sensorlist(self):
        if not hasattr(self, '_sensorlist'):
            self._sensorlist = {}
        return self._sensorlist
    
    @sensorlist.setter
    def sensorlist(self, value):
        self._sensorlist = value


    def setupUi(self, orig_cfg, mode, dlg, dlgUI):

        self.orig_cfg = orig_cfg
        self.mode = mode
        self.dlgUI = dlgUI
        self.dlgUI.new_cfg = copy.deepcopy(self.orig_cfg)

        # only do this once
        for senkey, sendesc in self._sensorlist:
            self.dlgUI.sensACB.addItem(sendesc, QtCore.QVariant(senkey))
            self.dlgUI.sensBCB.addItem(sendesc, QtCore.QVariant(senkey))

        self.dlgUI.sensACB.currentIndexChanged.connect(self.SensorAChange)
        self.dlgUI.sensBCB.currentIndexChanged.connect(self.SensorBChange)

        self.dlgUI.netLE.textEdited.connect(self.LEEdited)
        self.dlgUI.staLE.textEdited.connect(self.LEEdited)
        self.dlgUI.ipLE.textEdited.connect(self.LEEdited)
        self.dlgUI.tagnoLE.textEdited.connect(self.LEEdited)
        self.dlgUI.snLE.textEdited.connect(self.LEEdited)
        self.dlgUI.dpLE.textEdited.connect(self.LEEdited)
        self.dlgUI.dpauthLE.textEdited.connect(self.LEEdited)
        self.dlgUI.sensAMonPortLE.textEdited.connect(self.LEEdited)
        self.dlgUI.sensBMonPortLE.textEdited.connect(self.LEEdited)

        self.resetBtn = self.dlgUI.buttonBox.button(QtWidgets.QDialogButtonBox.Reset)
        self.resetBtn.setDefault(True)
        self.resetBtn.clicked.connect(self.reset)
        # pal = resetBtn.palette()
        # pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255,0,255))
        # resetBtn.setPalette(pal)
        # resetBtn.setAutoFillBackground(True)
        self.cancelBtn = self.dlgUI.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        self.cancelBtn.setDefault(False)
        self.saveBtn = self.dlgUI.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
        self.saveBtn.setDefault(False)
        # self.dlgUI.buttonBox.setFocus()
        # saveBtn.setFocus()
        # self.dlgUI.buttonBox.setFocusProxy(saveBtn)
        # self.dlgUI.tagnoLE.setFocus()

        self.refresh_dialog()
        self.dlgUI.mainGB.setFocus()


    def refresh_dialog(self):

        title = 'Edit Configuration' if self.mode == EditDlgHelper.EDIT_MODE else 'Add New Configuration'
        self.dlgUI.mainGB.setTitle(title)

        self.dlgUI.netLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_NET, ''))
        self.dlgUI.staLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_STA, ''))
        self.dlgUI.ipLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_IP, ''))
        self.dlgUI.tagnoLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_TAGNO, ''))
        self.dlgUI.snLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_SN, ''))
        self.dlgUI.dpLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_DATAPORT , ''))
        self.dlgUI.dpauthLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_DP1_AUTH, ''))
        self.dlgUI.sensAMonPortLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_MONPORT_A, ''))
        self.dlgUI.sensBMonPortLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_MONPORT_B, ''))

        self.dlgUI.sensACB.setCurrentText('UNKNOWN SENSOR MODEL')
        self.dlgUI.sensBCB.setCurrentText('UNKNOWN SENSOR MODEL')
        self.dlgUI.sensACB.setCurrentIndex(-1)
        self.dlgUI.sensBCB.setCurrentIndex(-1)
        for senkey, sendesc in self._sensorlist:
            # self.dlgUI.sensACB.addItem(sendesc, QtCore.QVariant(senkey))
            # self.dlgUI.sensBCB.addItem(sendesc, QtCore.QVariant(senkey))
            if self.mode == EditDlgHelper.EDIT_MODE:
                if senkey == self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A]:
                    # self.dlgUI.sensACB.setCurrentIndex(self.dlgUI.sensACB.count() - 1)
                    self.dlgUI.sensACB.setCurrentText(sendesc)
                if senkey == self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B]:
                    # self.dlgUI.sensBCB.setCurrentIndex(self.dlgUI.sensBCB.count() - 1)
                    self.dlgUI.sensBCB.setCurrentText(sendesc)
            else:
                if senkey == 'none':
                    self.dlgUI.sensACB.setCurrentText(sendesc)
                    self.dlgUI.sensBCB.setCurrentText(sendesc)

        self.validate()


    def reset(self):
        self.dlgUI.new_cfg = copy.deepcopy(self.orig_cfg)
        self.refresh_dialog()


    def SensorAChange(self, new_ndx):
        if (new_ndx >= 0):
            senskey = self.dlgUI.sensACB.itemData(new_ndx)
            self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] = senskey
            self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A] = senskey
            self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A] = list(filter(lambda s: s[0] == senskey, self.sensorlist))[0][1]
            self.validate()


    def SensorBChange(self, new_ndx):
        if (new_ndx >= 0):
            senskey = self.dlgUI.sensBCB.itemData(new_ndx)
            self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B] = senskey
            self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B] = senskey
            self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B] = list(filter(lambda s: s[0] == senskey, self.sensorlist))[0][1]
            self.validate()


    def LEEdited(self, newtext):
        # this is crude, but since slot doesn't get source object of signal, what option is there...
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_NET] = self.dlgUI.netLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_STA] = self.dlgUI.staLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_IP] = self.dlgUI.ipLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_TAGNO] = self.dlgUI.tagnoLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SN] = self.dlgUI.snLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_DATAPORT] = self.dlgUI.dpLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SFN_AUTH] = self.dlgUI.dpauthLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_CFG_AUTH] = self.dlgUI.dpauthLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_DP1_AUTH] = self.dlgUI.dpauthLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_DP2_AUTH] = self.dlgUI.dpauthLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_DP3_AUTH] = self.dlgUI.dpauthLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_DP4_AUTH] = self.dlgUI.dpauthLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_MONPORT_A] = self.dlgUI.sensAMonPortLE.text()
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_MONPORT_B] = self.dlgUI.sensBMonPortLE.text()
        self.validate()


    def validate(self):
        valid = True

        self.resetBtn.setEnabled(self.is_dirty)

        # check NET
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_NET, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_NET]):
            self.dlgUI.netLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.netLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check STA
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_STA, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_STA]):
            self.dlgUI.staLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.staLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check IP
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_IP, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_IP]):
            self.dlgUI.ipLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.ipLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check TAGNO
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_TAGNO, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_TAGNO]):
            self.dlgUI.tagnoLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.tagnoLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check SN
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_SN, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SN]):
            self.dlgUI.snLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.snLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check DATAPORT
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_DATAPORT, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_DATAPORT]):
            self.dlgUI.dpLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.dpLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check DP AUTH
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_DP1_AUTH, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_DP1_AUTH]):
            self.dlgUI.dpauthLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.dpauthLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check SENSOR A
        if self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] in [x[0] for x in self.sensorlist]:
            pal = self.dlgUI.sensACB.palette();
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 102, 0))
            self.dlgUI.sensACB.setPalette(pal);
        else:
            pal = self.dlgUI.sensACB.palette();
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor(179, 0, 0))
            self.dlgUI.sensACB.setPalette(pal);
            valid = False

        # check SENSOR A CAL MON PORT
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_MONPORT_A, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_MONPORT_A]):
            self.dlgUI.sensAMonPortLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.sensAMonPortLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False

        # check SENSOR B
        if self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B] in [x[0] for x in self.sensorlist]:
            pal = self.dlgUI.sensBCB.palette();
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 102, 0))
            self.dlgUI.sensBCB.setPalette(pal);
        else:
            pal = self.dlgUI.sensBCB.palette();
            pal.setColor(QtGui.QPalette.Text, QtGui.QColor(179, 0, 0))
            self.dlgUI.sensBCB.setPalette(pal);
            # self.dlgUI.sensBCB.setStyleSheet("QComboBox{color:rgb(179, 0, 0);}")
            valid = False

        # check SENSOR B CAL MON PORT
        if WrapperCfg.is_valid_wcfg_key(WrapperCfg.WRAPPER_KEY_MONPORT_B, self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_MONPORT_B]):
            self.dlgUI.sensBMonPortLE.setStyleSheet("QLineEdit{color:rgb(0, 102, 0);}")
        else:
            self.dlgUI.sensBMonPortLE.setStyleSheet("QLineEdit{color:rgb(179, 0, 0);}")
            valid = False



        self.saveBtn.setEnabled(valid)

