from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigNumber, NoSave
from Tools.Directories import fileExists
from os import system

class DeliteInadyn(Screen):
    skin = '\n\t<screen position="120,70" size="480,410" title="Black Hole E2 Inadyn Manager">\n\t\t<widget name="linactive" position="10,10" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32"  alphatest="on" />\n\t\t<widget name="lactive" position="10,10" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32"  alphatest="on" />\n\t\t<widget name="lab1" position="50,10" size="350,30" font="Regular;20" valign="center"  transparent="1"/>\n\t\t<widget name="lab2" position="10,50" size="230,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labtime" position="240,50" size="100,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<widget name="lab3" position="10,100" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labuser" position="160,100" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<widget name="lab4" position="10,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labpass" position="160,150" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<widget name="lab5" position="10,200" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labalias" position="160,200" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<widget name="sinactive" position="10,250" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32"  alphatest="on" />\n\t\t<widget name="sactive" position="10,250" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32"  alphatest="on" />\n\t\t<widget name="lab6" position="50,250" size="100,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labsys" position="160,250" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>\n\t\t<widget name="lab7" position="10,300" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="160,300" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="160,300" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="20,360" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="170,360" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="320,360" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="20,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="170,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="320,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Activate Inadyn'))
        self['lactive'] = Pixmap()
        self['linactive'] = Pixmap()
        self['lab2'] = Label(_('Time Update in Minutes:'))
        self['labtime'] = Label()
        self['lab3'] = Label(_('Username:'))
        self['labuser'] = Label()
        self['lab4'] = Label(_('Password:'))
        self['labpass'] = Label()
        self['lab5'] = Label(_('Alias:'))
        self['labalias'] = Label()
        self['sactive'] = Pixmap()
        self['sinactive'] = Pixmap()
        self['lab6'] = Label(_('System:'))
        self['labsys'] = Label()
        self['lab7'] = Label(_('Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running !'))
        self['key_red'] = Label(_('Start'))
        self['key_green'] = Label(_('Show Log'))
        self['key_yellow'] = Label(_('Setup'))
        self['lactive'].hide()
        self['sactive'].hide()
        self['labrun'].hide()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close,
         'red': self.restartIna,
         'green': self.inaLog,
         'yellow': self.setupin})
        self.onLayoutFinish.append(self.updateIna)

    def restartIna(self):
        if self.my_nabina_state == False:
            mybox = self.session.open(MessageBox, _('You have to Activate Inadyn before to start'), MessageBox.TYPE_INFO)
            mybox.setTitle('Info')
        else:
            rc = system('/usr/bin/inadyn_script.sh stop')
            rc = system('/usr/bin/inadyn_script.sh start')
            rc = system('ps')
            self.updateIna()

    def updateIna(self):
        self['lactive'].hide()
        self['linactive'].hide()
        self['sactive'].hide()
        self['sinactive'].hide()
        self['labrun'].hide()
        self['labstop'].hide()
        self.my_nabina_state = False
        if fileExists('/usr/bin/inadyn_script.sh'):
            f = open('/usr/bin/inadyn_script.sh', 'r')
            for line in f.readlines():
                line = line.strip()
                if line.find('INADYN_ON=') != -1:
                    line = line[10:]
                    if line == '1':
                        self['lactive'].show()
                        self.my_nabina_state = True
                    else:
                        self['linactive'].show()
                elif line.find('INADYN_USERNAME=') != -1:
                    line = line[16:]
                    self['labuser'].setText(line)
                elif line.find('INADYN_PASSWORD=') != -1:
                    line = line[16:]
                    self['labpass'].setText(line)
                elif line.find('INADYN_ALIAS=') != -1:
                    line = line[13:]
                    self['labalias'].setText(line)
                elif line.find('UPDATE_PERIOD=') != -1:
                    line = int(line[14:])
                    line = line / 1000 / 60
                    self['labtime'].setText(str(line))
                elif line.find('DYN_SYSTEM_ON=') != -1:
                    line = line[14:]
                    if line == '1':
                        self['sactive'].show()
                    else:
                        self['sinactive'].show()
                elif line.find('DYN_SYSTEM=') != -1:
                    line = line[11:]
                    self['labsys'].setText(line)

            f.close()
        rc = system('ps > /tmp/ninadyn.tmp')
        check = False
        if fileExists('/tmp/ninadyn.tmp'):
            f = open('/tmp/ninadyn.tmp', 'r')
            for line in f.readlines():
                if line.find('inadyn') != -1:
                    check = True

            f.close()
            system('rm -f /tmp/ninadyn.tmp')
        if check == True:
            self['labstop'].hide()
            self['labrun'].show()
            self['key_red'].setText(_('Restart'))
        else:
            self['labstop'].show()
            self['labrun'].hide()
            self['key_red'].setText(_('Start'))

    def KeyOk(self):
        pass

    def setupin(self):
        self.session.openWithCallback(self.updateIna, DeliteInaSetup)

    def inaLog(self):
        self.session.open(DeliteInaLog)


class DeliteInaSetup(Screen, ConfigListScreen):
    skin = '\n\t<screen position="140,120" size="440,300" title="Black Hole E2 Inadyn Setup">\n\t\t<widget name="config" position="10,10" size="420,240" scrollbarMode="showOnDemand" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="150,250" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="150,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.saveIna,
         'back': self.close,
         'green': self.vkeyb})
        self.updateList()

    def updateList(self):
        self.ina_active = NoSave(ConfigYesNo(default='False'))
        self.ina_user = NoSave(ConfigText(fixed_size=False))
        self.ina_pass = NoSave(ConfigText(fixed_size=False))
        self.ina_alias = NoSave(ConfigText(fixed_size=False))
        self.ina_period = NoSave(ConfigNumber())
        self.ina_sysactive = NoSave(ConfigYesNo(default='False'))
        self.ina_system = NoSave(ConfigText(fixed_size=False))
        if fileExists('/usr/bin/inadyn_script.sh'):
            f = open('/usr/bin/inadyn_script.sh', 'r')
            for line in f.readlines():
                line = line.strip()
                if line.find('INADYN_ON=') != -1:
                    line = line[10:]
                    if line == '1':
                        self.ina_active.value = True
                    else:
                        self.ina_active.value = False
                    ina_active1 = getConfigListEntry(_('Activate Inadyn'), self.ina_active)
                    self.list.append(ina_active1)
                elif line.find('INADYN_USERNAME=') != -1:
                    line = line[16:]
                    self.ina_user.value = line
                    ina_user1 = getConfigListEntry(_('Username'), self.ina_user)
                    self.list.append(ina_user1)
                elif line.find('INADYN_PASSWORD=') != -1:
                    line = line[16:]
                    self.ina_pass.value = line
                    ina_pass1 = getConfigListEntry(_('Password'), self.ina_pass)
                    self.list.append(ina_pass1)
                elif line.find('INADYN_ALIAS=') != -1:
                    line = line[13:]
                    self.ina_alias.value = line
                    ina_alias1 = getConfigListEntry(_('Alias'), self.ina_alias)
                    self.list.append(ina_alias1)
                elif line.find('UPDATE_PERIOD=') != -1:
                    line = int(line[14:])
                    line = line / 1000 / 60
                    self.ina_period.value = line
                    ina_period1 = getConfigListEntry(_('Time Update in Minutes'), self.ina_period)
                    self.list.append(ina_period1)
                elif line.find('DYN_SYSTEM_ON=') != -1:
                    line = line[14:]
                    if line == '1':
                        self.ina_sysactive.value = True
                    else:
                        self.ina_sysactive.value = False
                    ina_sysactive1 = getConfigListEntry(_('Set System'), self.ina_sysactive)
                    self.list.append(ina_sysactive1)
                elif line.find('DYN_SYSTEM=') != -1:
                    line = line[11:]
                    self.ina_system.value = line
                    ina_system1 = getConfigListEntry(_('System'), self.ina_system)
                    self.list.append(ina_system1)

            f.close()
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def vkeyb(self):
        sel = self['config'].getCurrent()
        if sel:
            self.vkvar = sel[0]
            self.vki = self['config'].getCurrentIndex()
            value = 'xmeo'
            if self.vki == 1:
                value = self.ina_user.value
            elif self.vki == 2:
                value = self.ina_pass.value
            elif self.vki == 3:
                value = self.ina_alias.value
            elif self.vki == 6:
                value = self.ina_system.value
            if value != 'xmeo':
                self.session.openWithCallback(self.UpdateAgain, VirtualKeyBoard, title=self.vkvar, text=value)
            else:
                self.session.open(MessageBox, _('Please use Virtual Keyboard for text rows only:\n-Username\n-Password\n-Alias\n-System'), MessageBox.TYPE_INFO)

    def UpdateAgain(self, newt):
        self.list = []
        if newt is None:
            newt = ''
        if newt.strip() != '':
            if self.vki == 1:
                self.ina_user.value = newt
            elif self.vki == 2:
                self.ina_pass.value = newt
            elif self.vki == 3:
                self.ina_alias.value = newt
            elif self.vki == 6:
                self.ina_system.value = newt
            ina_active1 = getConfigListEntry(_('Activate Inadyn'), self.ina_active)
            self.list.append(ina_active1)
            ina_user1 = getConfigListEntry(_('Username'), self.ina_user)
            self.list.append(ina_user1)
            ina_pass1 = getConfigListEntry(_('Password'), self.ina_pass)
            self.list.append(ina_pass1)
            ina_alias1 = getConfigListEntry(_('Alias'), self.ina_alias)
            self.list.append(ina_alias1)
            ina_period1 = getConfigListEntry(_('Time Update in Minutes'), self.ina_period)
            self.list.append(ina_period1)
            ina_sysactive1 = getConfigListEntry(_('Set System'), self.ina_sysactive)
            self.list.append(ina_sysactive1)
            ina_system1 = getConfigListEntry(_('System'), self.ina_system)
            self.list.append(ina_system1)
            self['config'].list = self.list
            self['config'].l.setList(self.list)

    def saveIna(self):
        if fileExists('/usr/bin/inadyn_script.sh'):
            inme = open('/usr/bin/inadyn_script.sh', 'r')
            out = open('/usr/bin/inadyn_script.tmp', 'w')
            for line in inme.readlines():
                line = line.replace('\n', '')
                if line.find('INADYN_ON=') != -1:
                    strview = '0'
                    if self.ina_active.value == True:
                        strview = '1'
                    line = 'INADYN_ON=' + strview
                elif line.find('INADYN_USERNAME=') != -1:
                    line = 'INADYN_USERNAME=' + self.ina_user.value.strip()
                elif line.find('INADYN_PASSWORD=') != -1:
                    line = 'INADYN_PASSWORD=' + self.ina_pass.value.strip()
                elif line.find('INADYN_ALIAS=') != -1:
                    line = 'INADYN_ALIAS=' + self.ina_alias.value.strip()
                elif line.find('UPDATE_PERIOD=') != -1:
                    strview = self.ina_period.value * 1000 * 60
                    strview = str(strview)
                    line = 'UPDATE_PERIOD=' + strview
                elif line.find('DYN_SYSTEM_ON=') != -1:
                    strview = '0'
                    if self.ina_sysactive.value == True:
                        strview = '1'
                    line = 'DYN_SYSTEM_ON=' + strview
                elif line.find('DYN_SYSTEM=') != -1:
                    line = 'DYN_SYSTEM=' + self.ina_system.value.strip()
                out.write(line + '\n')

            out.close()
            inme.close()
        else:
            self.session.open(MessageBox, _('Sorry Inadyn Script is Missing'), MessageBox.TYPE_INFO)
            self.close()
        if fileExists('/usr/bin/inadyn_script.tmp'):
            system('mv -f  /usr/bin/inadyn_script.tmp /usr/bin/inadyn_script.sh')
            system('chmod 0755 /usr/bin/inadyn_script.sh')
        self.myStop()

    def myStop(self):
        self.close()


class DeliteInaLog(Screen):
    skin = '\n\t<screen position="140,120" size="440,300" title="Black Hole E2 Inadyn Log">\n\t\t<widget name="infotext" position="10,10" size="420,280" font="Regular;18" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['infotext'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'up': self['infotext'].pageUp,
         'down': self['infotext'].pageDown})
        strview = ''
        if fileExists('/var/log/inadyn.log'):
            f = open('/var/log/inadyn.log', 'r')
            for line in f.readlines():
                strview += line

            f.close()
        self['infotext'].setText(strview)
