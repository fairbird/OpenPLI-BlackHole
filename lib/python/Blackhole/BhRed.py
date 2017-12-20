from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.config import config, configfile, getConfigListEntry, ConfigYesNo, ConfigSubsection, ConfigInteger, NoSave
from Components.Console import Console
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir
from os import system, remove as os_remove
from BhUtils import DeliteGetSkinPath, BhU_check_proc_version
from enigma import eListboxPythonMultiContent, gFont, eTimer

def Bh_read_Universe_Cfg(universe):
    fname = '/universe/.%s.cfg' % universe
    data = ['False', '0', 'False']
    if fileExists(fname):
        all = open(fname, 'rb').readlines()
        info = {}
        for line in all:
            d = line.split(':', 1)
            if len(d) > 1:
                info[d[0].strip()] = d[1].strip()

        data[0] = info.get('universe_lock', 'False')
        data[1] = info.get('universe_pin', '0')
        data[2] = info.get('universe_force_reboot', 'False')
    return data


class UniverseList(MenuList):

    def __init__(self, enableWrapAround = False):
        MenuList.__init__(self, [], enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 24))
        self.l.setItemHeight(106)


class BhRedDisabled(Screen):
    skin = '\n\t<screen position="center,center" size="700,300" title="Expand your universe.">\n\t\t<widget name="lab1" position="20,20" size="660,260" font="Regular;20" />\n\t</screen>'

    def __init__(self, session, reason):
        Screen.__init__(self, session)
        msg = _('Sorry no space available to expand your Universe.\n\n')
        msg += _('To enable Parallel dimensions you need a dedicated Usb stick.\n\nInstructions:\n')
        msg += _('1) Format your Usb stick \n -click on blue -> blue -> Usb Format Wizard\n\n')
        msg += _('2) Map the newly formatted stick to "universe"\n -click on blue -> blue -> Devices Manager.')
        if reason == 'flash':
            msg = _('Sorry you can only access Parallel Universes from the image installed in flash.')
        self['lab1'] = Label(msg)
        self['actions'] = ActionMap(['WizardActions'], {'ok': self.close,
         'back': self.close})


class BhRedWrong(Screen):
    skin = '\n\t<screen position="center,center" size="700,330" title="Outdated universes.">\n\t\t<widget name="lab1" position="20,10" size="660,260" font="Regular;20" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="146,280" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="432,280" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="146,280" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="432,280" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Big Bang'))
        self['key_green'] = Label(_('Exit'))
        msg = _('Sorry your Parallel Universes are older than your Black Hole world.\nYou need to re-inizialize the system, reformat your Usb stick or generate a Bing Bang.\n')
        self['lab1'] = Label(msg)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.gotobingBang,
         'green': self.close,
         'back': self.close})

    def gotobingBang(self):
        msg = _('The Big Bang will collapse all of the Parallel Universes into the original Black Hole matrix.\nThis means that all of your Parallel Universes will be destroyed and turned back into Black Hole timespace.\nWarning, all of the data stored in your Parallel Universes will be lost.\nAre you sure you want to start the Bing Bang?')
        self.session.openWithCallback(self.startbigBang, MessageBox, msg, MessageBox.TYPE_YESNO)

    def startbigBang(self, answer):
        if answer == True:
            self.session.open(BhBigBang)
            self.close()


class BhRedPanel(Screen):
    skin = '\n\t<screen position="center,center" size="1000,530" title="Black Hole Parallel Universes Teleportation">\n\t\t\n\t\t<widget name="list" position="10,0" size="580,450" scrollbarMode="showOnDemand" transparent="1"   />\n\t\t\n\t\t<ePixmap pixmap="skin_default/div-v.png" position="590,0" size="2,450" alphatest="on" />\n\t\t<widget name="lab1" position="600,10" size="400,30" font="Regular;24" halign="center" foregroundColor="#9f1313" transparent="1"/>\n\t\t<widget name="lab2" position="600,60" size="400,390" font="Regular;20" valign="top" transparent="1"/>\n\t\t<ePixmap pixmap="skin_default/div-h.png" position="0,450" size="500,2" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/div-h.png" position="500,450" size="500,2" alphatest="on" />\n    \t\t<ePixmap pixmap="skin_default/buttons/red.png" position="145,470" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="430,470" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="715,470" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="145,470" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="430,470" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t\t<widget name="key_yellow" position="715,470" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n    \t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Jump to...'))
        self['key_green'] = Label(_('Big Bang'))
        self['key_yellow'] = Label(_('Exit'))
        self['lab1'] = Label()
        self['lab2'] = Label()
        self.current_universe = self.destination = self.destination_lock = self.destination_pin = self.destination_force_reboot = ''
        self.jump_on_close = False
        self.list = []
        self['list'] = UniverseList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'ok': self.confiG,
         'red': self.checkdesT,
         'green': self.check_origin,
         'yellow': self.close})
        self.onClose.append(self.closE)
        self.onShow.append(self.updateList)

    def updateList(self):
        self.list = []
        mypath = DeliteGetSkinPath()
        rc = system('df -h > /tmp/syinfo.tmp')
        mypixmap = mypath + 'icons/icon_home_BH.png'
        png = LoadPixmap(mypixmap)
        name = 'Black Hole'
        title = MultiContentEntryText(pos=(120, 30), size=(480, 50), font=0, text=name)
        png = MultiContentEntryPixmapAlphaTest(pos=(0, 3), size=(100, 100), png=png)
        self.list.append([name, title, png])
        mypixmap = mypath + 'icons/icon_avalon.png'
        png = LoadPixmap(mypixmap)
        name = 'Avalon'
        title = MultiContentEntryText(pos=(120, 30), size=(480, 50), font=0, text=name)
        png = MultiContentEntryPixmapAlphaTest(pos=(0, 3), size=(100, 100), png=png)
        self.list.append([name, title, png])
        mypixmap = mypath + 'icons/icon_chaos.png'
        png = LoadPixmap(mypixmap)
        name = 'Chaos'
        title = MultiContentEntryText(pos=(120, 30), size=(480, 50), font=0, text=name)
        png = MultiContentEntryPixmapAlphaTest(pos=(0, 3), size=(100, 100), png=png)
        self.list.append([name, title, png])
        mypixmap = mypath + 'icons/icon_ghost.png'
        png = LoadPixmap(mypixmap)
        name = 'Ghost'
        title = MultiContentEntryText(pos=(120, 30), size=(480, 50), font=0, text=name)
        png = MultiContentEntryPixmapAlphaTest(pos=(0, 3), size=(100, 100), png=png)
        self.list.append([name, title, png])
        self['list'].setList(self.list)
        self.current_universe = self.whereIAm()
        txt = _('You are in %s universe.') % self.current_universe
        self['lab1'].setText(txt)
        btot = buse = bempty = utot = uuse = uempty = ''
        f = open('/tmp/syinfo.tmp', 'r')
        for line in f.readlines():
            parts = line.split()
            tot = len(parts) - 1
            if parts[tot].strip() == '/':
                btot = parts[tot - 4].strip()
                buse = parts[tot - 1].strip()
                bempty = parts[tot - 2].strip()
            elif parts[tot].strip() == '/universe':
                utot = parts[tot - 4].strip()
                uuse = parts[tot - 1].strip()
                uempty = parts[tot - 2].strip()
                break

        f.close()
        os_remove('/tmp/syinfo.tmp')
        text = _('Black Hole details:\nBlack Hole is the original matrix of all Parallel Universes and resides in its own phisycal space.\n')
        text += _('Estimated size: %s \n') % btot
        text += _('Occupied space: %s \n') % buse
        text += _('Empty space: %s \n\n') % bempty
        text += _('Parallel Universes details:\nParallel Universes share the same space because they are all together in the same place, but in different dimensions.\n')
        text += _('Estimated size: %s \n') % utot
        text += _('Occupied space: %s \n') % uuse
        text += _('Empty space: %s \n\n') % uempty
        self['lab2'].setText(text)
        pos = 0
        sel = self['list'].getCurrent()
        for x in self.list:
            if x[0] == self.current_universe:
                self['list'].moveToIndex(pos)
                break
            pos += 1

    def whereIAm(self):
        ret = 'Black Hole'
        all = ['Avalon', 'Chaos', 'Ghost']
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/usr ') != -1:
                for a in all:
                    if line.find(a) != -1:
                        ret = a

                break

        f.close()
        return ret

    def confiG(self):
        sel = self['list'].getCurrent()
        if sel[0] != 'Black Hole':
            data = Bh_read_Universe_Cfg(sel[0])
            self.config_univ = sel[0]
            self.config_pin = data[1]
            if data[0] == 'True':
                msg = _('Enter the pin for %s universe') % sel[0]
                self.session.openWithCallback(self.confiG2, InputBox, title=msg, windowTitle=_('Insert Pin'), text='0000', useableChars='1234567890')
            else:
                self.session.open(BhUniverseConfig, sel[0])

    def confiG2(self, pin):
        if pin is None:
            pin = '0'
        if int(pin) == int(self.config_pin):
            self.session.open(BhUniverseConfig, self.config_univ)
        else:
            self.session.open(MessageBox, _('Sorry, wrong pin.'), MessageBox.TYPE_ERROR)

    def checkdesT(self):
        sel = self['list'].getCurrent()
        self.destination = sel[0]
        if self.current_universe == self.destination:
            msg = _('You are already in %s universe.') % self.destination
            self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
        else:
            data = Bh_read_Universe_Cfg(self.destination)
            self.destination_lock = data[0]
            self.destination_pin = data[1]
            self.destination_force_reboot = data[2]
            if data[0] == 'True':
                msg = _('Enter the pin for %s universe') % self.destination
                self.session.openWithCallback(self.checkdesTPin, InputBox, title=msg, windowTitle=_('Insert Pin'), text='0000', useableChars='1234567890')
            else:
                self.askjumpConfirm()

    def checkdesTPin(self, pin):
        if pin is None:
            pin = '0'
        if int(pin) == int(self.destination_pin):
            self.askjumpConfirm()
        else:
            self.session.open(MessageBox, _('Sorry, wrong pin.'), MessageBox.TYPE_ERROR)

    def askjumpConfirm(self):
        msg = _('We are going to jump into %s Universe.\nPlease remember that anything you do in this Universe, such as install sofware, skins or plugins will have no effect on the other Universes.\nAre you sure you want to jump?') % self.destination
        self.session.openWithCallback(self.prEjumP, MessageBox, msg, MessageBox.TYPE_YESNO)

    def prEjumP(self, answer):
        if answer == True:
            rc = system('/usr/bin/StartBhCam stop')
            mvi = '/usr/share/' + self.destination + '.mvi'
            mvi = mvi.replace(' ', '_')
            cmd = 'cp %s /bin/jump_screen.mvi' % mvi
            rc = system(cmd)
            self.jumP()

    def jumP(self):
        path = '/universe/' + self.destination
        path1 = path + '/etc'
        path2 = path + '/usr'
        path3 = path + '/var/lib/opkg'
        pathspinorig = '/usr/share/spinners/' + self.destination + '/*'
        pathspindest = path2 + '/share/enigma2/skin_default/spinner/'
        if self.destination != 'Black Hole':
            if not pathExists(path):
                createDir(path)
            if not pathExists(path1):
                createDir(path1)
                cmd = 'cp -r /etc %s' % path
                system(cmd)
            if not pathExists(path3):
                pathtmp = path + '/var'
                createDir(pathtmp)
                pathtmp = pathtmp + '/lib'
                createDir(pathtmp)
                cmd = 'cp -r /var/lib/opkg %s/var/lib' % path
                system(cmd)
            if not pathExists(path2):
                createDir(path2)
                pathtmp = path2 + '/share'
                createDir(pathtmp)
                pathtmp = pathtmp + '/enigma2'
                createDir(pathtmp)
                pathtmp = pathtmp + '/skin_default'
                createDir(pathtmp)
                pathtmp = pathtmp + '/spinner'
                createDir(pathtmp)
                cmd = 'cp -f %s %s' % (pathspinorig, pathspindest)
                system(cmd)
        if fileExists('/bin/bh_parallel_mount'):
            os_remove('/bin/bh_parallel_mount')
        if self.destination != 'Black Hole':
            if self.destination_force_reboot == 'False':
                out = open('/bin/bh_parallel_mount', 'w')
                line = 'mount -o bind %s /etc > /tmp/jump.tmp\n' % path1
                out.write(line)
                line = 'mount -o bind %s /var/lib/opkg > /tmp/jump.tmp\n' % path3
                out.write(line)
                line = 'mount -t unionfs -o dirs=%s:/usr=ro none /usr > /tmp/jump.tmp\n' % path2
                out.write(line)
                out.write('exit 0\n\n')
                out.close()
                system('chmod 0755 /bin/bh_parallel_mount')
        out = open('/bin/bh_jump', 'w')
        out.write('#!/bin/sh\n\n')
        out.write('telinit 4\n')
        if self.current_universe != 'Black Hole':
            out.write('fuser -km /etc > /tmp/jump.tmp\n')
            out.write('umount -l /etc > /tmp/jump.tmp\n')
            out.write('umount -l /usr > /tmp/jump.tmp\n')
            out.write('umount -l /var/lib/opkg > /tmp/jump.tmp\n')
        if self.destination != 'Black Hole':
            out.write('sleep 1\n')
            line = 'mount -o bind %s /etc > /tmp/jump.tmp\n' % path1
            out.write(line)
            line = 'mount -o bind %s /var/lib/opkg > /tmp/jump.tmp\n' % path3
            out.write(line)
            line = 'mount -t unionfs -o dirs=%s:/usr=ro none /usr > /tmp/jump.tmp\n' % path2
            out.write(line)
        out.write('sleep 1\n')
        out.write('telinit 3\n\n')
        out.write('exit 0\n\n')
        out.close()
        rc = system('chmod 0755 /bin/bh_jump')
        self.jump_on_close = True
        configfile.save()
        self.close()

    def check_origin(self):
        origin = self.whereIAm()
        if origin != 'Black Hole':
            msg = _('The Big Bang will collapse all of the Parallel Universes into the original Black Hole matrix.\nThis means that all of your Parallel Universes will be destroyed and turned back into Black Hole timespace.\n')
            msg += _('For this reason you have to save yourself by jumping back into Black Hole Universe before you start the Big Bang.')
            self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
        else:
            msg = _('The Big Bang will collapse all of the Parallel Universes into the original Black Hole matrix.\nThis means that all of your Parallel Universes will be destroyed and turned back into Black Hole timespace.\n')
            msg += _('Warning, all of the data stored in your Parallel Universes will be lost.\nAre you sure you want to start the Bing Bang?')
            self.session.openWithCallback(self.startbigBang, MessageBox, msg, MessageBox.TYPE_YESNO)

    def startbigBang(self, answer):
        if answer == True:
            self.session.openWithCallback(self.updateList, BhBigBang)

    def closE(self):
        if self.jump_on_close == True:
            self.session.nav.stopService()
            self.session.nav.shutdown()
            Console().ePopen('/bin/bh_jump')


class BhUniverseConfig(Screen, ConfigListScreen):
    skin = '\n\t<screen position="center,center" size="700,340" title="Parallel Universe Setup">\n\t\t<widget name="lab1" position="10,30" halign="center" size="680,60" zPosition="1" font="Regular;24" valign="top" transparent="1" />\n\t\t<widget name="config" position="10,100" size="680,110" scrollbarMode="showOnDemand" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="140,270" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="140,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />\n\t\t<ePixmap position="420,270" size="140,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />\n\t\t<widget name="key_green" position="420,270" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />\n\t</screen>'

    def __init__(self, session, universe):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Save'))
        msg = _('Setup %s Universe') % universe
        self['lab1'] = Label(msg)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.keyCancel,
         'back': self.keyCancel,
         'green': self.keySave}, -2)
        self.universe = universe
        self.updateList()

    def updateList(self):
        self.universe_lock = NoSave(ConfigYesNo(default=False))
        self.universe_pin = NoSave(ConfigInteger(limits=(0, 9999), default=0))
        self.universe_force_reboot = NoSave(ConfigYesNo(default=False))
        data = Bh_read_Universe_Cfg(self.universe)
        if data[0] == 'True':
            self.universe_lock.value = True
        self.universe_pin.value = int(data[1])
        if data[2] == 'True':
            self.universe_force_reboot.value = True
        item = getConfigListEntry(_('Universe access protected'), self.universe_lock)
        self.list.append(item)
        item = getConfigListEntry(_('Universe access pin'), self.universe_pin)
        self.list.append(item)
        item = getConfigListEntry(_('Force reboot in Black Hole'), self.universe_force_reboot)
        self.list.append(item)
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def whereIAm(self):
        ret = 'Black Hole'
        all = ['Avalon', 'Chaos', 'Ghost']
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/usr ') != -1:
                for a in all:
                    if line.find(a) != -1:
                        ret = a

                break

        f.close()
        return ret

    def keySave(self):
        fname = '/universe/.%s.cfg' % self.universe
        out = open(fname, 'w')
        line = 'universe_lock:' + str(self.universe_lock.value) + '\nuniverse_pin:' + str(self.universe_pin.value) + '\nuniverse_force_reboot:' + str(self.universe_force_reboot.value) + '\n'
        out.write(line)
        out.close()
        current_universe = self.whereIAm()
        if current_universe == self.universe:
            if self.universe_force_reboot.value == True:
                if fileExists('/bin/bh_parallel_mount'):
                    os_remove('/bin/bh_parallel_mount')
            elif not fileExists('/bin/bh_parallel_mount'):
                path = '/universe/' + self.universe
                path1 = path + '/etc'
                path2 = path + '/usr'
                path3 = path + '/var/lib/opkg'
                out = open('/bin/bh_parallel_mount', 'w')
                line = 'mount -o bind %s /etc > /tmp/jump.tmp\n' % path1
                out.write(line)
                line = 'mount -o bind %s /var/lib/opkg > /tmp/jump.tmp\n' % path3
                out.write(line)
                line = 'mount -t unionfs -o dirs=%s:/usr=ro none /usr > /tmp/jump.tmp\n' % path2
                out.write(line)
                out.write('exit 0\n\n')
                out.close()
                system('chmod 0755 /bin/bh_parallel_mount')
        self.close()

    def keyCancel(self):
        self.close()


class BhBigBang(Screen):
    skin = '\n\t<screen position="center,center" size="1270,720" title="Big Bang" backgroundColor="#000000"  flags="wfNoBorder" >\n\t\t<widget name="lab1" position="320,230" size="590,30" backgroundColor="#000000" halign="center"  valign="center" font="Regular;30" />\n\t\t<widget name="lab2" position="585,260" size="70,200" backgroundColor="#000000" halign="center" valign="center" font="Regular;50" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Please Wait, the Big Bang is in progress'))
        self['lab2'] = Label()
        self['actions'] = ActionMap(['OkCancelActions'], {'back': self.close})
        self.labtext = _('Please Wait, the Big Bang is in progress')
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updatepiX)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)

    def startShow(self):
        self.count = 0
        self.activityTimer.start(10)

    def updatepiX(self):
        running = True
        self.activityTimer.stop()
        if self.count == 0:
            self['lab2'].setText('3')
            cmd = 'rm -f -r /universe/Avalon'
            rc = system(cmd)
        elif self.count == 1:
            self['lab2'].setText('2')
            cmd = 'rm -f -r /universe/Chaos'
            rc = system(cmd)
        elif self.count == 2:
            self['lab2'].setText('1')
            cmd = 'rm -f -r /universe/Ghost'
            rc = system(cmd)
        elif self.count == 3:
            self['lab2'].setText('0')
            rc = system('chmod a+w /universe/.buildv')
            rc = system(' rm -f /universe/.buildv')
            rc = system(' rm -f /universe/.*.cfg')
        else:
            running = False
            self.session.openWithCallback(self.bigEnd, MessageBox, _('Your Universes have been re-inizialized. You can now start to rebuild your worlds.'), MessageBox.TYPE_INFO)
        if running == True:
            self.activityTimer.start(1500)
            self.count += 1

    def bigEnd(self, answer):
        self.close()

    def delTimer(self):
        del self.activityTimer


class BhRedp():

    def __init__(self):
        self['BhRedp'] = ActionMap(['InfobarExtensions'], {'BhRedpshow': self.showBhRedp})

    def showBhRedp(self):
        flash = True
        mounted = False
        bh_ver = BhU_check_proc_version()
        un_ver = bh_ver
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/universe') != -1:
                if line.find('ext') != -1:
                    mounted = True

        f.close()
        if fileExists('/.meoinfo'):
            flash = False
        if fileExists('/.bainfo'):
            flash = False
        if flash == True:
            if mounted == True:
                if fileExists('/universe/.buildv'):
                    f = open('/universe/.buildv', 'r')
                    un_ver = f.readline().strip()
                    f.close()
                else:
                    out = open('/universe/.buildv', 'w')
                    out.write(bh_ver)
                    out.close()
                    system('chmod a-w /universe/.buildv')
                if un_ver == bh_ver:
                    self.session.openWithCallback(self.callBhAction, BhRedPanel)
                else:
                    self.session.openWithCallback(self.callBhAction, BhRedWrong)
            else:
                self.session.openWithCallback(self.callBhAction, BhRedDisabled, '0')
        else:
            self.session.openWithCallback(self.callBhAction, BhRedDisabled, 'flash')

    def callBhAction(self, *args):
        if len(args):
            actionmap, context, action = args
            actionmap.action(context, action)
