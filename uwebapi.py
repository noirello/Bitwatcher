# -*- coding: UTF-8 -*-
import cookielib
import json
import re
import urllib2

import utils

class ConnectionError(Exception):
    """ 
        Általános kapcsolódási hiba. 
        Minden esetben ilyen típusú hibával tér vissza a uWebAPI osztály.
    """
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

class uWebAPI:
    """
        A uTorrent vezérlése a webes API-n keresztül. Támogatja a token alapú azonosítás. 
        Az azonosításhoz szükséges adatokat a CONFIG_FILE-ból nyeri.
    """
    def __init__(self):
        self.token = ""
        self.set_authentication()
    
    def set_authentication(self):
        """ Az azonosításhoz szükséges fejléc és a cookie tárolásához szükséges tároló beállítása."""
        config = utils.getConfig()
        self.headers =  {"Authorization" : "Basic %s" % config["webui"]["auth"]}
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.url = "%s:%d/gui" % (config["webui"]["url"], config["webui"]["port"]) 
    
    def request_token(self):
        """ Új token igénylése."""
        req = urllib2.Request("%s/token.html" % self.url, None, self.headers)
        try:
            data = self.opener.open(req).read()
        except urllib2.URLError:
            raise ConnectionError("Cannot request token at %s" % self.url)
        p = re.compile(r"<.*?>")
        self.token =  p.sub("", data) 
                        
    def get_torrents(self):
        """ A torrent lista lekérdezése. """
        self.request_token()
        req = urllib2.Request("%s/?token=%s&list=1" % (self.url, self.token), None, self.headers)
        try:
            resp = self.opener.open(req).read()
            return json.loads(resp)['torrents']
        except urllib2.URLError:
            raise ConnectionError("Cannot get the torrent list.")
    
    def action(self, cmd, hash):
        """
            A cmd típusú művelet végrehajtása az adot hash kódú torrenten.
        """
        req = urllib2.Request("%s/?token=%s&action=%s&hash=%s" % (self.url, self.token, cmd, hash), None, self.headers)
        try:
            self.opener.open(req)
        except urllib2.HTTPError as e:
            if e.code == 400:
                self.request_token()
                self.action(cmd, hash)
            else:
                raise ConnectionError("Cannot do the action %s, on the %s hash coded torrent." % (cmd, hash) )
        return True
    
    def deactivate(self):
        """ Minden aktív torrent megállítása. """
        config = utils.getConfig()
        for i in self.get_torrents():
            if i[1]&1 == 1:
                config["torrents"].append(i[0])
                self.action("stop", i[0])
        utils.setConfig(config)
        
    def reactivate(self):
        """ A megállított torrentek elindítása. """
        config = utils.getConfig()
        while len(config["torrents"]):
            self.action("start", config["torrents"].pop())
        utils.setConfig(config)