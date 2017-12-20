from Screens.Screen import Screen
from enigma import eTimer
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Screens.Setup import Setup
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.config import config
from Tools.Directories import fileExists
from BhUtils import BhU_find_hdd
from os import system, statvfs, remove as os_remove

class DeliteHdd(Screen):
    skin = '\n\t<screen position="110,100" size="500,400" title="Black Hole E2 Hard Disk Panel">\n\t\t<widget name="infotext" position="10,10" size="490,260" font="Regular;16" />\n\t\t<widget name="lab1" position="20,280" size="100,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="120,280" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="120,280" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="20,350" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="170,350" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="320,350" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="20,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="170,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="320,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\t\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['infotext'] = ScrollLabel()
        self['lab1'] = Label(_('Status:'))
        self['labstop'] = Label(_('Standby'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Standby Now'))
        self['key_green'] = Label(_('Set Acoustic'))
        self['key_yellow'] = Label(_('Set Standby'))
        self.cur_state = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'back': self.close,
         'up': self['infotext'].pageUp,
         'left': self['infotext'].pageUp,
         'down': self['infotext'].pageDown,
         'right': self['infotext'].pageDown,
         'red': self.setStand,
         'green': self.setAcu,
         'yellow': self.setSsec})
        self.hdd_dev = BhU_find_hdd()
        self.hddloc = '/dev/' + self.hdd_dev
        self.onLayoutFinish.append(self.updateHdd)

    def myclose(self):
        self.activityTimer.stop()
        del self.activityTimer
        mybox = self.session.openWithCallback(self.domyclose, MessageBox, _('Sorry, Hard Disk not Found.'), type=MessageBox.TYPE_INFO)
        mybox.setTitle(_('Info'))

    def domyclose(self, ret):
        self.close()

    def updateHdd(self):
        if self.hdd_dev == '':
            self.activityTimer = eTimer()
            self.activityTimer.timeout.get().append(self.myclose)
            self.activityTimer.start(100, True)
        else:
            self['labstop'].hide()
            self['labrun'].hide()
            cmd = 'hdparm -C ' + self.hddloc + '> /tmp/hdpar.tmp'
            rc = system(cmd)
            strview = ''
            procf = '/proc/ide/hda/'
            if self.hddloc.find('host1') != -1:
                procf = '/proc/ide/hdc/'
            model = 'Generic'
            filename = '/sys/block/%s/device/model' % self.hdd_dev
            if fileExists(filename):
                model = file(filename).read().strip()
                strview += _('HARD DISK MODEL:') + ' \t' + model + '\n'
            size = '0'
            filename = '/sys/block/%s/size' % self.hdd_dev
            if fileExists(filename):
                cap = int(file(filename).read().strip())
                cap = cap / 1000 * 512 / 1000
                cap = '%d.%03d GB' % (cap / 1024, cap % 1024)
                strview += _('Disk Size:') + '     \t' + cap + '\n'
            free = _('Not mounted')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/hdd') != -1:
                    stat = statvfs('/media/hdd')
                    free = stat.f_bfree / 1000 * stat.f_bsize / 1000
                    free = '%d.%03d GB' % (free / 1024, free % 1024)
                    break

            f.close()
            strview += _('Available Space:') + '\t' + free + '\n'
            mysett = self.getHconf()
            cvalue1 = config.usage.hdd_standby.value
            if cvalue1 < 12:
                cvalue1 = 600
            cvalue = int(cvalue1) / 60
            mystand = str(cvalue)
            strview += _('Standby:') + '\t\t' + mystand + _(' min.\n')
            myfile = procf + 'settings'
            if fileExists(myfile):
                strview += '_______________________________________________\n'
                f = open(myfile, 'r')
                for line in f.readlines():
                    if line.find('--') != -1:
                        strview += '_______________________________________________\n'
                        continue
                    parts = line.strip().split()
                    if len(parts) > 3:
                        line = parts[0] + '\t' + parts[1] + '\t' + parts[2] + '\t' + parts[3]
                        strview += line + '\n'

                strview += '_______________________________________________\n\n'
                f.close()
            self.cur_state = False
            check = False
            if fileExists('/tmp/hdpar.tmp'):
                f = open('/tmp/hdpar.tmp', 'r')
                for line in f.readlines():
                    if line.find('active') != -1:
                        check = True

                f.close()
                os_remove('/tmp/hdpar.tmp')
            if check == False:
                self['labstop'].show()
            else:
                self['labrun'].show()
                self.cur_state = True
            self['infotext'].setText(strview)

    def setStand(self):
        if self.cur_state == True:
            cmd = 'hdparm -y ' + self.hddloc
            rc = system(cmd)
            self.updateHdd()
        else:
            mybox = self.session.open(MessageBox, _('Hard Disk is already sleeping'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))

    def setAcu(self):
        mysett = self.getHconf()
        curvalue = mysett[1]
        self.session.openWithCallback(self.SaveAcu, InputBox, title=_('Enter here the value for Hdd Acoustic:'), windowTitle=_('Hard Disk Setup'), text=curvalue, type=2)

    def SaveAcu(self, noise):
        if noise:
            mysett = self.getHconf()
            seconds = mysett[0]
            mylist = [seconds, noise]
            self.SaveHconf(mylist)

    def setSsec(self):
        self.session.openWithCallback(self.updateHdd, Setup, 'harddisk')

    def SaveSsec(self, seconds):
        if seconds:
            mysett = self.getHconf()
            noise = mysett[1]
            sec = int(seconds) * 60 / 5
            seconds = str(sec)
            mylist = [seconds, noise]
            self.SaveHconf(mylist)

    def SaveHconf(self, mylist):
        seconds = mylist[0]
        noise = mylist[1]
        out = open('/usr/bin/.hd_parm.sh', 'w')
        strview = '#!/bin/sh\n\nhdparm -S' + seconds + ' ' + self.hddloc + '\n'
        out.write(strview)
        strview = 'hdparm -M' + noise + ' ' + self.hddloc + '\n'
        out.write(strview)
        out.close()
        system('chmod 0755 /usr/bin/.hd_parm.sh')
        cmd = 'hdparm -S' + seconds + ' ' + self.hddloc
        rc = system(cmd)
        cmd = 'hdparm -M' + noise + ' ' + self.hddloc
        rc = system(cmd)
        mybox = self.session.open(MessageBox, _('New Settings Activated.'), MessageBox.TYPE_INFO)
        mybox.setTitle('Info')
        self.updateHdd()

    def getHconf(self):
        noise = '128'
        seconds = '120'
        if fileExists('/usr/bin/.hd_parm.sh'):
            f = open('/usr/bin/.hd_parm.sh', 'r')
            for line in f.readlines():
                if line.find('-S') != -1:
                    parts = line.strip().split(' ')
                    seconds = parts[1]
                    seconds = seconds.replace('-S', '')
                if line.find('-M') != -1:
                    parts = line.strip().split(' ')
                    noise = parts[1]
                    noise = noise.replace('-M', '')

            f.close()
        return [seconds, noise]
