from Screens.Screen import Screen
from Screens.Standby import Standby, TryQuitMainloop
from Components.Label import Label
from Components.config import config, ConfigBoolean
import socket
from Tools.Directories import fileExists
from urllib2 import Request, urlopen, URLError, HTTPError
from random import randint
from enigma import eEPGCache, eDVBDB
from os import system
config.misc.deliteepgpop = ConfigBoolean(default=True)

class DeliteInterface:

    def __init__(self):
        self.session = None

    def setSession(self, session):
        self.session = session
        self.pop = self.session.instantiateDialog(Nab_debOut)

    def procCmd(self, cmd):
        if cmd is not None:
            if self.session:
                if cmd.find('extepg') == 0:
                    self.downloadExtEpg(cmd)
                elif cmd.find('reloadsettings') == 0:
                    self.reloadSettings()
                elif cmd.find('standby') == 0:
                    self.session.open(Standby)
                elif cmd.find('shutdown') == 0:
                    self.session.open(TryQuitMainloop, 1)
                elif cmd.find('reboot') == 0:
                    self.session.open(TryQuitMainloop, 2)
                elif cmd.find('restartenigma2') == 0:
                    self.session.open(TryQuitMainloop, 3)
                elif cmd.find('re2') == 0:
                    self.session.open(TryQuitMainloop, 3)
                elif cmd.find('restartemu') == 0:
                    mydata = 'START_CAMD'
                    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    client_socket.connect('/tmp/Blackhole.socket')
                    client_socket.send(mydata)
                    client_socket.close()
                elif cmd.find('popshow') == 0:
                    if config.misc.deliteepgpop.value:
                        self.pop.show()
                        self.pop.setmyText(cmd[8:])
                        self.pop.mystate = 1
                elif cmd.find('popsettext') == 0:
                    if config.misc.deliteepgpop.value:
                        self.pop.setmyText(cmd[11:])
                elif cmd.find('popclose') == 0:
                    if self.pop.mystate == 1:
                        self.pop.hide()

    def reloadSettings(self):
        settings = eDVBDB.getInstance()
        settings.reloadServicelist()
        settings.reloadBouquets()

    def downloadExtEpg(self, cmd):
        parts = cmd.split(',')
        myurl = parts[2]
        myext = '.gz'
        if myurl.find('.dat.bz2') != -1:
            myext = '.bz2'
        myepgpath = config.misc.epgcache_filename.value
        myepgfile = myepgpath + myext
        randurl = self.selecturL()
        myurl0 = myurl.replace('http://www.vuplus-community.net/rytec', randurl)
        online = self.checkOnLine(myurl0)
        if online == True:
            myurl = myurl0
        try:
            filein = urlopen(myurl)
        except HTTPError as e:
            pass
        except URLError as e:
            pass
        else:
            fileout = open(myepgfile, 'wb')
            while True:
                bytes = filein.read(1024000)
                fileout.write(bytes)
                if bytes == '':
                    break

            filein.close()
            fileout.close()

        if fileExists(myepgfile):
            cmd = 'gunzip -f ' + myepgfile
            if myext == '.bz2':
                cmd = 'bunzip2 -f ' + myepgfile
            rc = system(cmd)
            epgcache = eEPGCache.getInstance()
            epgcache.load()
            epgcache.save()

    def checkOnLine(self, url):
        try:
            filein = urlopen(url, timeout=1)
        except URLError as e:
            online = False
        except HTTPError as e:
            online = False
        else:
            filein.close()
            online = True

        return online

    def selecturL(self):
        url = 'http://www.xmltvepg.nl'
        nm = randint(1, 3)
        if nm == 2:
            url = 'http://www.xmltvepg.be'
        elif nm == 3:
            url = 'http://enigma2.world-of-satellite.com/epg_data'
        return url


class Nab_debOut(Screen):
    skin = '\n\t<screen position="380,150" size="520,240" title="Black Hole Message">\n\t\t<widget name="outlabel" position="10,10" size="500,230" font="Regular;20" halign="center" valign="center" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['outlabel'] = Label('')
        self.mystate = 0

    def setmyText(self, myt):
        self['outlabel'].setText(myt)

    def MyClose(self):
        self.close()
