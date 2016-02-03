import copy

from PyQt5 import QtGui, QtCore, QtWidgets

from config.wrapper_cfg import WrapperCfg

from gui.edit_dlg import Ui_EditDlg


class EditDlgHelper(object):

    EDIT_MODE = 1
    ADD_MODE = 2

    def __init__(self): 
        pass

    # @property
    # def new_cfg(self):
    #     if not hasattr(self.dlgUI, '_new_cfg'):
    #         self.dlgUI._new_cfg = {}
    #     return self.dlgUI._new_cfg
    
    # @new_cfg.setter
    # def new_cfg(self, value):
    #     self.dlgUI._new_cfg = value

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

        # ip regex (([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}
        self.dlgUI.netLE.textEdited.connect(self.LEEdited)
        self.dlgUI.staLE.textEdited.connect(self.LEEdited)
        self.dlgUI.ipLE.textEdited.connect(self.LEEdited)
        self.dlgUI.tagnoLE.textEdited.connect(self.LEEdited)
        self.dlgUI.snLE.textEdited.connect(self.LEEdited)
        self.dlgUI.dpLE.textEdited.connect(self.LEEdited)
        self.dlgUI.dpauthLE.textEdited.connect(self.LEEdited)
        self.dlgUI.sensAMonPortLE.textEdited.connect(self.LEEdited)
        self.dlgUI.sensBMonPortLE.textEdited.connect(self.LEEdited)

        self.refresh_dialog()


        # title = 'Edit Configuration' if self.mode == EditDlgHelper.EDIT_MODE else 'Add New Configuration'
        # self.dlgUI.mainGB.setTitle(title)

        # self.dlgUI.netLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_NET, ''))
        # self.dlgUI.staLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_STA, ''))
        # self.dlgUI.ipLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_IP, ''))
        # self.dlgUI.tagnoLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_TAGNO, ''))
        # self.dlgUI.snLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_SN, ''))
        # self.dlgUI.dpLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_DATAPORT , ''))
        # self.dlgUI.dpauthLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_DP1_AUTH, ''))
        # self.dlgUI.sensAMonPortLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_MONPORT_A, ''))
        # self.dlgUI.sensBMonPortLE.setText(self.dlgUI.new_cfg.get(WrapperCfg.WRAPPER_KEY_MONPORT_B, ''))

        # # now lets set Sensor model drop downs...
        # self.dlgUI.sensACB.setCurrentIndex(-1)
        # self.dlgUI.sensBCB.setCurrentIndex(-1)
        # for senkey, sendesc in self._sensorlist:
        #     self.dlgUI.sensACB.addItem(sendesc, QtCore.QVariant(senkey))
        #     self.dlgUI.sensBCB.addItem(sendesc, QtCore.QVariant(senkey))
        #     if mode == EditDlgHelper.EDIT_MODE:
        #         if senkey == self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A]:
        #             self.dlgUI.sensACB.setCurrentIndex(self.dlgUI.sensACB.count() - 1)
        #         if senkey == self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B]:
        #             self.dlgUI.sensBCB.setCurrentIndex(self.dlgUI.sensBCB.count() - 1)
        #     else:
        #         if senkey == 'none':
        #             self.dlgUI.sensACB.setCurrentIndex(self.dlgUI.sensACB.count() - 1)
        #         if senkey == 'none':
        #             self.dlgUI.sensBCB.setCurrentIndex(self.dlgUI.sensBCB.count() - 1)


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

        # now lets set Sensor model drop downs...
        # self.dlgUI.sensACB.clear()#setCurrentIndex(0)
        # self.dlgUI.sensBCB.clear()#setCurrentIndex(0)
        for senkey, sendesc in self._sensorlist:
            # self.dlgUI.sensACB.addItem(sendesc, QtCore.QVariant(senkey))
            # self.dlgUI.sensBCB.addItem(sendesc, QtCore.QVariant(senkey))
            if self.mode == EditDlgHelper.EDIT_MODE:
                if senkey == self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A]:
                    # self.dlgUI.sensACB.setCurrentIndex(self.dlgUI.sensACB.count() - 1)
                    self.dlgUI.sensACB.setCurrentText(sendesc)
                if senkey == self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B]:
                    # self.dlgUI.sensBCB.setCurrentIndex(self.dlgUI.sensBCB.count() - 1)
                    self.dlgUI.sensBCB.setCurrentText(sendesc)
            else:
                if senkey == 'none':
                    self.dlgUI.sensACB.setCurrentText(sendesc)
                    self.dlgUI.sensBCB.setCurrentText(sendesc)

    def reset(self):
        self.dlgUI.new_cfg = copy.deepcopy(self.orig_cfg)
        self.refresh_dialog()


    def SensorAChange(self, new_ndx):
        senskey = self.dlgUI.sensACB.itemData(new_ndx)
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] = senskey
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A] = senskey
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A] = list(filter(lambda s: s[0] == senskey, self.sensorlist))[0][1]


    def SensorBChange(self, new_ndx):
        senskey = self.dlgUI.sensBCB.itemData(new_ndx)
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B] = senskey
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B] = senskey
        self.dlgUI.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B] = list(filter(lambda s: s[0] == senskey, self.sensorlist))[0][1]


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
