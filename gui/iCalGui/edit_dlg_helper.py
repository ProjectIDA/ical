import copy

from PyQt5 import QtCore, QtWidgets

from config.wrapper_cfg import WrapperCfg

from gui.iCalGui.edit_dlg import Ui_EditDlg


class EditDlgHelper(object):

    EDIT_MODE = 1
    ADD_MODE = 2

    def __init__(self): #, orig_cfg, mode, edit_dlg):
        pass

    @property
    def new_cfg(self):
        if not hasattr(self, '_new_cfg'):
            self._new_cfg = {}
        return self._new_cfg
    
    @new_cfg.setter
    def new_cfg(self, value):
        self._new_cfg = value

    @property
    def sensorlist(self):
        if not hasattr(self, '_sensorlist'):
            self._sensorlist = {}
        return self._sensorlist
    
    @sensorlist.setter
    def sensorlist(self, value):
        self._sensorlist = value


    def setupUi(self, orig_cfg, mode, edit_dlg):
        
        self.new_cfg = copy.deepcopy(orig_cfg)
        print(self.new_cfg)
        self.edit_dlg = edit_dlg

        title = 'Edit Configuration' if mode == EditDlgHelper.EDIT_MODE else 'Add New Configuration'
        self.edit_dlg.mainGB.setTitle(title)

        self.edit_dlg.netLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_NET, ''))
        self.edit_dlg.staLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_STA, ''))
        self.edit_dlg.ipLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_IP, ''))
        self.edit_dlg.tagnoLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_TAGNO, ''))
        self.edit_dlg.snLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_SN, ''))
        self.edit_dlg.dpLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_DATAPORT , ''))
        self.edit_dlg.dpauthLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_DP1_AUTH, ''))
        self.edit_dlg.sensAMonPortLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_MONPORT_A, ''))
        self.edit_dlg.sensBMonPortLE.setText(self.new_cfg.get(WrapperCfg.WRAPPER_KEY_MONPORT_B, ''))

        # ip regex (([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}
        self.edit_dlg.netLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.staLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.ipLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.tagnoLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.snLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.dpLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.dpauthLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.sensAMonPortLE.textEdited.connect(self.LEEdited)
        self.edit_dlg.sensBMonPortLE.textEdited.connect(self.LEEdited)

        # now lets set Sensor model drop downs...

        a_sens_ndx = -1
        b_sens_ndx = -1
        for senkey, sendesc in self._sensorlist:
            self.edit_dlg.sensACB.addItem(sendesc, QtCore.QVariant(senkey))
            if mode == EditDlgHelper.EDIT_MODE:
                if senkey == self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A]:
                    a_sens_ndx = self.edit_dlg.sensACB.count() - 1
            else:
                if senkey == 'none':
                    a_sens_ndx = self.edit_dlg.sensACB.count() - 1
        for senkey, sendesc in self._sensorlist:
            self.edit_dlg.sensBCB.addItem(sendesc, QtCore.QVariant(senkey))
            if mode == EditDlgHelper.EDIT_MODE:
                if senkey == self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B]:
                    b_sens_ndx = self.edit_dlg.sensBCB.count() - 1
            else:
                if senkey == 'none':
                    b_sens_ndx = self.edit_dlg.sensBCB.count() - 1

        self.edit_dlg.sensACB.setCurrentIndex(a_sens_ndx if a_sens_ndx >= 0 else 0)
        self.edit_dlg.sensBCB.setCurrentIndex(b_sens_ndx if b_sens_ndx >= 0 else 0)

        self.edit_dlg.sensACB.currentIndexChanged.connect(self.SensorAChange)
        self.edit_dlg.sensBCB.currentIndexChanged.connect(self.SensorBChange)

    # def set_sensor_list(self, )

    def SensorAChange(self, new_ndx):
        print('CHANGE')
        senskey = self.edit_dlg.sensACB.itemData(new_ndx)
        self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_A] = senskey
        self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_A] = senskey
        self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_DESCR_A] = list(filter(lambda s: s[0] == senskey, self.sensorlist))[0][1]


    def SensorBChange(self, new_ndx):
        senskey = self.edit_dlg.sensBCB.itemData(new_ndx)
        self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_COMPNAME_B] = senskey
        self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_ROOTNAME_B] = senskey
        self.new_cfg[WrapperCfg.WRAPPER_KEY_SENS_DESCR_B] = list(filter(lambda s: s[0] == senskey, self.sensorlist))[0][1]


    def LEEdited(self, newtext):
        # this is crude, but since slot doesn't get source of signal, what option is there...
        self.new_cfg[WrapperCfg.WRAPPER_KEY_NET] = self.edit_dlg.netLE.text()