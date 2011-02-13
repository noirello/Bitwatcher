# -*- coding: UTF-8 -*-
import base64
import sys
from PySide import QtCore, QtGui

import utils
from connector import Connector

class SettingsWindow(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        tabbox = QtGui.QTabWidget()
        tabbox.addTab(self.create_NWTab(), u"Netwatcher")
        tabbox.addTab(self.create_uTTab(), u"uTorrent Web API")
        tabbox.addTab(self.create_aTab(), u"Alapbeállítások")
        btn_lyl = QtGui.QHBoxLayout()
        ok_b = QtGui.QPushButton()
        ok_b.setText("OK")
        ok_b.clicked.connect(self.set)
        btn_lyl.addSpacerItem(QtGui.QSpacerItem(0, 0))
        btn_lyl.addWidget(ok_b)
        
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.setAlignment(QtCore.Qt.AlignCenter)
        mainlayout.addWidget(tabbox)
        mainlayout.addLayout(btn_lyl)
        
        self.get_settings()    
        self.setLayout(mainlayout)
        
        self.setWindowTitle(u"Beállítások")
        self.setWindowFlags(QtCore.Qt.Tool)
        
    def create_NWTab(self):
        wdg = QtGui.QWidget()
        lyl = QtGui.QGridLayout()
        odl_lb = QtGui.QLabel(u"Egy napos limit:")
        fdl_lb = QtGui.QLabel(u"Négy napos limit:")
        self.odl_sb = QtGui.QSpinBox()
        self.odl_sb.setMaximum(16000)
        self.odl_sb.setSingleStep(100)
        self.odl_sb.setSuffix(" MB")
        self.fdl_sb = QtGui.QSpinBox()
        self.fdl_sb.setMaximum(32000)
        self.fdl_sb.setSingleStep(100)
        self.fdl_sb.setSuffix(" MB")
        self.odl_sb.valueChanged.connect(self.setlimit_odr)
        self.fdl_sb.valueChanged.connect(self.setlimit_fdr)
        odr_lb = QtGui.QLabel(u"Egy napos újraindítási limit:")
        fdr_lb = QtGui.QLabel(u"Négy napos újraindítási limit:")
        self.odr_sb = QtGui.QSpinBox()
        self.odr_sb.setMaximum(16000)
        self.odr_sb.setSingleStep(100)
        self.odr_sb.setSuffix(" MB")
        self.fdr_sb = QtGui.QSpinBox()
        self.fdr_sb.setMaximum(32000)
        self.fdr_sb.setSingleStep(100)
        self.fdr_sb.setSuffix(" MB")
        
        ref_lb = QtGui.QLabel(u"Frissítési idő:")
        self.ref_sb = QtGui.QSpinBox()
        self.ref_sb.setMaximum(600)
        self.ref_sb.setMinimum(10)
        self.ref_sb.setSuffix(" Sec")
        
        lyl.addWidget(odl_lb,1,0)
        lyl.addWidget(fdl_lb,2,0)
        lyl.addWidget(self.odl_sb,1,1)
        lyl.addWidget(self.fdl_sb,2,1)
        lyl.addWidget(odr_lb,3,0)
        lyl.addWidget(fdr_lb,4,0)
        lyl.addWidget(self.odr_sb,3,1)
        lyl.addWidget(self.fdr_sb,4,1)
        lyl.addWidget(ref_lb,5,0)
        lyl.addWidget(self.ref_sb,5,1)
        wdg.setLayout(lyl)
        return wdg
    
    def setlimit_odr(self, value):
        self.odr_sb.setMaximum(int(value[:-2]))
        
    def setlimit_fdr(self, value):
        self.fdr_sb.setMaximum(int(value[:-2]))
    
    def create_uTTab(self):
        wdg = QtGui.QWidget()
        lyl = QtGui.QGridLayout()
        usr_lb = QtGui.QLabel(u"Felhasználó:")
        psw_lb = QtGui.QLabel(u"Jelszó:")
        url_lb = QtGui.QLabel(u"Host:")
        prt_lb = QtGui.QLabel(u"Port:")
        self.usr_lt = QtGui.QLineEdit()
        self.psw_lt = QtGui.QLineEdit()
        self.psw_lt.setEchoMode(QtGui.QLineEdit.Password)
        self.prt_lt = QtGui.QLineEdit()
        prt_val = QtGui.QIntValidator()
        prt_val.setRange(1,99999)
        self.prt_lt.setValidator(prt_val)
        self.prt_lt.setFixedWidth(60)
        self.url_lt = QtGui.QLineEdit()

        lyl.addWidget(url_lb,0,0)
        lyl.addWidget(self.url_lt,0,1)
        lyl.addWidget(prt_lb,1,0)
        lyl.addWidget(self.prt_lt,1,1)
        lyl.addWidget(usr_lb,2,0)
        lyl.addWidget(psw_lb,3,0)
        lyl.addWidget(self.usr_lt,2,1)
        lyl.addWidget(self.psw_lt,3,1)
        
        wdg.setLayout(lyl)
        return wdg
    
    def create_aTab(self):
        wdg = QtGui.QWidget()
        lyl = QtGui.QGridLayout()

        self.email_chk = QtGui.QCheckBox()
        self.email_chk.setText(u"E-mail küldése")
        self.email_chk.stateChanged.connect(self.enabledEmail)
        email_lb = QtGui.QLabel(u"E-mail cím:")
        self.email_lt = QtGui.QLineEdit()
        self.email_lt.setEnabled(False)
        self.de_chk = QtGui.QCheckBox()
        self.de_chk.setText(u"Deaktiválskor")
        self.de_chk.setEnabled(False)
        self.re_chk = QtGui.QCheckBox()
        self.re_chk.setEnabled(False)
        self.re_chk.setText(u"Reaktiváláskor")
        
        lyl.addWidget(self.email_chk,0,0)
        lyl.addWidget(email_lb,1,0)
        lyl.addWidget(self.email_lt,1,1)
        lyl.addWidget(self.de_chk,2,0)
        lyl.addWidget(self.re_chk,2,1)
        
        wdg.setLayout(lyl)
        return wdg
    
    def enabledEmail(self):
        self.email_lt.setEnabled(not self.email_lt.isEnabled())
        self.de_chk.setEnabled(not self.de_chk.isEnabled())
        self.re_chk.setEnabled(not self.re_chk.isEnabled())
        if self.email_chk.isChecked() == False:
            self.email_lt.clear()
            self.de_chk.setChecked(False)
            self.re_chk.setChecked(False)
            
    def get_settings(self):
        config = utils.getConfig()
        self.odl_sb.setValue(config["netwatcher"]["one_day_limit"])
        self.fdl_sb.setValue(config["netwatcher"]["four_day_limit"])
        self.odr_sb.setValue(config["netwatcher"]["reactivate_limit1"])
        self.fdr_sb.setValue(config["netwatcher"]["reactivate_limit4"])
        self.ref_sb.setValue(config["netwatcher"]["refresh_time"])
        self.email_chk.setChecked(config["general"]["send_email"])
        self.email_lt.setText(config["general"]["email_address"])
        self.de_chk.setChecked(config["general"]["deactive"])
        self.re_chk.setChecked(config["general"]["reactive"])
        auth = base64.decodestring(config["webui"]["auth"]).split(":")
        self.usr_lt.setText(auth[0])
        self.psw_lt.setText(auth[1])
        self.url_lt.setText(config["webui"]["url"])
        self.prt_lt.setText(str(config["webui"]["port"]))
        
    def set(self):
        config = utils.getConfig()
        config["netwatcher"]["one_day_limit"] = self.odl_sb.value()
        config["netwatcher"]["four_day_limit"] = self.fdl_sb.value()
        config["netwatcher"]["reactivate_limit1"] = self.odr_sb.value()
        config["netwatcher"]["reactivate_limit4"] = self.fdr_sb.value()
        config["netwatcher"]["refresh_time"] = self.ref_sb.value()
        config["webui"]["auth"] = base64.encodestring("%s:%s" % (self.usr_lt.text(), self.psw_lt.text()))
        config["webui"]["url"] = self.url_lt.text()
        config["webui"]["port"] = int(self.prt_lt.text())
        config["general"]["send_email"] = self.email_chk.isChecked()
        config["general"]["email_address"] = self.email_lt.text()
        config["general"]["deactive"] = self.de_chk.isChecked()
        config["general"]["reactive"] = self.re_chk.isChecked()
        utils.setConfig(config)
        self.close()
        
class MainWindow(QtGui.QWidget):
    forceSig = QtCore.Signal(bool)
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setObjectName("MainWindow")
        self.icon = QtGui.QIcon('icon.png')
        self.host_lb = QtGui.QLabel()
        self.win1_data_lb = QtGui.QLabel()
        self.win4_data_lb = QtGui.QLabel()
        self.win1_data_lb.setAlignment(QtCore.Qt.AlignRight)
        self.win4_data_lb.setAlignment(QtCore.Qt.AlignRight)
        self.status_lb = QtGui.QLabel(u"Sztátus:")
        self.createTrayIcon()
        self.conn = Connector(self.forceSig)
        self.conn.refreshed.connect(self.update)
        self.conn.statusSig.connect(self.setStatus) 
        self.conn.uconnected.connect(self.connectError)
        self.conn.start()
        
        layout = QtGui.QVBoxLayout()
        btn_lyl = QtGui.QHBoxLayout() 
        box = QtGui.QGroupBox()
        box.setTitle("Adatok")
        box.setLayout(self.createNWDataLayout())
        setting_bt = QtGui.QPushButton()
        setting_bt.setText(u"Beállítások")
        setting_bt.clicked.connect(self.settings)
        self.forcing_bt = QtGui.QPushButton()
        self.forcing_bt.setText(u"Megállít")
        self.forcing_bt.clicked.connect(self.forcing)
        btn_lyl.addSpacerItem(QtGui.QSpacerItem(0,0))
        btn_lyl.addWidget(setting_bt)
        btn_lyl.addWidget(self.forcing_bt)
        
        layout.addWidget(box)
        layout.addLayout(btn_lyl)
        
        self.setLayout(layout)
        self.setMinimumWidth(300)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle("Bitwatcher v0.10 BETA")
    
    def setStatus(self, status):
        self.status = status
        if self.status == 0:
            self.forcing_bt.setText(u"Erőltetett indítás")
            self.status_lb.setText(u"Szüneteltetve")
        elif self.status == 1:
            self.forcing_bt.setText(u"Erőltetett szüneteltetés")
            self.status_lb.setText(u"Seedel")
        elif self.status == 2:
            self.forcing_bt.setText(u"Erőltetés vége")
            self.status_lb.setText(u"Erőltetett szünet")
        elif self.status == 3:
            self.forcing_bt.setText(u"Erőltetés vége")
            self.status_lb.setText(u"Erőltetett seed")
    
    def forcing(self):
        if self.status == 0 or self.status == 1:
            self.forceSig.emit(True)
        elif self.status == 2 or self.status == 3:
            self.forceSig.emit(False)
    
    def connectError(self, conn):
        if not conn:
            self.tray.showMessage("Kapcsolat hiba", u"A Bitwatcher nem tud csatlakozni a uTorrenthez. Ellenőrizd a beállításokat!")
      
    def createNWDataLayout(self):
        lyl = QtGui.QGridLayout()
        win1_text_lb = QtGui.QLabel(u"Egy napos forgalom:")
        win4_text_lb = QtGui.QLabel(u"Négy napos frogalom:")
        
        lyl.addWidget(self.host_lb,0,0)
        lyl.addWidget(win1_text_lb,1,0)
        lyl.addWidget(win4_text_lb,2,0)
        
        lyl.addWidget(self.win1_data_lb,1,1)
        lyl.addWidget(self.win4_data_lb,2,1)
        lyl.addWidget(self.status_lb,3,0)
        return lyl
    
    def quit(self):
        self.conn.stop()
        QtGui.qApp.quit()
        
    def trayActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.show()
            self.activateWindow()
        
    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addSeparator()
        quit = QtGui.QAction(u"&Kilép", self)
        forcing = QtGui.QAction(u"&Erőltet", self)
        forcing.triggered.connect(self.forcing)
        quit.triggered.connect(self.quit)
        sett = QtGui.QAction(u"&Beállít", self)
        sett.triggered.connect(self.settings)
        self.trayIconMenu.addAction(sett)
        self.trayIconMenu.addAction(forcing)
        self.trayIconMenu.addAction(quit)
        self.tray = QtGui.QSystemTrayIcon(self)
        self.tray.setContextMenu(self.trayIconMenu)
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self.tray.activated.connect(self.trayActivated)
    
    def settings(self):
        settings = SettingsWindow()
        settings.open()
        settings.exec_()
        
    def getConverted(self, byte):
        if isinstance(byte, int) or isinstance(byte, long):
            if byte < 1024:
                return "%d B" % byte
            elif byte < 1024**2:
                return "%.2f KB" % (byte/1024.0)
            elif byte < 1024**3:
                return "%.2f MB" % (byte/1024.0**2)
            elif byte < 1024**4:
                return "%.2f GB" % (byte/1024.0**3)
        else:
            return byte
        
    def update(self, data):
        if not data['error']:
            limit1 = self.getConverted(data['window1day']['current'])
            limit4 = self.getConverted(data['window4day']['current'])
        else:
            limit1 = "Hiba"
            limit4 = "Hiba" 
        self.host_lb.setText("Host : %s" % data['host'])
        self.win1_data_lb.setText(limit1)
        self.win4_data_lb.setText(limit4)
        self.tray.setToolTip("%s / 16 GB, %s / 32 GB" % (limit1, limit4))

if __name__ == '__main__':
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    app = QtGui.QApplication(sys.argv)
    css = open("style.css", "r")
    app.setStyleSheet(css.read())
    css.close()
    w = MainWindow()
    sys.exit(app.exec_())