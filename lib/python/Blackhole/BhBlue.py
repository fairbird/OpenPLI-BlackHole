from Screens.Screen import Screen
from enigma import iServiceInformation, eTimer
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.Pixmap import MultiPixmap
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigText, getConfigListEntry, ConfigSelection, NoSave
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from ServiceReference import ServiceReference
from os import system, listdir, chdir, getcwd, rename as os_rename
from BhEpgPanel import DeliteEpgPanel
from BhSettings import DeliteSettings
from BhInfo import DeliteInfo
from BhUtils import BhU_get_Version, BhU_check_proc_version
import socket
config.delite = ConfigSubsection()
config.delite.fp = ConfigText(default='')

class DeliteBluePanel(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('xx CAMs Installed'))
        self['lab2'] = Label(_('Set Default CAM'))
        self['lab3'] = Label(_('Active CAM'))
        self['Ilab1'] = Label()
        self['Ilab2'] = Label()
        self['Ilab3'] = Label()
        self['Ilab4'] = Label()
        self['key_red'] = Label(_('Epg Panel'))
        self['key_green'] = Label(_('Autocam'))
        self['key_yellow'] = Label(_('Sys Info'))
        self['key_blue'] = Label(_('Extra Settings'))
        self['activecam'] = Label()
        self['Ecmtext'] = ScrollLabel()
        self.emlist = []
        self.populate_List()
        self['list'] = MenuList(self.emlist)
        totcam = str(len(self.emlist))
        self['lab1'].setText(totcam + '   ' + _('CAMs Installed'))
        self.onShow.append(self.updateBP)
        self['myactions'] = ActionMap(['ColorActions', 'OkCancelActions', 'DirectionActions'], {'ok': self.keyOk,
         'cancel': self.close,
         'green': self.autoCam,
         'red': self.keyRed,
         'yellow': self.nInfo,
         'blue': self.Settings,
         'up': self['Ecmtext'].pageUp,
         'down': self['Ecmtext'].pageDown}, -1)

    def nInfo(self):
        self.session.open(DeliteInfo)

    def Settings(self):
        self.session.open(DeliteSettings)

    def autoCam(self):
        self.session.open(DeliteAutocamMan)

    def keyRed(self):
        self.session.open(DeliteEpgPanel)

    def populate_List(self):
        self.camnames = {}
        cams = listdir('/usr/camscript')
        for fil in cams:
            if fil.find('Ncam_') != -1:
                f = open('/usr/camscript/' + fil, 'r')
                for line in f.readlines():
                    if line.find('CAMNAME=') != -1:
                        line = line.strip()
                        cn = line[9:-1]
                        self.emlist.append(cn)
                        self.camnames[cn] = '/usr/camscript/' + fil

                f.close()

        if fileExists('/etc/BhCamConf') == False:
            out = open('/etc/BhCamConf', 'w')
            out.write('delcurrent|/usr/camscript/Ncam_Ci.sh\n')
            out.write('deldefault|/usr/camscript/Ncam_Ci.sh\n')
            out.close()

    def updateBP(self):
        name = 'N/A'
        provider = 'N/A'
        aspect = 'N/A'
        videosize = 'N/A'
        myserviceinfo = ''
        myservice = self.session.nav.getCurrentService()
        if myservice is not None:
            myserviceinfo = myservice.info()
            if self.session.nav.getCurrentlyPlayingServiceReference():
                name = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
            provider = self.getServiceInfoValue(iServiceInformation.sProvider, myserviceinfo)
            aspect = self.getServiceInfoValue(iServiceInformation.sAspect, myserviceinfo)
            if aspect in (1, 2, 5, 6, 9, 10, 13, 14):
                aspect = '4:3'
            else:
                aspect = '16:9'
            if myserviceinfo:
                width = myserviceinfo and myserviceinfo.getInfo(iServiceInformation.sVideoWidth) or -1
                height = myserviceinfo and myserviceinfo.getInfo(iServiceInformation.sVideoHeight) or -1
                if width != -1 and height != -1:
                    videosize = '%dx%d' % (width, height)
        self['Ilab1'].setText(_('Name: ') + name)
        self['Ilab2'].setText(_('Provider: ') + provider)
        self['Ilab3'].setText(_('Aspect Ratio: ') + aspect)
        self['Ilab4'].setText(_('Videosize: ') + videosize)
        self.currentcam = '/usr/camscript/Ncam_Ci.sh'
        self.defaultcam = '/usr/camscript/Ncam_Ci.sh'
        f = open('/etc/BhCamConf', 'r')
        for line in f.readlines():
            parts = line.strip().split('|')
            if parts[0] == 'delcurrent':
                self.currentcam = parts[1]
            elif parts[0] == 'deldefault':
                self.defaultcam = parts[1]

        f.close()
        defCamname = 'Common Interface'
        curCamname = 'Common Interface'
        for c in self.camnames.keys():
            if self.camnames[c] == self.defaultcam:
                defCamname = c
            if self.camnames[c] == self.currentcam:
                curCamname = c

        pos = 0
        for x in self.emlist:
            if x == defCamname:
                self['list'].moveToIndex(pos)
                break
            pos += 1

        mytext = ''
        if fileExists('/tmp/ecm.info'):
            f = open('/tmp/ecm.info', 'r')
            for line in f.readlines():
                line = line.replace('\n', '')
                line = line.strip()
                if len(line) > 3:
                    mytext = mytext + line + '\n'

            f.close()
        if len(mytext) < 5:
            mytext = '\n\n    ' + _('Ecm Info not available.')
        self['activecam'].setText(curCamname)
        self['Ecmtext'].setText(mytext)

    def getServiceInfoValue(self, what, myserviceinfo):
        if myserviceinfo is None:
            return ''
        else:
            v = myserviceinfo.getInfo(what)
            if v == -2:
                v = myserviceinfo.getInfoString(what)
            elif v == -1:
                v = 'N/A'
            return v

    def keyOk(self):
        self.sel = self['list'].getCurrent()
        self.newcam = self.camnames[self.sel]
        inme = open('/etc/BhCamConf', 'r')
        out = open('/etc/BhCamConf.tmp', 'w')
        for line in inme.readlines():
            if line.find('delcurrent') == 0:
                line = 'delcurrent|' + self.newcam + '\n'
            elif line.find('deldefault') == 0:
                line = 'deldefault|' + self.newcam + '\n'
            out.write(line)

        out.close()
        inme.close()
        os_rename('/etc/BhCamConf.tmp', '/etc/BhCamConf')
        out = open('/etc/CurrentBhCamName', 'w')
        out.write(self.sel)
        out.close()
        cmd = 'cp -f ' + self.newcam + ' /usr/bin/StartBhCam'
        system(cmd)
        mydata = 'STOP_CAMD,' + self.currentcam
        client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client_socket.connect('/tmp/Blackhole.socket')
        client_socket.send(mydata)
        client_socket.close()
        mydata = 'NEW_CAMD,' + self.newcam
        client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client_socket.connect('/tmp/Blackhole.socket')
        client_socket.send(mydata)
        client_socket.close()
        self.session.openWithCallback(self.myclose, Nab_DoStartCam, self.sel)

    def checkKern(self):
        mycheck = 0
        deversion = BhU_get_Version()
        if deversion == BhU_check_proc_version():
            mycheck = 1
        else:
            nobox = self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash Black Hole image v.  ') + deversion, MessageBox.TYPE_INFO)
            nobox.setTitle(_('Info'))
            self.myclose()
        return mycheck

    def myclose(self):
        self.close()


class Nab_DoStartCam(Screen):
    skin = '\n\t<screen position="390,100" size="484,250" title="Black Hole" flags="wfNoBorder">\n\t\t<widget name="connect" position="0,0" size="484,250" zPosition="-1" pixmaps="skin_default/startcam_1.png,skin_default/startcam_2.png,skin_default/startcam_3.png,skin_default/startcam_4.png" transparent="1" />\n\t\t<widget name="lab1" position="10,180" halign="center" size="460,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />\n\t</screen>'

    def __init__(self, session, title):
        Screen.__init__(self, session)
        msg = _('Please wait while starting\n') + title + '...'
        self['connect'] = MultiPixmap()
        self['lab1'] = Label(msg)
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updatepix)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)

    def startShow(self):
        self.curpix = 0
        self.count = 0
        self['connect'].setPixmapNum(0)
        self.activityTimer.start(10)

    def updatepix(self):
        self.activityTimer.stop()
        if self.curpix > 2:
            self.curpix = 0
        if self.count > 7:
            self.curpix = 3
        self['connect'].setPixmapNum(self.curpix)
        if self.count == 20:
            self.hide()
            self.close()
        self.activityTimer.start(140)
        self.curpix += 1
        self.count += 1

    def delTimer(self):
        del self.activityTimer


class DeliteAutocamMan(Screen):
    skin = '\n\t<screen position="240,120" size="800,520" title="Black Hole Autocam Manager">\n\t\t<widget name="defaultcam" position="10,10" size="780,30" font="Regular;24" halign="center" valign="center" backgroundColor="#9f1313" />\n\t\t<widget source="list" render="Listbox" position="20,60" size="760,400" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n    \t\t<ePixmap pixmap="skin_default/buttons/red.png" position="200,480" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,480" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="200,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_yellow" position="440,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n    \t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Add'))
        self['key_yellow'] = Label(_('Delete'))
        self['defaultcam'] = Label(_('Default Cam:'))
        self.emlist = []
        self.camnames = {}
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.addtocam,
         'yellow': self.deltocam})
        self.updateList()

    def addtocam(self):
        self.session.openWithCallback(self.updateList, DeliteSetupAutocam)

    def updateList(self):
        self.list = []
        cams = listdir('/usr/camscript')
        for fil in cams:
            if fil.find('Ncam_') != -1:
                f = open('/usr/camscript/' + fil, 'r')
                for line in f.readlines():
                    if line.find('CAMNAME=') != -1:
                        line = line.strip()
                        cn = line[9:-1]
                        self.emlist.append(cn)
                        self.camnames[cn] = '/usr/camscript/' + fil

                f.close()

        f = open('/etc/BhCamConf', 'r')
        for line in f.readlines():
            parts = line.strip().split('|')
            if parts[0] == 'delcurrent':
                continue
            elif parts[0] == 'deldefault':
                defaultcam = self.GetCamName(parts[1])
                self['defaultcam'].setText(_('Default Cam:  ') + defaultcam)
            else:
                text = parts[2] + '\t' + self.GetCamName(parts[1])
                res = (text, parts[0])
                self.list.append(res)

        f.close()
        self['list'].list = self.list

    def GetCamName(self, cam):
        activeCam = ''
        for c in self.camnames.keys():
            if self.camnames[c] == cam:
                activeCam = c

        return activeCam

    def deltocam(self):
        mysel = self['list'].getCurrent()
        if mysel:
            mysel = mysel[1]
            out = open('/etc/BhCamConf.tmp', 'w')
            f = open('/etc/BhCamConf', 'r')
            for line in f.readlines():
                parts = line.strip().split('|')
                if parts[0] != mysel:
                    out.write(line)

            f.close()
            out.close()
            os_rename('/etc/BhCamConf.tmp', '/etc/BhCamConf')
            self.updateList()


class DeliteSetupAutocam(Screen, ConfigListScreen):
    skin = '\n\t<screen position="240,190" size="800,340" title="Black Hole Autocam Setup">\n\t\t<widget name="config" position="10,20" size="780,280" scrollbarMode="showOnDemand" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="330,270" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="330,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.saveMyconf,
         'back': self.close})
        self.updateList()

    def updateList(self):
        mychoices = []
        self.chname = 'Unknown'
        self.chref = 'Unknown'
        myservice = self.session.nav.getCurrentService()
        if myservice is not None:
            myserviceinfo = myservice.info()
            if self.session.nav.getCurrentlyPlayingServiceReference():
                self.chname = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
                self.chref = self.session.nav.getCurrentlyPlayingServiceReference().toString()
        cams = listdir('/usr/camscript')
        for fil in cams:
            if fil.find('Ncam_') != -1:
                f = open('/usr/camscript/' + fil, 'r')
                for line in f.readlines():
                    if line.find('CAMNAME=') != -1:
                        line = line.strip()
                        cn = line[9:-1]
                        cn2 = '/usr/camscript/' + fil
                        res = (cn2, cn)
                        mychoices.append(res)

                f.close()

        self.autocam_file = NoSave(ConfigSelection(choices=mychoices))
        res = getConfigListEntry(self.chname, self.autocam_file)
        self.list.append(res)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def saveMyconf(self):
        check = True
        f = open('/etc/BhCamConf', 'r')
        for line in f.readlines():
            parts = line.strip().split('|')
            if parts[0] == self.chref:
                check = False

        f.close()
        if check == True:
            line = self.chref + '|' + self.autocam_file.value + '|' + self.chname + '\n'
            out = open('/etc/BhCamConf', 'a')
            out.write(line)
            out.close()
        self.close()


class DeliteBp:

    def __init__(self):
        self['DeliteBp'] = ActionMap(['InfobarExtensions'], {'DeliteBpshow': self.showDeliteBp})

    def showDeliteBp(self):
        self.session.openWithCallback(self.callNabAction, DeliteBluePanel)

    def callNabAction(self, *args):
        if len(args):
            actionmap, context, action = args
            actionmap.action(context, action)
