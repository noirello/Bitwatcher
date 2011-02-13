# -*- coding: UTF-8 -*-
import os
import sys
import json
import psutil
import win32com.client

CONFIG_FILE = "config"

PROCESS_NAME = sys.argv[0][sys.argv[0].rfind('\\')+1:]

def isExecuting():
    for pid in psutil.process_iter():
        if pid.name == PROCESS_NAME:
            return True
    return False

def getConfig():
    """ A config file betöltése. """
    f = open(CONFIG_FILE, "r")
    conf = json.load(f)
    f.close()
    return conf

def setConfig(obj):
    """ A config file módosítása. """
    f = open(CONFIG_FILE, "w")
    json.dump(obj ,f)
    f.close()

def createShortcut():
    wScriptShellObject = win32com.client.Dispatch("WScript.Shell")
    shortcutName = unicode("%s\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\bitwatcher.lnk" % os.environ['APPDATA'], "utf8")
    shortcut = wScriptShellObject.CreateShortcut(shortcutName)
    shortcut.TargetPath = sys.argv[0] #"D:/Development/Projects/bitwatcher/src/dist/bitwatcher.exe"
    shortcut.WorkingDirectory = sys.argv[0][0:sys.argv[0].rfind('\\')] #"D:/Development/Projects/bitwatcher/src/dist"
    #IconLocation
    shortcut.Save()