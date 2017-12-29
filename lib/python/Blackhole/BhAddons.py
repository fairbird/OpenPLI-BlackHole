from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from enigma import eTimer, loadPic, eDVBDB
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigYesNo, ConfigSubsection, ConfigInteger, ConfigSelection, ConfigClock, NoSave
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Pixmap import Pixmap, MultiPixmap
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir
from os import system, listdir, chdir, getcwd, remove as os_remove
from urllib2 import Request, urlopen, URLError, HTTPError
from BhUtils import nab_strip_html, DeliteGetSkinPath, nab_Detect_Machine, BhU_get_Version
from operator import itemgetter
config.bhaddons = ConfigSubsection()
config.bhaddons.lock = ConfigYesNo(default=False)
config.bhaddons.pin = ConfigInteger(limits=(0, 9999), default=0)

class DeliteAddons(Screen):
    skin = '\n\t<screen position="160,115" size="390,330" title="Black Hole E2 Addons Manager">\n\t\t<widget source="list" render="Listbox" position="10,16" size="370,300" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t{"template": [\n                    \tMultiContentEntryText(pos = (50, 1), size = (320, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                 \tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                    \t],\n                    \t"fonts": [gFont("Regular", 22)],\n                    \t"itemHeight": 36\n                \t}\n            \t\t</convert>\n\t\t</widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        if not pathExists('/var/uninstall'):
            createDir('/var/uninstall')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.checkAcceSS,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = DeliteGetSkinPath()
        mypixmap = mypath + 'icons/addons_manager.png'
        png = LoadPixmap(mypixmap)
        name = _('Addons Download Manager')
        idx = 0
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabpackpanel.png'
        png = LoadPixmap(mypixmap)
        name = _('Online Feeds Settings update')
        idx = 1
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabpackpanel.png'
        png = LoadPixmap(mypixmap)
        name = _('Online Black Hole image update')
        idx = 2
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabpackpanel.png'
        png = LoadPixmap(mypixmap)
        name = _('Manual Install Bh packges')
        idx = 3
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/ipkpackpanel.png'
        png = LoadPixmap(mypixmap)
        name = _('Manual Install Ipk packges')
        idx = 4
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/uninstpanel.png'
        png = LoadPixmap(mypixmap)
        name = _('Addons Uninstall Panel')
        idx = 5
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/statpanel.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Statistics')
        idx = 6
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabpackpanel.png'
        png = LoadPixmap(mypixmap)
        name = _('Addons Parental Control')
        idx = 7
        res = (name, png, idx)
        self.list.append(res)
        self['list'].list = self.list

    def checkAcceSS(self):
        if config.bhaddons.lock.value == True:
            msg = _('Enter the pin')
            self.session.openWithCallback(self.checkAcceSS2, InputBox, title=msg, windowTitle=_('Insert Pin'), text='0000', useableChars='1234567890')
        else:
            self.KeyOk()

    def checkAcceSS2(self, pin):
        if pin is None:
            pin = 0
        if int(pin) == config.bhaddons.pin.value:
            self.KeyOk()
        else:
            self.session.open(MessageBox, _('Sorry, wrong pin.'), MessageBox.TYPE_ERROR)

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            self.session.open(Nab_downArea)
        elif self.sel == 1:
            self.session.open(Bh_Feed_Settings2)
        elif self.sel == 2:
            self.session.open(Bh_Feed_Upgrade)
        elif self.sel == 3:
            self.checkPanel()
        elif self.sel == 4:
            self.checkPanel2()
        elif self.sel == 5:
            self.session.open(Nab_uninstPanel)
        elif self.sel == 6:
            staturl = 'http://www.vuplus-community.net/bhaddons/index.php?op=outmestats2'
            downfile = '/tmp/cpanel.tmp'
            if fileExists(downfile):
                os_remove(downfile)
            self.session.openWithCallback(self.StatsDone, Nab_ConnectPop, staturl, downfile)
        elif self.sel == 7:
            self.session.open(addonsParentalConfig)
        else:
            nobox = self.session.open(MessageBox, _('Function Not Yet Available'), MessageBox.TYPE_INFO)
            nobox.setTitle(_('Info'))

    def StatsDone(self):
        downfile = '/tmp/cpanel.tmp'
        if fileExists(downfile):
            self.session.open(Nab_Stats)
        else:
            nobox = self.session.open(MessageBox, _('Sorry, Connection Failed.'), MessageBox.TYPE_INFO)

    def runUpgrade(self, result):
        if result:
            from Plugins.SystemPlugins.SoftwareManager.plugin import UpdatePlugin
            self.session.open(UpdatePlugin, '/usr/lib/enigma2/python/Plugins/SystemPlugins/SoftwareManager')

    def checkPanel(self):
        check = 0
        pkgs = listdir('/tmp')
        for fil in pkgs:
            if fil.find('.tgz') != -1:
                check = 1

        if check == 1:
            self.session.open(Nab_downPanel)
        else:
            mybox = self.session.open(MessageBox, _('Nothing to install.\nYou have to Upload a bh.tgz package in the /tmp directory before to install Addons'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))

    def checkPanel2(self):
        check = 0
        pkgs = listdir('/tmp')
        for fil in pkgs:
            if fil.find('.ipk') != -1:
                check = 1

        if check == 1:
            self.session.open(Nab_downPanelIPK)
        else:
            mybox = self.session.open(MessageBox, _('Nothing to install.\nYou have to Upload an ipk package in the /tmp directory before to install Addons'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))


class Nab_downArea(Screen):
    skin = '\n\t<screen position="160,115" size="390,330" title="Black Hole E2 Downloads Manager">\n\t\t<widget source="list" render="Listbox" position="10,15" size="370,280" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t{"template": [\n                   \tMultiContentEntryText(pos = (50, 1), size = (320, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                 \tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                    \t],\n                    \t"fonts": [gFont("Regular", 24)],\n                    \t"itemHeight": 36\n                \t}\n            \t\t</convert>\n\t\t</widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        if not pathExists('/var/uninstall'):
            createDir('/var/uninstall')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = DeliteGetSkinPath()
        mypixmap = mypath + 'icons/nabplugins.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Addons Plugins')
        idx = 1
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabplugins.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Feeds Plugins')
        idx = 2
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabskins.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Image Skins')
        idx = 3
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabscript.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Image Script')
        idx = 4
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nablangs.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Image Boot Logo')
        idx = 5
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabsettings.png'
        png = LoadPixmap(mypixmap)
        name = _('Black Hole Settings')
        idx = 6
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabpicons.png'
        png = LoadPixmap(mypixmap)
        name = _('Picons Packages')
        idx = 7
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/nabuploads.png'
        png = LoadPixmap(mypixmap)
        name = _('Latest 10 Uploads')
        idx = 8
        res = (name, png, idx)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        bh_version = BhU_get_Version()
        bh_version = int(bh_version.replace('.', ''))
        pluginver = 'Plugins'
        catver = 'outcat10_2'
        if bh_version > 199:
            pluginver = 'Plugins2'
            catver = 'outcat10_3'
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        box = nab_Detect_Machine()
        self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Cams'
        self.title = 'Buuuuu'
        if self.sel == 1:
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=' + pluginver
            self.title = 'Black Hole Addons Plugins'
        elif self.sel == 2:
            self.url = 'feeds'
            self.title = 'Black Hole Feeds Plugins'
        elif self.sel == 3:
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Skins'
            self.title = 'Black Hole Skins'
        elif self.sel == 4:
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Scripts'
            self.title = 'Black Hole Scripts'
        elif self.sel == 5:
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Logos'
            self.title = 'Black Hole Boot Logo'
        elif self.sel == 6:
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Settings'
            self.title = 'Black Hole Settings'
        elif self.sel == 7:
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Picons'
            self.title = 'Black Hole Picons Packages'
        elif self.sel == 8:
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=' + catver
            self.title = 'Latest 10 Uploads'
        downfile = '/tmp/cpanel.tmp'
        if fileExists(downfile):
            os_remove(downfile)
        if self.url == 'feeds':
            self.session.open(Nab_downFeedCat)
        else:
            self.session.openWithCallback(self.connectionDone, Nab_ConnectPop, self.url, downfile)

    def connectionDone(self):
        downfile = '/tmp/cpanel.tmp'
        if fileExists(downfile):
            self.session.open(Nab_downCat, self.title)
        else:
            nobox = self.session.open(MessageBox, _('Sorry, Connection Failed.'), MessageBox.TYPE_INFO)


class Nab_downFeedCat(Screen):
    skin = '\n\t<screen position="center,center" size="880,490" title="Black Hole Feeds Plugins">\n\t\t<widget source="list" render="Listbox" position="10,10" size="860,470" zPosition="1" scrollbarMode="showOnDemand"  transparent="1">\n            \t<convert type="TemplatedMultiContent">\n                {"template": [\n                MultiContentEntryText(pos = (4, 2), size = (840, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                ],\n                "fonts": [gFont("Regular", 26)],\n                "itemHeight": 36\n                }\n            \t</convert>\n             </widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['list'] = ''
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})
        mlist = []
        if fileExists('/usr/share/dict/pfeeds.en'):
            f = open('/usr/share/dict/pfeeds.en', 'r')
            for line in f.readlines():
                if len(line) > 4:
                    parts = line.strip().split('|')
                    res = (parts[0], parts[1], parts[2])
                    mlist.append(res)

            f.close()
        self['list'] = List(mlist)

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.session.open(Nab_ShowFeedFile, self.sel[1], self.sel[2])


class Nab_ShowFeedFile(Screen):
    skin = '\n\t<screen position="center,center" size="800,405" title="Black Hole E2 Package Details">\n\t\t<widget name="infotext" position="20,15" size="760,315" font="Regular;24" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="173,365" size="140,40" alphatest="on" />\n\t\t<widget name="key_green" position="173,365" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="486,365" size="140,40" alphatest="on" />\n\t\t<widget name="key_yellow" position="486,365" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t</screen>'

    def __init__(self, session, myidf, desc):
        Screen.__init__(self, session)
        self['key_green'] = Label(_('Install'))
        self['key_yellow'] = Label(_('Cancel'))
        self['infotext'] = ScrollLabel(desc)
        self.fileN = myidf
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'ok': self.KeyGreend,
         'back': self.close,
         'green': self.KeyGreend,
         'yellow': self.close,
         'up': self['infotext'].pageUp,
         'down': self['infotext'].pageDown})

    def KeyGreend(self):
        message = _('Do you want to install the Addon:\n ') + self.fileN + _(' ?')
        ybox = self.session.openWithCallback(self.installadd, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('Install'))

    def installadd(self, answer):
        if answer is True:
            dest = self.fileN
            mydir = getcwd()
            chdir('/')
            cmd = 'opkg update'
            if fileExists('/var/volatile/tmp/official-all'):
                cmd = "echo -e 'Testing: %s '" % dest
            cmd0 = 'opkg install --noaction %s > /tmp/package.info' % dest
            cmd1 = 'opkg install --force-overwrite ' + dest
            cmd2 = 'rm -f ' + dest
            self.session.open(Console, title=_('Ipk Package Installation'), cmdlist=[cmd,
             cmd0,
             cmd1,
             cmd2,
             'sleep 5'], finishedCallback=self.installipkDone)
            chdir(mydir)

    def installipkDone(self):
        if fileExists('/tmp/package.info'):
            f = open('/tmp/package.info', 'r')
            for line in f.readlines():
                if line.find('Installing') != -1:
                    parts = line.strip().split()
                    pname = '/usr/uninstall/' + parts[1] + '.del'
                    out = open(pname, 'w')
                    line = '#!/bin/sh\n\nopkg remove --force-depends --force-remove %s\nrm -f %s\n\nexit 0\n' % (parts[1], pname)
                    out.write(line)
                    out.close()
                    cmd = 'chmod 0755 ' + pname
                    rc = system(cmd)

            f.close()
            rc = system('rm -f /tmp/package.info')
        mybox = self.session.open(MessageBox, _('You need to restart Gui to complete package installation.\nPress ok to continue'), MessageBox.TYPE_INFO)
        mybox.setTitle(_('Info'))
        self.eDVBDB = eDVBDB.getInstance()
        self.eDVBDB.reloadServicelist()
        self.eDVBDB.reloadBouquets()
        self.close()


class Nab_downCat(Screen):
    skin = '\n\t<screen position="80,95" size="560,405" title="Black Hole E2 Downloads Manager">\n\t\t<widget source="list" render="Listbox" position="10,16" size="540,345" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t</screen>'

    def __init__(self, session, title):
        Screen.__init__(self, session)
        self.mytitle = title
        self.flist = []
        ivalue = ''
        step = 0
        if fileExists('/tmp/cpanel.tmp'):
            f = open('/tmp/cpanel.tmp', 'r')
            for line in f.readlines():
                line = line.replace('\n', '')
                line = line.strip()
                if step == 0:
                    ivalue = line
                    step = 1
                else:
                    res = (line, ivalue)
                    self.flist.append(res)
                    step = 0

            f.close()
            os_remove('/tmp/cpanel.tmp')
        self['list'] = List(self.flist)
        self.onShown.append(self.setWindowTitle)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def setWindowTitle(self):
        self.setTitle(self.mytitle)

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.myidf = self.sel[1]
            self.url = 'http://www.vuplus-community.net/bhaddons/index.php?op=outfile&idf=' + self.myidf
            downfile = '/tmp/cpanel.tmp'
            if fileExists(downfile):
                os_remove(downfile)
            self.session.openWithCallback(self.connectionDone, Nab_ConnectPop, self.url, downfile)

    def connectionDone(self):
        downfile = '/tmp/cpanel.tmp'
        if fileExists(downfile):
            self.session.open(Nab_ShowDownFile, self.myidf)
        else:
            nobox = self.session.open(MessageBox, _('Sorry, Connection Failed.'), MessageBox.TYPE_INFO)


class Nab_ShowPreviewFile(Screen):
    skin = '\n\t<screen position="0,0" size="1280,720" title="Black Hole E2 Preview" flags="wfNoBorder">\n\t\t<widget name="lab1" position="0,0" size="1280,720" zPosition="1" />\n\t\t<widget name="lab2" position="0,30" size="1280,30" zPosition="2" font="Regular;26" halign="center" valign="center" backgroundColor="red" foregroundColor="white" />\n\t</screen>'

    def __init__(self, session, myprev):
        Screen.__init__(self, session)
        self['lab1'] = Pixmap()
        self['lab2'] = Label(_('Black Hole Preview: click ok to exit'))
        self['actions'] = ActionMap(['WizardActions'], {'ok': self.close,
         'back': self.close})
        self.fileP = myprev.replace('.tgz', '.jpg')
        self.onLayoutFinish.append(self.addonsconn)

    def addonsconn(self):
        myicon = '/tmp/' + self.fileP
        png = loadPic(myicon, 1280, 720, 0, 0, 0, 1)
        self['lab1'].instance.setPixmap(png)
        os_remove(myicon)


class Nab_ShowDownFile(Screen):
    skin = '\n\t<screen position="80,95" size="560,405" title="Black Hole E2 Package Details">\n\t\t<widget name="infotext" position="10,15" size="540,315" font="Regular;20" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="210,365" size="140,40" alphatest="on" />\n\t\t<widget name="key_green" position="210,365" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="400,365" size="140,40" alphatest="on" />\n\t\t<widget name="key_yellow" position="400,365" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t</screen>'

    def __init__(self, session, myidf):
        Screen.__init__(self, session)
        self['key_green'] = Label(_('Download'))
        self['key_yellow'] = Label(_('Preview'))
        self['infotext'] = ScrollLabel()
        self.tcat = ''
        step = 0
        strview = 'TITLE: '
        if fileExists('/tmp/cpanel.tmp'):
            f = open('/tmp/cpanel.tmp', 'r')
            for line in f.readlines():
                line = nab_strip_html(line)
                line = line.replace('\n', '')
                line = line.strip()
                if step == 0:
                    self.fileN = line
                    step = 1
                elif step == 1:
                    strview += line
                    strview += '\n\n'
                    step = 2
                elif step == 2:
                    strview += 'By: '
                    strview += line
                    step = 3
                elif step == 3:
                    strview += '                          ' + line + '\n\n'
                    step = 4
                elif step == 4:
                    strview += 'Size: ' + line
                    step = 5
                elif step == 5:
                    strview += '                                Downloads: ' + line + '\n'
                    step = 6
                elif step == 6:
                    self.tcat = line
                    step = 7
                elif step == 7:
                    strview += '---------------------------------------------------------------------\n' + line + '\n'
                    step = 8
                else:
                    strview += line + '\n'

            f.close()
            os_remove('/tmp/cpanel.tmp')
        self['infotext'].setText(strview)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'ok': self.KeyGreend,
         'back': self.close,
         'green': self.KeyGreend,
         'yellow': self.KeyYellowd,
         'up': self['infotext'].pageUp,
         'down': self['infotext'].pageDown})

    def KeyYellowd(self):
        if self.tcat != 'Skins' and self.tcat != 'Logos':
            nobox = self.session.open(MessageBox, _('Sorry, the preview is available only for Skins and Bootlogo.'), MessageBox.TYPE_INFO)
        else:
            self.fileP = self.fileN.replace('.tgz', '.jpg')
            self.url = '"http://www.vuplus-community.net/bhaddons/files/' + self.fileP + '"'
            cmd = 'wget -O /tmp/' + self.fileP + ' ' + self.url
            self.session.openWithCallback(self.addonsconn2, Nab_ConnectPop, cmd, 'N/A')

    def addonsconn2(self):
        self.session.open(Nab_ShowPreviewFile, self.fileP)

    def KeyGreend(self):
        self.url = '"http://www.vuplus-community.net/bhaddons/files/' + self.fileN + '"'
        cmd = 'wget -O /tmp/' + self.fileN + ' ' + self.url
        self.session.openWithCallback(self.addonsconn, Nab_ConnectPop, cmd, 'N/A')

    def addonsconn(self):
        message = _('Do you want to install the Addon:\n ') + self.fileN + _(' ?')
        ybox = self.session.openWithCallback(self.installadd, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('Download Complete'))

    def installadd(self, answer):
        if answer is True:
            mytype = 1
            if self.fileN.find('.ipk') != -1:
                mytype = 2
            if mytype == 1:
                dest = '/tmp/' + self.fileN
                mydir = getcwd()
                chdir('/')
                cmd = 'tar -xzf ' + dest
                rc = system(cmd)
                chdir(mydir)
                cmd = 'rm -f ' + dest
                rc = system(cmd)
                if fileExists('/usr/sbin/nab_e2_restart.sh'):
                    rc = system('rm -f /usr/sbin/nab_e2_restart.sh')
                    mybox = self.session.open(MessageBox, _('You need to restart Gui to complete package installation.\nPress ok to continue'), MessageBox.TYPE_INFO)
                    mybox.setTitle(_('Info'))
                else:
                    mybox = self.session.open(MessageBox, _('Addon Succesfully Installed.'), MessageBox.TYPE_INFO)
                    mybox.setTitle(_('Info'))
                    self.close()
            elif mytype == 2:
                dest = '/tmp/' + self.fileN
                mydir = getcwd()
                chdir('/')
                cmd = 'opkg update'
                if fileExists('/var/volatile/tmp/official-all'):
                    cmd = "echo -e 'Testing: %s '" % dest
                cmd0 = 'opkg install --noaction %s > /tmp/package.info' % dest
                cmd1 = 'opkg install --force-overwrite ' + dest
                cmd2 = 'rm -f ' + dest
                self.session.open(Console, title='Ipk Package Installation', cmdlist=[cmd,
                 cmd0,
                 cmd1,
                 cmd2,
                 'sleep 5'], finishedCallback=self.installipkDone)
                chdir(mydir)
                self.eDVBDB = eDVBDB.getInstance()
                self.eDVBDB.reloadServicelist()
                self.eDVBDB.reloadBouquets()
                self.close()

    def installipkDone(self):
        if fileExists('/tmp/package.info'):
            f = open('/tmp/package.info', 'r')
            for line in f.readlines():
                if line.find('Installing') != -1:
                    parts = line.strip().split()
                    pname = '/usr/uninstall/' + parts[1] + '.del'
                    out = open(pname, 'w')
                    line = '#!/bin/sh\n\nopkg remove --force-depends --force-remove %s\nrm -f %s\n\nexit 0\n' % (parts[1], pname)
                    out.write(line)
                    out.close()
                    cmd = 'chmod 0755 ' + pname
                    rc = system(cmd)

            f.close()
            rc = system('rm -f /tmp/package.info')
        mybox = self.session.open(MessageBox, _('You need to restart Gui to complete package installation.\nPress ok to continue'), MessageBox.TYPE_INFO)
        mybox.setTitle(_('Info'))
        self.eDVBDB = eDVBDB.getInstance()
        self.eDVBDB.reloadServicelist()
        self.eDVBDB.reloadBouquets()
        self.close()


class Nab_downPanel(Screen):
    skin = '\n\t<screen position="80,95" size="560,405" title="Black Hole E2 Manual Install BH Packages">\n\t\t<widget source="list" render="Listbox" position="10,16" size="540,380" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.flist = []
        idx = 0
        pkgs = listdir('/tmp')
        for fil in pkgs:
            if fil.find('.tgz') != -1:
                res = (fil, idx)
                self.flist.append(res)
                idx = idx + 1

        self['list'] = List(self.flist)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[0]
            message = _('Do you want to install the Addon:\n ') + self.sel + _(' ?')
            ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Installation Confirm'))

    def installadd2(self, answer):
        if answer is True:
            dest = '/tmp/' + self.sel
            mydir = getcwd()
            chdir('/')
            cmd = 'tar -xzf ' + dest
            rc = system(cmd)
            chdir(mydir)
            cmd = 'rm -f ' + dest
            rc = system(cmd)
            if fileExists('/usr/sbin/nab_e2_restart.sh'):
                rc = system('rm -f /usr/sbin/nab_e2_restart.sh')
                mybox = self.session.open(MessageBox, _('You need to restart Gui to complete package installation.\nPress ok to continue'), MessageBox.TYPE_INFO)
                mybox.setTitle(_('Info'))
                self.eDVBDB = eDVBDB.getInstance()
                self.eDVBDB.reloadServicelist()
                self.eDVBDB.reloadBouquets()
                self.close()
            else:
                mybox = self.session.open(MessageBox, _('Addon Succesfully Installed.'), MessageBox.TYPE_INFO)
                mybox.setTitle(_('Info'))
                self.close()


class Nab_downPanelIPK(Screen):
    skin = '\n\t<screen position="80,95" size="560,405" title="Black Hole E2 Manual Install Ipk Packages">\n\t\t<widget source="list" render="Listbox" position="10,10" size="540,290" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t\t<widget name="warntext" position="0,305" size="560,100" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.flist = []
        idx = 0
        pkgs = listdir('/tmp')
        for fil in pkgs:
            if fil.find('.ipk') != -1:
                res = (fil, idx)
                self.flist.append(res)
                idx = idx + 1

        self['warntext'] = Label(_('Here you can install any kind of ipk packages.'))
        self['list'] = List(self.flist)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[0]
            message = _('Do you want to install the Addon:\n ') + self.sel + _(' ?')
            ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Installation Confirm'))

    def installadd2(self, answer):
        if answer is True:
            dest = '/tmp/' + self.sel
            mydir = getcwd()
            chdir('/')
            cmd = 'opkg update'
            if fileExists('/var/volatile/tmp/official-all'):
                cmd = "echo -e 'Testing: %s '" % dest
            cmd0 = 'opkg install --noaction %s > /tmp/package.info' % dest
            cmd1 = 'opkg install --force-overwrite ' + dest
            cmd2 = 'rm -f ' + dest
            self.session.open(Console, title='Ipk Package Installation', cmdlist=[cmd,
             cmd0,
             cmd1,
             cmd2,
             'sleep 5'], finishedCallback=self.installipkDone)
            chdir(mydir)

    def installipkDone(self):
        if fileExists('/tmp/package.info'):
            f = open('/tmp/package.info', 'r')
            for line in f.readlines():
                if line.find('Installing') != -1:
                    parts = line.strip().split()
                    pname = '/usr/uninstall/' + parts[1] + '.del'
                    out = open(pname, 'w')
                    line = '#!/bin/sh\n\nopkg remove --force-depends --force-remove %s\nrm -f %s\n\nexit 0\n' % (parts[1], pname)
                    out.write(line)
                    out.close()
                    cmd = 'chmod 0755 ' + pname
                    rc = system(cmd)

            f.close()
            rc = system('rm -f /tmp/package.info')
        mybox = self.session.open(MessageBox, _('You need to restart Gui to complete package installation.\nPress ok to continue'), MessageBox.TYPE_INFO)
        mybox.setTitle(_('Info'))
        self.eDVBDB = eDVBDB.getInstance()
        self.eDVBDB.reloadServicelist()
        self.eDVBDB.reloadBouquets()
        self.close()


class Nab_uninstPanel(Screen):
    skin = '\n\t<screen position="80,95" size="560,405" title="Black Hole E2 Uninstall Panel">\n\t\t<widget source="list" render="Listbox" position="10,16" size="540,380" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.flist = []
        idx = 0
        pkgs = listdir('/usr/uninstall')
        for fil in pkgs:
            if fil.find('.nab') != -1 or fil.find('.del') != -1:
                res = (fil, idx)
                self.flist.append(res)
                idx = idx + 1

        self['list'] = List(self.flist)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[0]
            message = _('Are you sure you want to Remove Package:\n ') + self.sel + _('?')
            ybox = self.session.openWithCallback(self.uninstPack, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Uninstall Confirmation'))

    def uninstPack(self, answer):
        if answer is True:
            orig = '/usr/uninstall/' + self.sel
            cmd = 'sh ' + orig
            rc = system(cmd)
            mybox = self.session.open(MessageBox, _('Addon Succesfully Removed. You need to Restart Gui for the changes to take effect.\nPress ok to continue'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
        self.close()


class Nab_Stats(Screen):
    skin = '\n\t<screen position="80,95" size="560,405" title="Black Hole E2 Statistics">\n\t\t<widget name="infotext" position="10,15" size="540,315" font="Regular;20" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['infotext'] = ScrollLabel()
        self['actions'] = ActionMap(['WizardActions'], {'ok': self.close,
         'back': self.close})
        self.statshow()

    def statshow(self):
        if fileExists('/tmp/cpanel.tmp'):
            strview = _('Black Hole Image Statistics:\n\n_____________________________________\n')
            step = 0
            f = open('/tmp/cpanel.tmp', 'r')
            for line in f.readlines():
                if step == 0:
                    strview += _('Total Connections:   \t')
                elif step == 1:
                    strview += _('Today Connections:   \t')
                elif step == 2:
                    strview += _('Available Forums:   \t')
                elif step == 3:
                    step = step + 1
                    continue
                elif step == 4:
                    strview += _('Shouts sent by users:\t')
                elif step == 5:
                    step = step + 1
                    continue
                elif step == 6:
                    step = step + 1
                    continue
                elif step == 7:
                    strview += _('Top downloaded File:\t')
                elif step == 8:
                    strview += _('Total Downloads:     \t')
                strview += line
                step = step + 1

            f.close()
            os_remove('/tmp/cpanel.tmp')
            self['infotext'].setText(strview)


class addonsParentalConfig(Screen, ConfigListScreen):
    skin = '\n\t<screen position="center,center" size="700,340" title="Addons parental control setup">\n\t\t<widget name="config" position="10,100" size="680,110" scrollbarMode="showOnDemand" transparent="1" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="140,270" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="140,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />\n\t\t<ePixmap position="420,270" size="140,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />\n\t\t<widget name="key_green" position="420,270" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.keyCancel,
         'back': self.keyCancel,
         'green': self.keySave}, -2)
        self.updateList()

    def updateList(self):
        item = getConfigListEntry(_('Addons access protected'), config.bhaddons.lock)
        self.list.append(item)
        item = getConfigListEntry(_('Addons access pin'), config.bhaddons.pin)
        self.list.append(item)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        self.close()

    def keyCancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()


class Nab_ConnectPop(Screen):
    skin = '\n\t<screen position="390,100" size="484,220" title="Black Hole E2" flags="wfNoBorder">\n\t\t<widget name="connect" position="0,0" size="484,250" zPosition="-1" pixmaps="skin_default/connection_1.png,skin_default/connection_2.png,skin_default/connection_3.png,skin_default/connection_4.png,skin_default/connection_5.png" transparent="1" />\n\t\t<widget name="lab1" position="10,180" halign="center" size="460,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />\n\t</screen>'

    def __init__(self, session, myurl, downfile):
        Screen.__init__(self, session)
        self['connect'] = MultiPixmap()
        self['connect'].setPixmapNum(0)
        self['lab1'] = Label(_('Wait please connection in progress ...'))
        self.myurl = myurl
        self.downfile = downfile
        self.activityTimer = eTimer()
        if self.downfile == 'N/A':
            self.activityTimer.timeout.get().append(self.updatepixWget)
        else:
            self.activityTimer.timeout.get().append(self.updatepix)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)

    def startShow(self):
        self.curpix = 0
        self.count = 0
        self.activityTimer.start(300)

    def updatepixWget(self):
        self.activityTimer.stop()
        if self.curpix > 3:
            self.curpix = 0
        if self.count > 8:
            self.curpix = 4
            self['lab1'].setText(_('Wait please, download in progress...'))
        self['connect'].setPixmapNum(self.curpix)
        if self.count == 10:
            rc = system(self.myurl)
        if self.count == 11:
            self.close()
        self.activityTimer.start(120)
        self.curpix += 1
        self.count += 1

    def updatepix(self):
        self.activityTimer.stop()
        if self.curpix > 3:
            self.curpix = 0
        if self.count > 8:
            self.curpix = 4
            req = Request(self.myurl)
            try:
                response = urlopen(req)
            except HTTPError as e:
                self.close()
            except URLError as e:
                self.close()
            else:
                self['lab1'].setText(_('Connection Established'))
                html = response.read()
                out = open(self.downfile, 'w')
                out.write(html)
                out.close()

        self['connect'].setPixmapNum(self.curpix)
        if self.count == 10:
            self.close()
        self.activityTimer.start(120)
        self.curpix += 1
        self.count += 1

    def delTimer(self):
        del self.activityTimer


class Bh_Feed_Settings2(Screen):
    skin = '\n\t<screen position="center,center" size="902,570" title="BH Feeds Settings">\n\t\t<widget name="lab1" position="50,260" size="800,40" zPosition="2" halign="center" font="Regular;24" />\n\t\t<widget name="lab2" position="10,10" size="882,22" font="Regular;20" valign="top" transparent="1"/>\n\t\t<widget name="lab3" position="20,32" size="872,20" font="Regular;20" valign="top" transparent="1"/>\n\t\t<widget source="list" render="Listbox" position="30,80" size="840,420" scrollbarMode="showOnDemand" transparent="1">\n            \t<convert type="TemplatedMultiContent">\n                    {"template": [\n                       MultiContentEntryText(pos = (10, 5), size = (690, 25), font=0, text = 0),\n                       MultiContentEntryText(pos = (20, 30), size = (670, 20), font=1, flags = RT_VALIGN_TOP, text = 1),\n                    ],\n                    "fonts": [gFont("Regular", 24),gFont("Regular", 20)],\n                    "itemHeight": 60\n                    }\n                   </convert>\n        \t</widget>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="120,530" size="140,40" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="380,530" size="140,40" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="640,530" size="200,40" alphatest="on"/>\n\t\t<widget name="key_red" position="120,530" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t\t<widget name="key_green" position="380,530" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t\t<widget name="key_yellow" position="640,530" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Install'))
        self['key_green'] = Label(_('Remove'))
        self['key_yellow'] = Label(_('Setup'))
        self['lab1'] = Label(_('Wait please checking for available updates...'))
        self['lab2'] = Label('')
        self['lab3'] = Label('')
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'ok': self.install_Pack,
         'red': self.install_Pack,
         'green': self.remove_Pack,
         'yellow': self.setuP})
        self.eDVBDB = eDVBDB.getInstance()
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateList2)
        self.checkupgrade = False
        self.updateList()

    def updateList(self):
        self.activityTimer.start(3)

    def updateList2(self):
        self.activityTimer.stop()
        self.installed = ''
        self.installedver = ''
        self.list = []
        ret = system('opkg update')
        ret = system('opkg info enigma2-settings* > /tmp/cpanel.tmp')
        packname = ''
        packver = ''
        step = 0
        if fileExists('/tmp/cpanel.tmp'):
            f = open('/tmp/cpanel.tmp', 'r')
            for line in f.readlines():
                if line.find('Package: enigma2-settings-vhannibal-common') != -1:
                    step = 0
                    continue
                elif line.find('Package:') != -1:
                    parts = line.strip().split()
                    packname = parts[1]
                    step = 1
                if step == 1:
                    if line.find('Version:') != -1:
                        parts = line.strip().split()
                        packver = _('version:') + ' ' + parts[1]
                        res = (packname, packver)
                        self.list.append(res)
                    elif line.find('Status:') != -1:
                        if line.find('not-installed') == -1:
                            self.installed = packname
                            self.installedver = packver
                            step = 0

            f.close()
            os_remove('/tmp/cpanel.tmp')
        mylist = sorted(self.list, key=itemgetter(0))
        self['list'].list = mylist
        self['lab1'].hide()
        lab2_text = _('Settings installed:') + ' ' + self.installed
        self['lab2'].setText(lab2_text)
        self['lab3'].setText(self.installedver)
        if self.checkupgrade == False:
            self.checkUpgrade()

    def checkUpgrade(self):
        self.checkupgrade = True
        foundupgrade = False
        ret = system('opkg list-upgradable  > /tmp/cpanel.tmp')
        if fileExists('/tmp/cpanel.tmp'):
            f = open('/tmp/cpanel.tmp', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == self.installed:
                    foundupgrade = True
                    break

            f.close()
            os_remove('/tmp/cpanel.tmp')
        if foundupgrade == True:
            self.askUpgrade()

    def askUpgrade(self):
        message = _('Upgrade found.\nDo you want to upgrade the settings package:\n ') + self.installed + _(' ?')
        self.session.openWithCallback(self.upgradePack, MessageBox, message, MessageBox.TYPE_YESNO)

    def upgradePack(self, answer):
        if answer is True:
            self.done_message = _('Package %s upgraded.') % self.installed
            cmd1 = 'opkg install ' + self.installed
            self.session.open(Console, title=_('New Settings Package Installation'), cmdlist=[cmd1], finishedCallback=self.ipkDone, closeOnSuccess=True)

    def install_Pack(self):
        if self.installed != '':
            text = _('You have to remove the installed %s before to install a new settings pack.') % self.installed
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO)
        else:
            self.sel = self['list'].getCurrent()
            if self.sel:
                self.newpack = self.sel[0]
                message = _('Do you want to install the Package:\n ') + self.newpack + _(' ?')
                self.session.openWithCallback(self.do_install_Pack, MessageBox, message, MessageBox.TYPE_YESNO)

    def do_install_Pack(self, answer):
        if answer is True:
            self.done_message = _('Package installed.')
            cmd1 = 'opkg install ' + self.newpack
            self.session.open(Console, title=_('New Settings Package Installation'), cmdlist=[cmd1], finishedCallback=self.ipkDone, closeOnSuccess=True)

    def remove_Pack(self):
        if self.installed == '':
            text = _('No package installed. Nothing to remove.')
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO)
        else:
            message = _('Are you sure you want to remove the Package:\n ') + self.installed + _(' ?')
            self.session.openWithCallback(self.do_remove_Pack, MessageBox, message, MessageBox.TYPE_YESNO)

    def do_remove_Pack(self, answer):
        if answer is True:
            out = open('/etc/bhcron/bh.cron', 'w')
            if fileExists('/etc/bhcron/root'):
                f = open('/etc/bhcron/root', 'r')
                for line in f.readlines():
                    if line.find(self.installed) != -1:
                        continue
                    out.write(line)

            f.close()
            out.close()
            self.deliteepgdisabled.value = True
            if fileExists('/etc/cron/crontabs/root'):
                print("/etc/cron/crontabs/root exists")
            else:
                rc = system('ln -sfn /etc/bhcron/root /etc/cron/crontabs/root')
            rc = system('crontab /etc/bhcron/bh.cron -c /etc/bhcron/')
            self.done_message = _('Package %s removed.') % self.installed
            cmd1 = 'opkg remove ' + self.installed
            self.session.open(Console, title=_('Removing package'), cmdlist=[cmd1], finishedCallback=self.ipkDone, closeOnSuccess=True)

    def setuP(self):
        if self.installed == '':
            text = _('No package installed. Nothing to setup.')
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO)
        else:
            self.session.open(Bh_Feed_SettingsSetup, self.installed)

    def ipkDone(self):
        self.eDVBDB.reloadServicelist()
        self.eDVBDB.reloadBouquets()
        self.session.open(MessageBox, self.done_message, MessageBox.TYPE_INFO)
        self.updateList2()


class Bh_Feed_SettingsSetup(Screen, ConfigListScreen):
    skin = '\n\t<screen position="center,center" size="900,340" title="BH Feeds Settings Setup">\n\t\t<widget name="lab1" position="10,10" size="220,30" font="Regular;20" transparent="1"/>\n\t\t<widget name="labprov" position="230,10" size="640,30" font="Regular;20"/>\n\t\t<widget name="config" position="10,40" size="880,250" scrollbarMode="showOnDemand" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="380,290" size="150,40" alphatest="on" />\n\t\t<widget name="key_red" position="380,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t</screen>'

    def __init__(self, session, provider):
        Screen.__init__(self, session)
        self.pack = provider
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['lab1'] = Label(_('Settings installed:'))
        self['labprov'] = Label(provider)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.saveMyset,
         'back': self.close})
        self.updateList()

    def updateList(self):
        self.packautodown = NoSave(ConfigYesNo(default=False))
        self.timerentry_starttime = NoSave(ConfigClock(default=0))
        self.freq = NoSave(ConfigSelection(default='2', choices=[('1', 'day'), ('2', 'week'), ('3', 'month')]))
        strview = ''
        mytmpt = [23, 2]
        autodown = False
        freq = '2'
        if fileExists('/etc/bhcron/root'):
            f = open('/etc/bhcron/root', 'r')
            for line in f.readlines():
                if line.find(self.pack) != -1:
                    strview = line
                    break

            f.close()
        if strview:
            parts = strview.strip().split()
            mytmpt = [int(parts[1]), int(parts[0])]
            freq = '1'
            if parts[2] == '1':
                freq = '3'
            elif parts[4] == '1':
                freq = '2'
            autodown = True
        self.packautodown.value = autodown
        self.timerentry_starttime.value = mytmpt
        self.freq.value = freq
        res = getConfigListEntry(_('Enable Automatic Settings update'), self.packautodown)
        self.list.append(res)
        res = getConfigListEntry(_('Check updates every'), self.freq)
        self.list.append(res)
        res = getConfigListEntry(_('Check updates at time'), self.timerentry_starttime)
        self.list.append(res)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def saveMyset(self):
        croncmd = '/usr/bin/opkg update && /usr/bin/opkg install ' + self.pack
        hour = '%02d' % self.timerentry_starttime.value[0]
        minutes = '%02d' % self.timerentry_starttime.value[1]
        freq = ' * * * '
        if self.freq.value == '2':
            freq = ' * * 1 '
        elif self.freq.value == '3':
            freq = ' 1 * * '
        newcron = minutes + ' ' + hour + freq + croncmd + '\n'
        out = open('/etc/bhcron/bh.cron', 'w')
        if fileExists('/etc/bhcron/root'):
            f = open('/etc/bhcron/root', 'r')
            for line in f.readlines():
                if line.find(self.pack) != -1:
                    continue
                out.write(line)

            f.close()
        if self.packautodown.value == True:
            out.write(newcron)
        out.close()
        if fileExists('/etc/cron/crontabs/root'):
           print("/etc/cron/crontabs/root exists")
        else:
           rc = system('ln -sfn /etc/bhcron/root /etc/cron/crontabs/root')
        rc = system('crontab /etc/bhcron/bh.cron -c /etc/bhcron/')
        self.close()


class Bh_Feed_Upgrade(Screen):
    skin = '\n\t<screen position="center,center" size="902,570" title="BH Feeds Upgrade">\n\t\t<widget name="lab1" position="50,260" size="800,40" zPosition="2" halign="center" font="Regular;24" />\n\t\t<widget name="lab2" position="10,10" size="882,22" font="Regular;20" valign="top" transparent="1"/>\n\t\t<widget name="lab3" position="20,32" size="872,20" font="Regular;20" valign="top" transparent="1"/>\n\t\t<widget source="list" render="Listbox" position="30,80" size="840,420" scrollbarMode="showOnDemand" transparent="1">\n            \t<convert type="TemplatedMultiContent">\n                    {"template": [\n                       MultiContentEntryText(pos = (10, 5), size = (690, 25), font=0, text = 0),\n                       MultiContentEntryText(pos = (20, 30), size = (670, 20), font=1, flags = RT_VALIGN_TOP, text = 1),\n                    ],\n                    "fonts": [gFont("Regular", 24),gFont("Regular", 20)],\n                    "itemHeight": 60\n                    }\n                   </convert>\n        \t</widget>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="380,530" size="140,40" alphatest="on"/>\n\t\t<widget name="key_red" position="380,530" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Install'))
        self['lab1'] = Label(_('Wait please checking for available updates...'))
        self['lab2'] = Label('')
        self['lab3'] = Label('')
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'ok': self.install_Pack,
         'red': self.install_Pack})
        self.eDVBDB = eDVBDB.getInstance()
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateList2)
        self.updateList()

    def updateList(self):
        self.activityTimer.start(3)

    def updateList2(self):
        self.activityTimer.stop()
        self.installed = ''
        self.installedver = ''
        self.list = []
        ret = system('opkg update')
        ret = system('cat /tmp/opkg/blackhole-Upgrade > /tmp/cpanel.tmp')
        packname = ''
        packver = ''
        step = 0
        if fileExists('/tmp/cpanel.tmp'):
            f = open('/tmp/cpanel.tmp', 'r')
            for line in f.readlines():
                if line.find('Package:') != -1:
                    parts = line.strip().split()
                    packname = parts[1]
                    step = 1
                if step == 1:
                    if line.find('Version:') != -1:
                        parts = line.strip().split()
                        packver = _('version:') + ' ' + parts[1]
                        res = (packname, packver)
                        self.list.append(res)
                    elif line.find('Status:') != -1:
                        if line.find('not-installed') == -1:
                            self.installed = packname
                            self.installedver = packver
                            step = 0

            f.close()
            os_remove('/tmp/cpanel.tmp')
        mylist = sorted(self.list, key=itemgetter(0))
        self['list'].list = mylist
        self['lab1'].hide()
        lab2_text = _('Upgrade installed:') + ' ' + self.installed
        self['lab2'].setText(lab2_text)
        self['lab3'].setText(self.installedver)

    def askUpgrade(self):
        message = _('Upgrade found.\nDo you want to upgrade the Black Hole package:\n ') + self.installed + _(' ?')
        self.session.openWithCallback(self.upgradePack, MessageBox, message, MessageBox.TYPE_YESNO)

    def upgradePack(self, answer):
        if answer is True:
            self.done_message = _('Package %s upgraded.') % self.installed
            cmd1 = 'opkg install --force-overwrite' + self.installed
            self.session.open(Console, title=_('New Upgrade Package Installation'), cmdlist=[cmd1], finishedCallback=self.ipkDone, closeOnSuccess=True)

    def install_Pack(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.newpack = self.sel[0]
            message = _('Do you want to install the Package:\n ') + self.newpack + _(' ?')
            self.session.openWithCallback(self.do_install_Pack, MessageBox, message, MessageBox.TYPE_YESNO)

    def do_install_Pack(self, answer):
        if answer is True:
            self.done_message = _('Package installed.')
            cmd1 = 'opkg install ' + self.newpack
            self.session.open(Console, title=_('New Upgrade Package Installation'), cmdlist=[cmd1], finishedCallback=self.ipkDone, closeOnSuccess=True)

    def ipkDone(self):
        self.eDVBDB.reloadServicelist()
        self.eDVBDB.reloadBouquets()
        self.session.open(MessageBox, self.done_message, MessageBox.TYPE_INFO)
        self.updateList2()
