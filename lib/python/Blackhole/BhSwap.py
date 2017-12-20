from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Tools.Directories import fileExists
from os import system, stat as mystat
import stat

class DeliteSwap(Screen):
    skin = '\n\t<screen position="150,130" size="420,340" title="Dream Elite Swap File Manager">\n\t\t<widget name="linactive" position="10,10" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32"  alphatest="on" />\n\t\t<widget name="lactive" position="10,10" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32"  alphatest="on" />\n\t\t<widget name="lab1" position="50,10" size="260,30" font="Regular;20" valign="center"  transparent="1"/>\n\t\t<widget name="lab2" position="10,100" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labplace" position="160,100" size="220,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<widget name="lab3" position="10,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labsize" position="160,150" size="220,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<widget name="lab4" position="10,200" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="160,200" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="160,200" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,290" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,290" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,290" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="0,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="140,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="280,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Enable Swap at startup'))
        self['lactive'] = Pixmap()
        self['linactive'] = Pixmap()
        self['lab2'] = Label(_('Swap Place:'))
        self['labplace'] = Label()
        self['lab3'] = Label(_('Swap Size:'))
        self['labsize'] = Label()
        self['lab4'] = Label(_('Status:'))
        self['labstop'] = Label(_('Inactive'))
        self['labrun'] = Label(_('Active'))
        self['key_red'] = Label(_('Activate'))
        self['key_green'] = Label(_('Create'))
        self['key_yellow'] = Label(_('Autostart'))
        self.swap_active = False
        self.swap_place = ''
        self.new_place = ''
        self.autos_start = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.actDeact,
         'green': self.createDel,
         'yellow': self.autoSsWap})
        self.onLayoutFinish.append(self.updateSwap)

    def updateSwap(self):
        self['lactive'].hide()
        self['linactive'].hide()
        self['labrun'].hide()
        self['labstop'].hide()
        self['key_green'].setText(_('Create'))
        rc = system('cat /proc/swaps > /tmp/swap.tmp')
        self.autos_start = False
        if fileExists('/usr/bin/.Bhautoswap'):
            self['lactive'].show()
            self.autos_start = True
        else:
            self['linactive'].show()
        fileplace = ''
        self.swap_place = ''
        if fileExists('/mnt/cf/swapfile'):
            fileplace = 'COMPACT FLASH'
            self.swap_place = '/mnt/cf/swapfile'
        elif fileExists('/mnt/usb/swapfile'):
            fileplace = 'USB'
            self.swap_place = '/mnt/usb/swapfile'
        elif fileExists('/mnt/card/swapfile'):
            fileplace = 'SD'
            self.swap_place = '/mnt/card/swapfile'
        elif fileExists('/hdd/swapfile'):
            fileplace = 'HARD DRIVE'
            self.swap_place = '/hdd/swapfile'
        self['labplace'].setText(fileplace)
        filesize = 0
        if fileplace != '':
            self['key_green'].setText(_('Delete'))
            info = mystat(self.swap_place)
            filesize = info[stat.ST_SIZE]
        mu = ''
        if filesize >= 1073741824:
            filesize = filesize / 1073741824
            mu = ' GB'
        elif filesize > 1048576:
            filesize = filesize / 1048576
            mu = ' MB'
        filesize = str(filesize) + mu
        self['labsize'].setText(filesize)
        self.swap_active = False
        if fileExists('/tmp/swap.tmp'):
            f = open('/tmp/swap.tmp', 'r')
            for line in f.readlines():
                if line.find('swapfile') != -1:
                    self.swap_active = True

            f.close()
            system('rm -f /tmp/swap.tmp')
        if self.swap_active == True:
            self['labrun'].show()
            self['key_red'].setText(_('Deactivate'))
        else:
            self['labstop'].show()
            self['key_red'].setText(_('Activate'))

    def actDeact(self):
        if self.swap_active == True:
            cmd = 'swapoff ' + self.swap_place
            rc = system(cmd)
            self.updateSwap()
        elif self.swap_active == False:
            if self.swap_place != '':
                cmd = 'mkswap ' + self.swap_place
                rc = system(cmd)
                cmd = 'swapon ' + self.swap_place
                rc = system(cmd)
                self.updateSwap()
            else:
                mybox = self.session.open(MessageBox, _('Swap File not found. You have to create the file before to activate.'), MessageBox.TYPE_INFO)
                mybox.setTitle(_('Info'))

    def createDel(self):
        if self.swap_active == True:
            cmd = 'swapoff ' + self.swap_place
            rc = system(cmd)
        if self.swap_place != '':
            cmd = 'rm -f ' + self.swap_place
            rc = system(cmd)
            system('rm -f /usr/bin/.Bhautoswap')
            mybox = self.session.open(MessageBox, _('Swap File Deleted and Autostart Deactivated.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            self.updateSwap()
        else:
            self.doCreateSwap()

    def doCreateSwap(self):
        mycf = myusb = mysd = myhdd = ''
        myoptions = []
        if fileExists('/proc/mounts'):
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/mnt/cf') != -1:
                    mycf = '/mnt/cf/'
                elif line.find('/media/cf') != -1:
                    mycf = '/mnt/cf/'
                elif line.find('/mnt/usb') != -1:
                    myusb = '/mnt/usb/'
                elif line.find('/media/usb') != -1:
                    myusb = '/mnt/usb/'
                elif line.find('/mnt/card') != -1:
                    mysd = '/mnt/card/'
                elif line.find('/media/card') != -1:
                    mysd = '/mnt/card/'
                elif line.find('/hdd') != -1:
                    myhdd = '/mnt/hdd/'
                elif line.find('/universe') != -1:
                    myhdd = '/universe/'

            f.close()
        if mycf:
            myoptions.append(['COMPACT FLASH', mycf])
        if myusb:
            myoptions.append(['USB', myusb])
        if mysd:
            myoptions.append(['SD', mysd])
        if myhdd:
            myoptions.append(['HARD DRIVE', myhdd])
        self.session.openWithCallback(self.doCSplace, ChoiceBox, title=_('Select the Swap File Place:'), list=myoptions)

    def doCSplace(self, name):
        if name:
            self.new_place = name[1]
            myoptions = [['8 MB', '8192'],
             ['16 MB', '16384'],
             ['32 MB', '32768'],
             ['64 MB', '65536'],
             ['128 MB', '131072'],
             ['256 MB', '262144'],
             ['512 MB', '524288'],
             ['1 GB', '1048576'],
             ['2 GB', '2097152']]
            self.session.openWithCallback(self.doCSsize, ChoiceBox, title=_('Select the Swap File Size:'), list=myoptions)

    def doCSsize(self, size):
        if size:
            size = size[1]
            myfile = self.new_place + 'swapfile'
            cmd = 'dd if=/dev/zero of=' + myfile + ' bs=1024 count=' + size + ' 2>/dev/null'
            rc = system(cmd)
            if rc == 0:
                mybox = self.session.open(MessageBox, _('Swap File successfully created.'), MessageBox.TYPE_INFO)
                mybox.setTitle('Info')
                self.updateSwap()
            else:
                mybox = self.session.open(MessageBox, _('Swap File creation Failed. Check for Available space.'), MessageBox.TYPE_INFO)
                mybox.setTitle(_('Info'))

    def autoSsWap(self):
        if fileExists('/usr/bin/.Bhautoswap'):
            system('rm -f /usr/bin/.Bhautoswap')
            mybox = self.session.open(MessageBox, _('Swap file Automatic Startup Disabled'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
        elif self.swap_place:
            strview = '#!/bin/sh\nmkswap ' + self.swap_place + '\nswapon ' + self.swap_place + '\n'
            out = open('/usr/bin/.Bhautoswap', 'w')
            out.write(strview)
            out.close()
            system('chmod 0755 /usr/bin/.Bhautoswap')
            mybox = self.session.open(MessageBox, _('Swap file Automatic Startup Enabled'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
        else:
            mybox = self.session.open(MessageBox, _('You have to create a Swap File before to activate the autostart.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
        self.updateSwap()
