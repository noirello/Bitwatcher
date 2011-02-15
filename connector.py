# -*- coding: UTF-8 -*-
import json
import urllib2
import time
from PySide import QtCore

import uwebapi
import utils

class Connector(QtCore.QThread):
    """ Kapcsolatok kezelése, külön szálban"""
    
    #Signalok deklaráléása - alapból az __init__()-en kívül kell, mert egyébként nem működik 
    refreshed = QtCore.Signal(dict)
    uconnected = QtCore.Signal(bool)
    statusSig = QtCore.Signal(int)
    
    def __init__(self, forceSig):
        QtCore.QThread.__init__(self)
        self.api = uwebapi.uWebAPI()
        self.data = None
        self.stopped = False
        self.forced = False
        forceSig.connect(self.forcing)
    
    def run(self):
        """
            Az adatok ismétlődő lekérdezése. 
            Az adatokat a self.refreshed signallal kerülnek átadásra.
        """
        config = utils.getConfig()
        checking_u = True 
        while not self.stopped:
            try:
                src = urllib2.urlopen(config["netwatcher"]["src"]).read()
                self.data = json.loads(src)
                if self.data['error'] == "false":
                    self.data['error'] = False
                    self.data['window1day']['current'] = int(self.data['window1day']['current'])
                    self.data['window4day']['current'] = int(self.data['window4day']['current'])
                    self.checking_transfer()
                    self.refreshed.emit(self.data)
                    #Kapcsolattesztelés minden 2. körben.
                    if checking_u: 
                        self.checking_connect()
                        checking_u = False
                    else:
                        checking_u = True
                else:
                    raise Exception()
            except:
                    self.refreshed.emit({'error' : True})
            time.sleep(config["netwatcher"]["refresh_time"])
    
    
    def checking_connect(self):
        """ A uTorrent webes kapcsolatának ellenőrzése."""
        self.api.set_authentication()
        try:
            self.api.get_torrents()
            self.uconnected.emit(True)
        except uwebapi.ConnectionError:
            self.uconnected.emit(False)
    
    def checking_transfer(self):
        """ A forgalomkorlátok, státuszok ellenőrzése."""
        config = utils.getConfig()
        if not self.forced:
            if (self.data['window1day']['current'] >= config["netwatcher"]["one_day_limit"]*1024**2) or (self.data['window4day']['current'] >= config["netwatcher"]["four_day_limit"]*1024**2):
                try:
                    self.api.deactivate()
                    self.status = 0
                except uwebapi.ConnectionError:
                    self.uconnected.emit(False)
            elif (self.data['window1day']['current'] <= config["netwatcher"]["reactivate_limit1"]*1024**2) or (self.data['window4day']['current'] <= config["netwatcher"]["reactivate_limit4"]*1024**2):
                try:
                    self.api.reactivate()
                    self.status = 1
                except uwebapi.ConnectionError:
                    self.uconnected.emit(False)
        else:
            if self.status == 1 or self.status == 2:
                try:
                    self.api.deactivate()
                    self.status = 2
                except uwebapi.ConnectionError:
                    self.uconnected.emit(False)
            if self.status == 0:
                try:
                    self.api.reactivate()
                    self.status = 3
                except uwebapi.ConnectionError:
                    self.uconnected.emit(False)
        self.statusSig.emit(self.status)
    
    def forcing(self, frc):
        """ Erőltetett státusz beállítása."""
        self.forced = frc
        self.checking_transfer()
    
    def stop(self):
        """ A szál leállítása."""
        self.stopped = True
        self.terminate()
        self.exit()