from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock, NoSave, configfile
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_SKIN_IMAGE
from os import system, listdir, remove as os_remove, rename as os_rename, popen, getcwd, chdir
from BhUtils import DeliteGetSkinPath, nab_Detect_Machine, BhU_get_Version
from enigma import eTimer
from Screens.Console import Console
from Screens.VirtualKeyBoard import VirtualKeyBoard
import time
import datetime

class DeliteSettings(Screen):
    skin = '\n\t<screen position="160,110" size="390,360" title="Black Hole Settings">\n\t\t<widget source="list" render="Listbox" position="10,10" size="370,330" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                \t\tMultiContentEntryText(pos = (60, 1), size = (300, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                \t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                \t\t],\n                \t\t"fonts": [gFont("Regular", 24)],\n                \t\t"itemHeight": 36\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        self.sel = self.sel[2]
        if self.sel == 0:
            self.session.open(BhSpeedUp)
        elif self.sel == 1:
            self.session.open(DeliteCronMang)
        elif self.sel == 2:
            self.session.open(DeliteSetupOSD2)
        elif self.sel == 3:
            from BHDevice import BHDevicesPanel
            self.session.open(BHDevicesPanel)
        elif self.sel == 4:
            from Screens.Setup import Setup
            self.session.open(Setup, 'subtitlesetup')
        elif self.sel == 5:
            from Screens.Setup import Setup
            self.session.open(Setup, 'autolanguagesetup')
        elif self.sel == 6:
            self.session.open(Bp_UsbFormat)
        elif self.sel == 7:
            from Screens.ParentalControlSetup import ParentalControlSetup
            self.session.open(ParentalControlSetup)
        elif self.sel == 8:
            self.session.open(DeliteKernelModules)
        elif self.sel == 9:
            from BhInadyn import DeliteInadyn
            self.session.open(DeliteInadyn)
        elif self.sel == 10:
            from BhSwap import DeliteSwap
            self.session.open(DeliteSwap)
        elif self.sel == 11:
            from BhHdd import DeliteHdd
            self.session.open(DeliteHdd)
        elif self.sel == 12:
            from BhNet import DeliteOpenvpn
            self.session.open(DeliteOpenvpn)
        elif self.sel == 13:
            from BhNet import DeliteSamba
            self.session.open(DeliteSamba)
        elif self.sel == 14:
            from BhNet import BhNfsServer
            self.session.open(BhNfsServer)
        elif self.sel == 15:
            from BhNet import DeliteTelnet
            self.session.open(DeliteTelnet)
        elif self.sel == 16:
            from BhNet import DeliteFtp
            self.session.open(DeliteFtp)
        elif self.sel == 17:
            if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DLNABrowser/plugin.py'):
                self.session.open(MessageBox, _('Please enable this application in BlackHole Speed Up panel to continue.'), MessageBox.TYPE_INFO)
            else:
                from Plugins.Extensions.DLNABrowser.plugin import DLNADeviceBrowser
                self.session.open(DLNADeviceBrowser)
        elif self.sel == 18:
            if not fileExists('/usr/bin/mediatomb'):
                self.session.open(MessageBox, _('Please enable this application in BlackHole Speed Up panel to continue.'), MessageBox.TYPE_INFO)
            else:
                from BhNet import BhMediatomb
                self.session.open(BhMediatomb)
        elif self.sel == 19:
            if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DLNAServer/plugin.py'):
                self.session.open(MessageBox, _('Please enable this application in BlackHole Speed Up panel to continue.'), MessageBox.TYPE_INFO)
            else:
                from Plugins.Extensions.DLNAServer.plugin import DLNAServer
                self.session.open(DLNAServer)
        elif self.sel == 20:
            from BhNet import BhPcsc
            self.session.open(BhPcsc)
        elif self.sel == 21:
            from BhNet import BhTunerServer
            self.session.open(BhTunerServer)
        elif self.sel == 22:
            from BhNet import BhNetBrowser
            self.session.open(BhNetBrowser)
        else:
            self.noYet()

    def noYet(self):
        nobox = self.session.open(MessageBox, _('Function Not Yet Available'), MessageBox.TYPE_INFO)
        nobox.setTitle(_('Info'))

    def updateList(self):
        self.list = []
        mypath = DeliteGetSkinPath()
        mypixmap = mypath + 'icons/infopanel_osd.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Speed Up')
        idx = 0
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_cron.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Cron Manager')
        idx = 1
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_osd.png'
        png = LoadPixmap(mypixmap)
        name = _('Osd Settings')
        idx = 2
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_space.png'
        png = LoadPixmap(mypixmap)
        name = _('Devices Manager')
        idx = 3
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_osd.png'
        png = LoadPixmap(mypixmap)
        name = _('Subtitle Settings')
        idx = 4
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_osd.png'
        png = LoadPixmap(mypixmap)
        name = _('Auto Language Selection Settings')
        idx = 5
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/swapsettings.png'
        png = LoadPixmap(mypixmap)
        name = _('Usb Format Wizard')
        idx = 6
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_osd.png'
        png = LoadPixmap(mypixmap)
        name = _('Parental Control')
        idx = 7
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_kmod.png'
        png = LoadPixmap(mypixmap)
        name = _('Kernel Modules Manager')
        idx = 8
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/inadynsettings.png'
        png = LoadPixmap(mypixmap)
        name = _('Inadyn Settings')
        idx = 9
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/swapsettings.png'
        png = LoadPixmap(mypixmap)
        name = _('Swap File Settings')
        idx = 10
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/hdsettings.png'
        png = LoadPixmap(mypixmap)
        name = _('Hard Disk Settings')
        idx = 11
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_vpn.png'
        png = LoadPixmap(mypixmap)
        name = _('OpenVpn Panel')
        idx = 12
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_samba.png'
        png = LoadPixmap(mypixmap)
        name = _('Samba/Cifs Panel')
        idx = 13
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_nfs.png'
        png = LoadPixmap(mypixmap)
        name = _('Nfs Server Panel')
        idx = 14
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_telnet.png'
        png = LoadPixmap(mypixmap)
        name = _('Telnet Panel')
        idx = 15
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_ftp.png'
        png = LoadPixmap(mypixmap)
        name = _('Ftp Panel')
        idx = 16
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_samba.png'
        png = LoadPixmap(mypixmap)
        name = _('UPnP Client Djmount')
        idx = 17
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_samba.png'
        png = LoadPixmap(mypixmap)
        name = _('UPnP Server Mediatomb')
        idx = 18
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_samba.png'
        png = LoadPixmap(mypixmap)
        name = _('UPnP Server Minidlna')
        idx = 19
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_samba.png'
        png = LoadPixmap(mypixmap)
        name = _('Pcsc Panel')
        idx = 20
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/infopanel_samba.png'
        png = LoadPixmap(mypixmap)
        name = _('Tuner Server')
        idx = 21
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/mountwizard.png'
        png = LoadPixmap(mypixmap)
        name = _('Network Browse & Mountpoints')
        idx = 22
        res = (name, png, idx)
        self.list.append(res)
        self['list'].list = self.list


class DeliteSetupOSD2(Screen):
    skin = '\n\t<screen position="339,190" size="602,340" title="Black Hole Osd Settings">\n\t\t<widget name="lsinactive" position="10,20" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lsactive" position="10,20" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lab1" position="50,20" size="260,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lbinactive" position="10,70" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lbactive" position="10,70" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lab2" position="50,70" size="550,50" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lpinactive" position="10,130" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lpactive" position="10,130" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lab4" position="50,130" size="260,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lzinactive" position="10,130" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lzactive" position="10,130" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lab5" position="50,130" size="260,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lcinactive" position="10,130" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lcactive" position="10,130" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>\n\t\t<widget name="lab6" position="50,130" size="260,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab3" position="10,180" size="320,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labsize" position="330,180" size="30,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on"/>\n\t\t<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Disable Light Infobar on Zap'))
        self['lsinactive'] = Pixmap()
        self['lsactive'] = Pixmap()
        self['lab2'] = Label(_('Enable Panic Button 0 (zap to 1 & clear zap history)'))
        self['lbinactive'] = Pixmap()
        self['lbactive'] = Pixmap()
        self['lab4'] = Label(_('Show Infobar on Event Change'))
        self['lpinactive'] = Pixmap()
        self['lpactive'] = Pixmap()
        self['lab5'] = Label(_('Hide Zap Errors'))
        self['lzinactive'] = Pixmap()
        self['lzactive'] = Pixmap()
        self['lab6'] = Label(_('Hide CI Messages'))
        self['lcinactive'] = Pixmap()
        self['lcactive'] = Pixmap()
        self['lab3'] = Label(_('Hide Infobar Timeout in sec.:'))
        self['labsize'] = Label('')
        self['key_red'] = Label(_('Setup'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.setupmyosd})
        self.onLayoutFinish.append(self.updatemyinfo)

    def updatemyinfo(self):
        self['lsinactive'].hide()
        self['lsactive'].hide()
        self['lbinactive'].hide()
        self['lbactive'].hide()
        self['lpinactive'].hide()
        self['lpactive'].hide()
        self['lzinactive'].hide()
        self['lzactive'].hide()
        self['lcinactive'].hide()
        self['lcactive'].hide()
        if config.misc.deliteeinfo.value:
            self['lsactive'].show()
        else:
            self['lsinactive'].show()
        if config.misc.delitepanicb.value:
            self['lbactive'].show()
        else:
            self['lbinactive'].show()
        if config.usage.show_infobar_on_event_change.value:
            self['lpactive'].show()
        else:
            self['lpinactive'].show()
        if config.usage.hide_zap_errors.value:
            self['lzactive'].show()
        else:
            self['lzinactive'].show()
        if config.usage.hide_ci_messages.value:
            self['lcactive'].show()
        else:
            self['lcinactive'].show()
        myt = '5'
        idx = config.usage.infobar_timeout.index
        if idx:
            myt = str(idx)
        self['labsize'].setText(myt)

    def setupmyosd(self):
        self.session.openWithCallback(self.updatemyinfo, DeliteSetupOSDConf2)


class DeliteSetupOSDConf2(Screen, ConfigListScreen):
    skin = '\n\t<screen position="339,190" size="602,340" title="Black Hole OSD Setup">\n\t\t<widget name="config" position="10,10" size="580,200" scrollbarMode="showOnDemand"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on"/>\n\t\t<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.saveMyosd,
         'back': self.close})
        self.updateList()

    def updateList(self):
        self.deliteeinfo = NoSave(ConfigYesNo(default='False'))
        self.delitepanicb = NoSave(ConfigYesNo(default='False'))
        self.show_infobar_on_event_change = NoSave(ConfigYesNo(default='False'))
        self.hide_zap_errors = NoSave(ConfigYesNo(default='False'))
        self.hide_ci_messages = NoSave(ConfigYesNo(default='False'))
        self.infobar_timeout = NoSave(ConfigSelection(default='5', choices=[('0', _('no timeout')),
         ('1', '1 ' + _('second')),
         ('2', '2 ' + _('seconds')),
         ('3', '3 ' + _('seconds')),
         ('4', '4 ' + _('seconds')),
         ('5', '5 ' + _('seconds')),
         ('6', '6 ' + _('seconds')),
         ('7', '7 ' + _('seconds')),
         ('8', '8 ' + _('seconds')),
         ('9', '9 ' + _('seconds')),
         ('10', '10 ' + _('seconds'))]))
        self.deliteeinfo.value = config.misc.deliteeinfo.value
        self.delitepanicb.value = config.misc.delitepanicb.value
        self.show_infobar_on_event_change.value = config.usage.show_infobar_on_event_change.value
        self.hide_zap_errors.value = config.usage.hide_zap_errors.value
        self.hide_ci_messages.value = config.usage.hide_ci_messages.value
        self.infobar_timeout.value = config.usage.infobar_timeout.value
        osd_ei = getConfigListEntry(_('Disable Light Infobar on Zap'), self.deliteeinfo)
        self.list.append(osd_ei)
        osd_panic = getConfigListEntry(_('Enable Panic Button 0'), self.delitepanicb)
        self.list.append(osd_panic)
        res = getConfigListEntry(_('Show Infobar on Event Change'), self.show_infobar_on_event_change)
        self.list.append(res)
        res = getConfigListEntry(_('Hide Zap Errors'), self.hide_zap_errors)
        self.list.append(res)
        res = getConfigListEntry(_('Hide CI Messages'), self.hide_ci_messages)
        self.list.append(res)
        infobar_timeout = getConfigListEntry(_('Hide Infobar Timeout in sec.'), self.infobar_timeout)
        self.list.append(infobar_timeout)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def saveMyosd(self):
        config.misc.deliteeinfo.value = self.deliteeinfo.value
        config.misc.delitepanicb.value = self.delitepanicb.value
        config.usage.show_infobar_on_event_change.value = self.show_infobar_on_event_change.value
        config.usage.hide_zap_errors.value = self.hide_zap_errors.value
        config.usage.hide_ci_messages.value = self.hide_ci_messages.value
        config.usage.infobar_timeout.value = self.infobar_timeout.value
        config.misc.deliteeinfo.save()
        config.misc.delitepanicb.save()
        config.usage.show_infobar_on_event_change.save()
        config.usage.hide_zap_errors.save()
        config.usage.hide_ci_messages.save()
        config.usage.infobar_timeout.save()
        self.close()


class DeliteCronMang(Screen):
    skin = '\n\t<screen position="240,120" size="800,520" title="Black Hole Cron Manager">\n\t\t<widget source="list" render="Listbox" position="10,10" size="780,460" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n    \t\t<ePixmap pixmap="skin_default/buttons/red.png" position="200,480" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,480" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="200,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_yellow" position="440,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n    \t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Add'))
        self['key_yellow'] = Label(_('Delete'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.addtocron,
         'yellow': self.delcron})
        self.updateList()

    def addtocron(self):
        self.session.openWithCallback(self.updateList, DeliteSetupCronConf)

    def updateList(self):
        self.list = []
        if fileExists('/etc/bhcron/root'):
            f = open('/etc/bhcron/root', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                line2 = 'Time: ' + parts[1] + ':' + parts[0] + '\t' + 'Command: ' + line[line.rfind('*') + 1:]
                res = (line2, line)
                self.list.append(res)

            f.close()
        self['list'].list = self.list

    def delcron(self):
        mysel = self['list'].getCurrent()
        if mysel:
            myline = mysel[1]
            out = open('/etc/bhcron/bh.cron', 'w')
            f = open('/etc/bhcron/root', 'r')
            for line in f.readlines():
                if line != myline:
                    out.write(line)

            f.close()
            out.close()
            if fileExists('/etc/cron/crontabs/root'):
               print("/etc/cron/crontabs/root exists")
            else:
               rc = system('ln -sfn /etc/bhcron/root /etc/cron/crontabs/root')
            rc = system('crontab /etc/bhcron/bh.cron -c /etc/bhcron/')
            self.updateList()


class DeliteSetupCronConf(Screen, ConfigListScreen):
    skin = '\n\t<screen position="240,190" size="800,340" title="Black Hole Cron Setup">\n\t\t<widget name="config" position="10,20" size="780,280" scrollbarMode="showOnDemand" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="330,270" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="330,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.checkentry,
         'back': self.close,
         'green': self.vkeyb})
        self.updateList()

    def updateList(self):
        self.cmdtime = NoSave(ConfigClock(default=0))
        self.default_command = NoSave(ConfigSelection(default='None', choices=[('None', _('None')),
         ('/usr/bin/Blackholecmd standby', _('standby')),
         ('/usr/bin/Blackholecmd shutdown', _('shutdown')),
         ('/usr/bin/Blackholecmd reboot', _('reboot')),
         ('/usr/bin/Blackholecmd restartenigma2', _('restartgui')),
         ('/usr/bin/Blackholecmd restartemu', _('restartemu'))]))
        self.user_command = NoSave(ConfigText(fixed_size=False))
        self.cmdtime.value = mytmpt = [0, 0]
        self.default_command.value = 'None'
        self.user_command.value = ''
        res = getConfigListEntry(_('Time to execute command or script'), self.cmdtime)
        self.list.append(res)
        res = getConfigListEntry(_('Predefined Command to execute'), self.default_command)
        self.list.append(res)
        res = getConfigListEntry(_('Custom Command'), self.user_command)
        self.list.append(res)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def vkeyb(self):
        sel = self['config'].getCurrent()
        if sel:
            self.vkvar = sel[0]
            self.vki = self['config'].getCurrentIndex()
            value = 'xmeo'
            if self.vki == 2:
                value = self.user_command.value
                if value == 'None':
                    value = ''
            if value != 'xmeo':
                self.session.openWithCallback(self.UpdateAgain, VirtualKeyBoard, title=self.vkvar, text=value)
            else:
                self.session.open(MessageBox, 'Please use Virtual Keyboard for text rows only (e.g. Custom Command)', MessageBox.TYPE_INFO)

    def UpdateAgain(self, newt):
        self.list = []
        if newt is None or newt == '':
            newt = 'None'
        self.user_command.value = newt
        res = getConfigListEntry(_('Time to execute command or script'), self.cmdtime)
        self.list.append(res)
        res = getConfigListEntry(_('Predefined Command to execute'), self.default_command)
        self.list.append(res)
        res = getConfigListEntry(_('Custom Command'), self.user_command)
        self.list.append(res)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def checkentry(self):
        msg = ''
        if self.user_command.value == 'None':
            self.user_command.value = ''
        if self.default_command.value == 'None' and self.user_command.value == '':
            msg = _('You must set at least one Command')
        if self.default_command.value != 'None' and self.user_command.value != '':
            msg = _('Entering a Custom command you have to set Predefined command: None ')
        if msg:
            self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
        else:
            self.saveMycron()

    def saveMycron(self):
        hour = '%02d' % self.cmdtime.value[0]
        minutes = '%02d' % self.cmdtime.value[1]
        if self.default_command.value != 'None':
            command = self.default_command.value
        else:
            command = self.user_command.value
        newcron = minutes + ' ' + hour + ' * * * ' + command.strip() + '\n'
        out = open('/etc/bhcron/bh.cron', 'w')
        if fileExists('/etc/bhcron/root'):
            f = open('/etc/bhcron/root', 'r')
            for line in f.readlines():
                out.write(line)

            f.close()
        out.write(newcron)
        out.close()
        if fileExists('/etc/cron/crontabs/root'):
           print("/etc/cron/crontabs/root exists")
        else:
           rc = system('ln -sfn /etc/bhcron/root /etc/cron/crontabs/root')
        rc = system('crontab /etc/bhcron/bh.cron -c /etc/bhcron/')
        self.close()


class DeliteDevicesPanel(Screen):
    skin = '\n\t<screen position="240,100" size="800,560" title="Black Hole Devices Manager">\n\t\t<widget source="list" render="Listbox" position="10,0" size="780,510" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t{"template": [\n              \t\t MultiContentEntryText(pos = (90, 0), size = (690, 30), font=0, text = 0),\n               \t\t MultiContentEntryText(pos = (110, 30), size = (670, 50), font=1, flags = RT_VALIGN_TOP, text = 1),\n               \t\t MultiContentEntryPixmapAlphaTest(pos = (0, 0), size = (80, 80), png = 2),\n                \t],\n                \t"fonts": [gFont("Regular", 24),gFont("Regular", 20)],\n                \t"itemHeight": 85\n                \t}\n            \t\t</convert>\n\t\t</widget>\n\t\t<widget name="lab1" zPosition="2" position="50,40" size="700,40" font="Regular;24" halign="center" transparent="1"/>\n    \t\t<ePixmap pixmap="skin_default/buttons/red.png" position="200,524" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,524" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="200,520" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_yellow" position="440,520" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n    \t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Mountpoints'))
        self['key_yellow'] = Label(_('Cancel'))
        self['lab1'] = Label(_('Wait please while scanning your devices...'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.mountUmount,
         'yellow': self.close})
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateList2)
        if not pathExists('/universe'):
            createDir('/universe')
        self.updateList()

    def updateList(self):
        self.activityTimer.start(10)

    def updateList2(self):
        self.activityTimer.stop()
        self.list = []
        self.conflist = []
        rc = system('blkid > /tmp/ninfo2.log')
        f = open('/tmp/ninfo2.log', 'r')
        for line in f.readlines():
            if line.find('/dev/sd') == -1:
                continue
            parts = line.strip().split()
            device = parts[0][5:-2]
            partition = parts[0][5:-1]
            pos = line.find('UUID') + 6
            end = line.find('"', pos)
            uuid = line[pos:end]
            dtype = self.get_Dtype(device)
            category = dtype[0]
            png = LoadPixmap(dtype[1])
            size = self.get_Dsize(device, partition)
            model = self.get_Dmodel(device)
            mountpoint = self.get_Dpoint(uuid, partition)
            name = '%s: %s' % (category, model)
            description = _(' device: %s  size: %s\n mountpoint: %s' % (parts[0], size, mountpoint))
            self.list.append((name, description, png))
            description = '%s  %s  %s' % (name, size, partition)
            self.conflist.append((description, uuid))

        self['list'].list = self.list
        self['lab1'].hide()

    def get_Dtype(self, device):
        mypath = DeliteGetSkinPath()
        name = 'USB'
        pix = mypath + 'icons/dev_usb.png'
        filename = '/sys/block/%s/removable' % device
        if fileExists(filename):
            if file(filename).read().strip() == '0':
                name = 'HARD DRIVE'
                pix = mypath + 'icons/dev_hdd.png'
        return (name, pix)

    def get_Dsize(self, device, partition):
        size = '0'
        filename = '/sys/block/%s/%s/size' % (device, partition)
        if fileExists(filename):
            size = int(file(filename).read().strip())
            cap = size / 1000 * 512 / 1000
            size = '%d.%03d GB' % (cap / 1000, cap % 1000)
        return size

    def get_Dmodel(self, device):
        model = 'Generic'
        filename = '/sys/block/%s/device/vendor' % device
        if fileExists(filename):
            vendor = file(filename).read().strip()
            filename = '/sys/block/%s/device/model' % device
            mod = file(filename).read().strip()
            model = '%s %s' % (vendor, mod)
        return model

    def get_Dpoint(self, uid, partition):
        point = _('NOT MAPPED')
        device = '/dev/' + partition
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find(uid) != -1 or line.find(device) != -1:
                parts = line.strip().split()
                point = parts[1]
                break

        f.close()
        return point

    def mountUmount(self):
        self.session.openWithCallback(self.updateList, DeliteSetupDevicePanelConf, self.conflist)


class DeliteSetupDevicePanelConf(Screen, ConfigListScreen):
    skin = '\n\t<screen position="center,center" size="902,340" title="Black Hole Devices Mountpoints Setup">\n\t\t<widget name="config" position="30,10" size="840,275" scrollbarMode="showOnDemand"/>\n\t\t<widget name="Linconn" position="30,285" size="840,20" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="200,300" size="140,40" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="550,300" size="140,40" alphatest="on"/>\n\t\t<widget name="key_red" position="200,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t\t<widget name="key_green" position="550,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t</screen>'

    def __init__(self, session, devices):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['key_green'] = Label(_('Cancel'))
        self['Linconn'] = Label(_('Wait please while scanning your box devices...'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.saveMypoints,
         'green': self.close,
         'back': self.close})
        self.devices = devices
        self.updateList()

    def updateList(self):
        self.list = []
        mounts = []
        meoboot = False
        if pathExists('/media/meoboot'):
            meoboot = True
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            mounts.append(line)

        f.close()
        for device in self.devices:
            uid = device[1]
            d1 = _('Not mapped')
            for line in mounts:
                if line.find(uid) != -1:
                    parts = line.strip()
                    d1 = parts[1].split()
                    break

            item = NoSave(ConfigSelection(default='Not mapped', choices=self.get_Choices()))
            mymeo = d1 + '/MbootM/.meoboot'
            if fileExists(mymeo) and meoboot == True:
                item = NoSave(ConfigSelection(default=d1, choices=[(d1, 'meoboot')]))
            item.value = d1.strip()
            text = device[0]
            res = getConfigListEntry(text, item, uid)
            self.list.append(res)

        self['config'].list = self.list
        self['config'].l.setList(self.list)
        self['Linconn'].hide()

    def get_Choices(self):
        choices = [('Not mapped', _('Not mapped'))]
        folders = listdir('/media')
        for f in folders:
            if f == 'net' or f == 'ram' or f == 'realroot' or f == 'union' or f == 'meoboot':
                continue
            c = '/media/' + f
            choices.append((c, c))

        choices.append(('/universe', '/universe'))
        return choices

    def saveMypoints(self):
        f = open('/etc/fstab', 'r')
        out = open('/etc/fstab.tmp', 'w')
        for line in f.readlines():
            if line.find('by-uuid') != -1 or len(line) < 6:
                continue
            if line.find('/dev/sda1') != -1:
                continue
            if line.find('UUID=') != -1:
                continue
            out.write(line)

        for x in self['config'].list:
            if x[1].value == 'Not mapped' or x[1].value == '/media/meoboot':
                continue
            line = 'UUID=%s    %s    auto   defaults    0  0\n' % (x[2], x[1].value)
            out.write(line)

        out.write('\n')
        f.close()
        out.close()
        os_rename('/etc/fstab.tmp', '/etc/fstab')
        message = _('Device changes need a system restart to take effect.\nRestart your Box now ?')
        self.session.openWithCallback(self.restBo, MessageBox, message, MessageBox.TYPE_YESNO)

    def restBo(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 2)
        else:
            self.close()


class Bp_UsbFormat(Screen):
    skin = '\n\t<screen position="center,center" size="580,350" title="Black Hole Usb Format Wizard">\n\t\t<widget name="lab1" position="10,10" size="560,280" font="Regular;20" valign="top" transparent="1"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="100,300" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="340,300" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="100,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="340,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        #msg = _('This wizard will help you to format Usb mass storage devices for Linux.\n')
        #msg += _('Please be sure that your usb drive is NOT CONNECTED to your Dreambox box before you continue.\n')
        #msg += _('If your usb drive is connected and mounted you have to poweroff your box, remove the usb device and reboot.\n')
        #msg += _('Press Red button to continue, when you are ready and your usb is disconnected.\n')
        msg = _('Press Red button to continue, when you are ready and your usb is connected.\n')
        self['key_red'] = Label(_('Continue ->'))
        self['key_green'] = Label(_('Cancel'))
        self['lab1'] = Label(msg)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.checkClose,
         'red': self.step_Bump,
         'green': self.checkClose})
# skip setup 1 and 2
#        self.step = 1
        self.step = 3
        self.devices = []
        self.device = None
        self.totalpartitions = 1
        self.totalsize = self.p1size = self.p2size = self.p3size = self.p4size = '0'
        self.canclose = True

    def stepOne(self):
        msg = _('Connect your usb storage to your Dreambox box\n')
        msg += _('Press Red button to continue when ready.\n\n')
        msg += _('Warning: If your usb is already connected\n')
        msg += _('to the box you have to unplug it, press\n')
        msg += _('the Green button and restart the wizard.\n')
        rc = system('/etc/init.d/autofs stop')
        self.devices = self.get_Devicelist()
        self['lab1'].setText(msg)
        self.step = 2

    def stepTwo(self):
        msg = _('The wizard will now try to identify your connected usb device.')
        msg += _('Press Red button to continue.')
        self['lab1'].setText(msg)
        self.step = 3

    def stepThree(self):
        newdevices = self.get_Devicelist()
        for d in newdevices:
            if d not in self.devices:
                self.device = d

        if self.device is None:
            self.wizClose(_('Sorry, no new usb storage device detected.\nBe sure to follow the wizard instructions.'))
        else:
            msg = self.get_Deviceinfo(self.device)
            self['lab1'].setText(msg)
            self.step = 4

    def stepFour(self):
        myoptions = [['1', '1'],
         ['2', '2'],
         ['3', '3'],
         ['4', '4']]
        self.session.openWithCallback(self.partSize1, ChoiceBox, title=_('Select number of partitions:'), list=myoptions)

    def partSize1(self, total):
        self.totalpartitions = int(total[1])
        if self.totalpartitions > 1:
            self.session.openWithCallback(self.partSize2, InputBox, title=_('Enter the size in Megabyte of the first partition:'), windowTitle=_('Partition size'), text='1', useableChars='1234567890')
        else:
            self.writePartFile()

    def partSize2(self, psize):
        if psize is None:
            psize = '100'
        self.p1size = psize
        if self.totalpartitions > 2:
            self.session.openWithCallback(self.partSize3, InputBox, title=_('Enter the size in Megabyte of the second partition:'), windowTitle=_('Partition size'), text='1', useableChars='1234567890')
        else:
            self.writePartFile()

    def partSize3(self, psize):
        if psize is None:
            psize = '100'
        self.p2size = psize
        if self.totalpartitions > 3:
            self.session.openWithCallback(self.partSize4, InputBox, title=_('Enter the size in Megabyte of the third partition:'), windowTitle=_('Partition size'), text='1', useableChars='1234567890')
        else:
            self.writePartFile()

    def partSize4(self, psize):
        if psize is None:
            psize = '100'
        self.p3size = psize
        self.writePartFile()

    def writePartFile(self):
        p1 = p2 = p3 = p4 = '0'
        device = '/dev/' + self.device
        out0 = '#!/bin/sh\n\nsfdisk %s << EOF\n' % device
        msg = _('Total Megabyte Available: \t') + str(self.totalsize)
        msg += _('\nPartition scheme:\n')
        p1 = self.p1size
        out1 = ',%s\n' % self.p1size
        if self.totalpartitions == 1:
            p1 = str(self.totalsize)
            out1 = ';\n'
        msg += '%s1 \t size:%s M\n' % (device, p1)
        if self.totalpartitions > 1:
            p2 = self.p2size
            out2 = ',%s\n' % self.p2size
            if self.totalpartitions == 2:
                p2 = self.totalsize - int(self.p1size)
                out2 = ';\n'
            msg += '%s2 \t size:%s M\n' % (device, p2)
        if self.totalpartitions > 2:
            p3 = self.p3size
            out3 = ',%s\n' % self.p3size
            if self.totalpartitions == 3:
                p3 = self.totalsize - (int(self.p1size) + int(self.p2size))
                out3 = ';\n'
            msg += '%s3 \t size:%s M\n' % (device, p3)
        if self.totalpartitions > 3:
            p4 = self.totalsize - (int(self.p1size) + int(self.p2size) + int(self.p3size))
            out4 = ';\n'
            msg += '%s4 \t size:%s M\n' % (device, p4)
        msg += _('\nWarning: all the data will be lost.\nAre you sure you want to format this device?\n')
        out = open('/tmp/sfdisk.tmp', 'w')
        out.write(out0)
        out.write(out1)
        if self.totalpartitions > 1:
            out.write(out2)
        if self.totalpartitions > 2:
            out.write(out3)
        if self.totalpartitions > 3:
            out.write(out4)
        out.write('EOF\n')
        out.close()
        system('chmod 0755 /tmp/sfdisk.tmp')
        self['lab1'].setText(msg)
        if int(self.p1size) + int(self.p2size) + int(self.p3size) + int(self.p4size) > self.totalsize:
            self.wizClose(_('Sorry, your partition(s) sizes are bigger than total device size.'))
        else:
            self.step = 5

    def do_Part(self):
        self.canclose = False
        self['key_green'].hide()
        device = '/dev/%s' % self.device
        cmd = "echo -e 'Partitioning: %s \n\n'" % device
        cmd2 = '/tmp/sfdisk.tmp'
        self.session.open(Console, title=_('Partitioning...'), cmdlist=[cmd, cmd2], finishedCallback=self.partDone)

    def partDone(self):
        msg = _('The device has been partitioned.\nPartitions will be now formatted.')
        self['lab1'].setText(msg)
        self.step = 6

    def choiceBoxFstype(self):
        menu = []
        menu.append((_('ext2 - recommended for USB flash memory'), 'ext2'))
        menu.append((_('ext3 - recommended for harddrives'), 'ext3'))
        menu.append((_('ext4 - DM800 No support'), 'ext4'))
        menu.append((_('vfat - use only for media-files'), 'vfat'))
        self.session.openWithCallback(self.choiceBoxFstypeCB, ChoiceBox, title=_('Choice filesystem.'), list=menu)

    def choiceBoxFstypeCB(self, choice):
        if choice is None:
            return
        newfstype = choice[1]
        if newfstype == 'ext4':
            self.formatcmd = '/sbin/mkfs.ext4 -F -O extent,flex_bg,large_file,uninit_bg -m1'
        elif newfstype == 'ext3':
            self.formatcmd = '/sbin/mkfs.ext3 -F -m0'
        elif newfstype == 'ext2':
            self.formatcmd = '/sbin/mkfs.ext2 -F -m0'
        elif newfstype == 'vfat':
            self.formatcmd = '/usr/sbin/mkfs.vfat'
        self.do_Format()

    def do_Format(self):
        os_remove('/tmp/sfdisk.tmp')
        cmds = ['sleep 1']
        device = '/dev/%s1' % self.device
        cmd = '%s %s' % (self.formatcmd, device)
        cmds.append(cmd)
        if self.totalpartitions > 1:
            device = '/dev/%s2' % self.device
            cmd = '%s %s' % (self.formatcmd, device)
            cmds.append(cmd)
        if self.totalpartitions > 2:
            device = '/dev/%s3' % self.device
            cmd = '%s %s' % (self.formatcmd, device)
            cmds.append(cmd)
        if self.totalpartitions > 3:
            device = '/dev/%s4' % self.device
            cmd = '%s %s' % (self.formatcmd, device)
            cmds.append(cmd)
        self.session.open(Console, title=_('Formatting...'), cmdlist=cmds, finishedCallback=self.succesS)

    def step_Bump(self):
        if self.step == 1:
            self.stepOne()
        elif self.step == 2:
            self.stepTwo()
        elif self.step == 3:
            self.stepThree()
        elif self.step == 4:
            self.stepFour()
        elif self.step == 5:
            self.do_Part()
        elif self.step == 6:
            self.choiceBoxFstype()

    def get_Devicelist(self):
        devices = []
        folder = listdir('/sys/block')
        for f in folder:
            if f.find('sd') != -1:
                devices.append(f)

        return devices

    def get_Deviceinfo(self, device):
        info = vendor = model = size = ''
        filename = '/sys/block/%s/device/vendor' % device
        if fileExists(filename):
            vendor = file(filename).read().strip()
            filename = '/sys/block/%s/device/model' % device
            model = file(filename).read().strip()
            filename = '/sys/block/%s/size' % device
            size = int(file(filename).read().strip())
            cap = size / 1000 * 512 / 1024
            size = '%d.%03d GB' % (cap / 1000, cap % 1000)
            self.totalsize = cap
        info = _('Model: ') + vendor + ' ' + model + '\n' + _('Size: ') + size + '\n' + _('Device: ') + '/dev/' + device
        return info

    def checkClose(self):
        if self.canclose == True:
            self.close()

    def wizClose(self, msg):
        self.session.openWithCallback(self.close, MessageBox, msg, MessageBox.TYPE_INFO)

    def succesS(self):
        mybox = self.session.open(MessageBox, _("Foramted finish.\nYou can mount your Usb now.\nPress ok to continue"), MessageBox.TYPE_INFO)
        self.close()
# Remove reboot command
#        mybox = self.session.openWithCallback(self.hreBoot, MessageBox, _("The Box will be now restarted to generate a new device UID.\nDon't forget to remap your device after the reboot.\nPress ok to continue"), MessageBox.TYPE_INFO)

    def hreBoot(self, answer):
        self.session.open(TryQuitMainloop, 2)


class DeliteKernelModules(Screen, ConfigListScreen):
    skin = '\n\t<screen position="240,190" size="800,340" title="Black Hole Extra Kernel Modules Setup">\n\t\t<widget name="config" position="10,20" size="780,280" scrollbarMode="showOnDemand" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="200,293" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,293" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="200,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_yellow" position="446,290" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['key_yellow'] = Label(_('Active Modules'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.saveMyconf,
         'yellow': self.showMod,
         'back': self.close})
        self.updateList()

    def showMod(self):
        self.session.open(DeliteKernelModShow)

    def updateList(self):
        self.ftdi_sio = NoSave(ConfigYesNo(default=False))
        self.pl2303 = NoSave(ConfigYesNo(default=False))
        self.tun = NoSave(ConfigYesNo(default=False))
        if fileExists('/usr/bin/bhextramod'):
            f = open('/usr/bin/bhextramod', 'r')
            for line in f.readlines():
                if line.find('ftdi_sio') != -1:
                    self.ftdi_sio.value = True
                elif line.find('pl2303') != -1:
                    self.pl2303.value = True
                elif line.find('tun') != -1:
                    self.tun.value = True

            f.close()
        res = getConfigListEntry(_('Smargo & other Usb card readers chipset ftdi:'), self.ftdi_sio)
        self.list.append(res)
        res = getConfigListEntry(_('Other Usb card readers chipset pl2303:'), self.pl2303)
        self.list.append(res)
        res = getConfigListEntry(_('Tun module needed for Openvpn:'), self.tun)
        self.list.append(res)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def saveMyconf(self):
        l1 = ''
        l2 = ''
        l3 = ''
        l4 = ''
        if self.ftdi_sio.value == True:
            l2 = 'modprobe ftdi_sio'
            system(l2)
        else:
            system('rmmod ftdi_sio')
        if self.pl2303.value == True:
            l3 = 'modprobe pl2303'
            system(l3)
        else:
            system('rmmod pl2303')
        if self.tun.value == True:
            l4 = 'modprobe tun'
            system(l4)
        else:
            system('rmmod tun')
        out = open('/usr/bin/bhextramod', 'w')
        out.write('#!/bin/sh\n')
        if l1 != '':
            out.write(l1 + '\n')
        if l2 != '':
            out.write(l2 + '\n')
        if l3 != '':
            out.write(l3 + '\n')
        if l4 != '':
            out.write(l4 + '\n')
        out.close()
        system('chmod 0755 /usr/bin/bhextramod')
        self.close()


class DeliteKernelModShow(Screen):
    skin = '\n\t<screen position="339,160" size="602,410" title="Active Kernel Modules">\n\t\t<widget source="list" render="Listbox" position="10,10" size="580,320" zPosition="1" scrollbarMode="showOnDemand" transparent="1">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\tMultiContentEntryText(pos = (10, 2), size = (570, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n\t\t\t\t],\n\t\t\t\t"fonts": [gFont("Regular", 24)],\n\t\t\t\t"itemHeight": 30\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\n\t\t<widget name="statuslab" position="10,340" size="580,70" font="Regular;20" valign="center" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-3,-3" shadowColor="black"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self['list'].onSelectionChanged.append(self.schanged)
        self['statuslab'] = Label('')
        self.updateList()
        self['actions'] = ActionMap(['WizardActions'], {'ok': self.close,
         'back': self.close})
        self.onLayoutFinish.append(self.refr_sel)

    def refr_sel(self):
        self['list'].index = 1
        self['list'].index = 0

    def updateList(self):
        rc = system('lsmod > /tmp/ninfo.tmp')
        strview = ''
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'Module':
                    continue
                res = (parts[0], line)
                self.list.append(res)

            f.close()
            os_remove('/tmp/ninfo.tmp')
            self['list'].list = self.list

    def schanged(self):
        mysel = self['list'].getCurrent()
        if mysel:
            mytext = mysel[1]
            parts = mytext.split()
            size = parts[1]
            pos = len(parts[0]) + len(parts[1])
            used = mytext[pos:]
            mytext = _('Module size: ') + size + _(' bytes\n') + _('Module used by: ') + used
            self['statuslab'].setText(mytext)


class BhSpeedUp(Screen, ConfigListScreen):
    skin = '\n\t<screen position="center,center" size="902,570" title="Black Hole Speed Up">\n\t\t<widget name="lab1" position="10,10" size="882,60" font="Regular;20" valign="top" transparent="1"/>\n\t\t<widget name="config" position="30,70" size="840,450" scrollbarMode="showOnDemand"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="200,530" size="140,40" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="550,530" size="140,40" alphatest="on"/>\n\t\t<widget name="key_red" position="200,530" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t\t<widget name="key_green" position="550,530" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t</screen>'

    def __init__(self, session, firstrun = False):
        Screen.__init__(self, session)
        self.firstrun = firstrun
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['lab1'] = Label(_('Retrieving data ...'))
        self['key_red'] = Label(_('Save'))
        self['key_green'] = Label(_('Cancel'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.saveMypoints,
         'green': self.close,
         'back': self.close})
        self.pluglist = [['BhWeather', 'bhweather'],
         ['BhFullBackup', 'bhfullbackup'],
         ['BhPersonalBackup', 'bhpersonalbackup'],
         ['BhEpgBackup', 'bhepgbackup'],
         ['Meoboot', 'enigma2-plugin-extensions-meoboot'],
         ['FlashExpander', 'enigma2-plugin-extensions-flashexpander'],
         ['dflash BlackHole', 'enigma2-plugin-extensions-dflash'],
         ['AutoResolution', 'enigma2-plugin-systemplugins-autoresolution'],
         ['CommonInterfaceAssignment', 'enigma2-plugin-systemplugins-commoninterfaceassignment'],
         ['AddStreamUrl', 'enigma2-plugin-extensions-addstreamurl'],
         ['PicturePlayer', 'enigma2-plugin-extensions-pictureplayer'],
         ['MyTube', 'enigma2-plugin-extensions-mytube'],
         ['YouTube', 'enigma2-plugin-extensions-youtube'],
         ['RemoteChannelStreamConverter', 'enigma2-plugin-extensions-remotestreamconvert'],
         ['StreamTV', 'enigma2-plugin-extensions-streamtv'],
         ['AutoShutDown', 'enigma2-plugin-systemplugins-autoshutdown'],
         ['CrossEPG', 'enigma2-plugin-systemplugins-crossepg'],
         ['xmodem', 'enigma2-plugin-extensions-xmodem'],
         ['UI3DSetup', 'enigma2-plugin-systemplugins-ui3dsetup'],
         ['UIPositionSetup', 'enigma2-plugin-systemplugins-uipositionsetup'],
         ['DLNABrowser', 'enigma2-plugin-extensions-dlnabrowser'],
         ['DLNAServer', 'enigma2-plugin-extensions-dlnaserver'],
         ['Mediatomb', 'enigma2-plugin-extensions-mediatomb'],
         ['WirelessAccessPoint', 'enigma2-plugin-systemplugins-wirelessaccesspoint'],
         ['DVDPlayer', 'enigma2-plugin-extensions-dvdplayer'],
         ['HBBTV', 'enigma2-plugin-extensions-hbbtv'],
         ['OpenOpera Browser', 'enigma2-plugin-extensions-openopera']]
        machine = nab_Detect_Machine()
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateFeed2)
        self.updateFeed()

    def updateFeed(self):
        self.activityTimer.start(3)

    def updateFeed2(self):
        self.activityTimer.stop()
        ret = system('opkg update')
        self.updateList()

    def updateList(self):
        self.list = []
        if fileExists('/tmp/bhspeed.tmp'):
            os_remove('/tmp/bhspeed.tmp')
        for plug in self.pluglist:
            cmd = 'opkg status %s >> /tmp/bhspeed.tmp' % plug[1]
            system(cmd)

        for plug in self.pluglist:
            item = NoSave(ConfigSelection(default='Enabled', choices=[('Enabled', _('Enabled')), ('Disabled', _('Disabled'))]))
            installed = self.checkInst(plug[1])
            if installed == True:
                item.value = 'Enabled'
            else:
                item.value = 'Disabled'
            res = getConfigListEntry(plug[0], item)
            self.list.append(res)

        self['config'].list = self.list
        self['config'].l.setList(self.list)
        self['lab1'].setText(_("Please disable ALL the plugins you don't need to use.\nThis will Speed Up Image Performance."))

    def checkInst(self, name):
        ret = False
        f = open('/tmp/bhspeed.tmp', 'r')
        for line in f.readlines():
            if line.find(name) != -1:
                ret = True
                break

        f.close()
        return ret

    def saveMypoints(self):
        self.mycmdlist = []
        for x in self['config'].list:
            cmd = self.buildcoM(x[0], x[1].value)
            if cmd != '':
                self.mycmdlist.append(cmd)
                if cmd == 'opkg remove --force-depends --force-remove enigma2-plugin-extensions-openopera':
                    self.mycmdlist.append('opkg remove --force-depends --force-remove OpenOpera')
                    self.mycmdlist.append('rm -rf /usr/local/hbb-browser')

        if len(self.mycmdlist) > 0:
            self.session.open(Console, title=_('Black Hole Speed Up'), cmdlist=self.mycmdlist, finishedCallback=self.allDone)
        else:
            self.close()

    def buildcoM(self, name, what):
        cmd = ''
        for plug in self.pluglist:
            if plug[0] == name:
                installed = self.checkInst(plug[1])
                if what == 'Enabled' and installed == False:
                    cmd = 'opkg --force-overwrite install %s' % plug[1]
                elif what == 'Disabled' and installed == True:
                    cmd = 'opkg remove --force-depends --force-remove %s' % plug[1]
                break

        return cmd

    def allDone(self):
        if self.firstrun == True:
            self.close()
        else:
            mybox = self.session.openWithCallback(self.close, MessageBox, _('Make Enigma2 restart for the changes to take effect.\nPress ok to continue'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))

    def hrestEn(self, answer):
        self.session.open(TryQuitMainloop, 3)
