from Screens.Screen import Screen
from Screens.ServiceInfo import ServiceInfo
from Screens.About import About
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Gauge import Gauge
from Components.Pixmap import Pixmap
from Components.ScrollLabel import ScrollLabel
from Tools.Directories import fileExists
from BhUtils import BhU_find_hdd
from os import system, remove as os_remove
from enigma import ePoint, eSize, eTimer
from random import randint

class DeliteInfo(Screen):
    skin = '\n\t<screen position="0,0" size="1280,720" title="Black Hole E2 System Info" flags="wfNoBorder">\n\t\t<ePixmap pixmap="skin_default/background_system.png" position="0,0" size="1280,720" alphatest="on"  />\n\t\t<widget name="ramg" position="94,80" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="swapg" position="212,80" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="memtg" position="377,76" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="spacetg" position="580,76" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="cffg" position="769,80" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="usbg" position="916,80" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="hddg" position="1060,80" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="flashg" position="200,317" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="hddtempg" position="312,317" size="100,100" zPosition="1" borderColor="#f23d21" transparent="1" />\n\t\t<widget name="smallmon" position="565,282" size="160,130" zPosition="1" font="Regular;16" valign="center" backgroundColor="black" />\n\t\t<widget name="spy1" size="40,40" position="143,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy2" size="40,40" position="243,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy3" size="40,40" position="295,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy4" size="40,40" position="393,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy5" size="40,40" position="446,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy6" size="40,40" position="800,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy7" size="40,40" position="851,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy8" size="40,40" position="949,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy9" size="40,40" position="1000,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy10" size="40,40" position="1097,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="spy11" size="40,40" position="1150,585" zPosition="1" pixmap="skin_default/spy_gray.png" alphatest="on" />\n\t\t<widget name="moni" size="0,0" position="644,350" zPosition="1" backgroundColor="#000000" />\n\t\t<widget name="monipix" size="560,560" position="364,80" zPosition="2" pixmap="skin_default/big_monitor.png" alphatest="on" />\n\t\t<widget name="moni2" size="500,430" position="394,110" font="Regular;20" zPosition="3" backgroundColor="#000000" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['hddtempg'] = Gauge()
        self['ramg'] = Gauge()
        self['swapg'] = Gauge()
        self['memtg'] = Gauge()
        self['spacetg'] = Gauge()
        self['cffg'] = Gauge()
        self['usbg'] = Gauge()
        self['hddg'] = Gauge()
        self['flashg'] = Gauge()
        self['spy1'] = Pixmap()
        self['spy2'] = Pixmap()
        self['spy3'] = Pixmap()
        self['spy4'] = Pixmap()
        self['spy5'] = Pixmap()
        self['spy6'] = Pixmap()
        self['spy7'] = Pixmap()
        self['spy8'] = Pixmap()
        self['spy9'] = Pixmap()
        self['spy10'] = Pixmap()
        self['spy11'] = Pixmap()
        self['smallmon'] = Label('')
        self['moni'] = Label('')
        self['moni2'] = Label('')
        self['monipix'] = Pixmap()
        self['smallmon'].hide()
        self['monipix'].hide()
        self['moni2'].hide()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'NumberActions'], {'ok': self.KeyOk,
         'back': self.KeyOk,
         'red': self.KeyRed,
         'green': self.KeyGreen,
         'yellow': self.KeyYellow,
         'blue': self.KeyBlue,
         '1': self.KeyOne,
         '2': self.KeyTwo,
         '3': self.KeyThree})
        self.extendedFlash = False
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateList)
        self.moni_state = 0
        self.moniTimer = eTimer()
        self.moniTimer.timeout.get().append(self.moveON)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)

    def startShow(self):
        self.smallmontxt = ''
        self.activityTimer.start(10)

    def updateList(self):
        self.activityTimer.stop()
        self.getMemo()
        self.getSpace()
        self.getSpyes()
        self.getHddtemp()
        self['smallmon'].setText(self.smallmontxt)
        self['smallmon'].show()

    def moniShow(self):
        self.x = 644
        self.y = 350
        self.w = 0
        self.h = 0
        self.moniTimer.start(10)

    def moveON(self):
        self.moniTimer.stop()
        self['moni'].instance.move(ePoint(int(self.x), int(self.y)))
        self['moni'].instance.resize(eSize(int(self.w), int(self.h)))
        if self.x > 364:
            self.x -= 280 / 20
        if self.y > 80:
            self.y -= 270 / 20
        if self.h < 560:
            self.h += 560 / 20
        if self.w < 560:
            self.w += 560 / 20
            self.moniTimer.start(80)
        else:
            self['monipix'].show()
            self['moni2'].show()
            self.moni_state = 1

    def KeyOk(self):
        if self.moni_state == 1:
            self['moni'].instance.resize(eSize(0, 0))
            self['monipix'].hide()
            self['moni2'].hide()
            self.moni_state = 0
        else:
            self.close()

    def getMemo(self):
        ramused = 0
        swapused = 0
        totused = 0
        rc = system('free > /tmp/ninfo.tmp')
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'Mem:':
                    ramused = int(int(parts[2]) * 100 / int(parts[1]))
                elif parts[0] == 'Swap:':
                    if int(parts[1]) > 1:
                        swapused = int(int(parts[2]) * 100 / int(parts[1]))
                elif parts[0] == 'Total:':
                    totused = int(int(parts[2]) * 100 / int(parts[1]))

            f.close()
            os_remove('/tmp/ninfo.tmp')
        self.smallmontxt += _('Ram in use: ') + str(ramused) + ' %\n'
        self.smallmontxt += _('Swap in use: ') + str(swapused) + ' %\n'
        self['ramg'].setValue(int(ramused * 100 / 120 + 50))
        self['swapg'].setValue(int(swapused * 100 / 120 + 50))
        self['memtg'].setValue(int(totused * 100 / 120 + 50))

    def getSpace(self):
        rc = system('df > /tmp/ninfo.tmp')
        flused = 0
        fltot = 0
        flperc = 0
        cfused = 0
        cftot = 0
        cfperc = 0
        usused = 0
        ustot = 0
        usperc = 0
        hdused = 0
        hdtot = 0
        hdperc = 0
        fperc = 0
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == '/':
                    strview = parts[totsp - 1].replace('%', '')
                    if strview.isdigit():
                        flperc = int(parts[totsp - 1].replace('%', ''))
                        fltot = int(parts[totsp - 4])
                        flused = int(parts[totsp - 3])
                if parts[totsp] == '/usr':
                    self.extendedFlash = True
                    strview = parts[totsp - 1].replace('%', '')
                    if strview.isdigit():
                        flperc = int(parts[totsp - 1].replace('%', ''))
                        fltot = int(parts[totsp - 4])
                        flused = int(parts[totsp - 3])
                if parts[totsp] == '/media/cf':
                    cfperc = int(parts[totsp - 1].replace('%', ''))
                    cftot = int(parts[totsp - 4])
                    cfused = int(parts[totsp - 3])
                if parts[totsp] == '/media/usb':
                    strview = parts[totsp - 1].replace('%', '')
                    if strview.isdigit():
                        usperc = int(parts[totsp - 1].replace('%', ''))
                        ustot = int(parts[totsp - 4])
                        usused = int(parts[totsp - 3])
                if parts[totsp] == '/media/hdd':
                    strview = parts[totsp - 1].replace('%', '')
                    if strview.isdigit():
                        hdperc = int(parts[totsp - 1].replace('%', ''))
                        hdtot = int(parts[totsp - 4])
                        hdused = int(parts[totsp - 3])

            f.close()
            os_remove('/tmp/ninfo.tmp')
            ftot = cftot + ustot + hdtot
            fused = int(cfused) + int(usused) + int(hdused)
            if ftot > 100:
                fperc = fused * 100 / ftot
        self.smallmontxt += _('Flash in use: ') + str(flperc) + ' %\n'
        self.smallmontxt += _('Cf in use: ') + str(cfperc) + ' %\n'
        self.smallmontxt += _('Usb in use: ') + str(usperc) + ' %\n'
        self.smallmontxt += _('Hdd in use: ') + str(hdperc) + ' %\n'
        self['spacetg'].setValue(int(fperc * 100 / 120 + 50))
        self['cffg'].setValue(int(cfperc * 100 / 120 + 50))
        self['usbg'].setValue(int(usperc * 100 / 120 + 50))
        self['hddg'].setValue(int(hdperc * 100 / 120 + 50))
        self['flashg'].setValue(int(flperc * 100 / 120 + 50))

    def getSpyes(self):
        atelnet = False
        aftp = False
        avpn = False
        asamba = False
        anfs = False
        rc = system('ps > /tmp/nvpn.tmp')
        if fileExists('/etc/inetd.conf'):
            f = open('/etc/inetd.conf', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'telnet':
                    atelnet = True
                if parts[0] == 'ftp':
                    aftp = True

            f.close()
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('openvpn') != -1:
                    avpn = True
                if line.find('smbd') != -1:
                    asamba = True
                if line.find('rpc.mountd') != -1:
                    anfs = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if atelnet == True:
            self['spy2'].hide()
        else:
            self['spy3'].hide()
        if aftp == True:
            self['spy4'].hide()
        else:
            self['spy5'].hide()
        if avpn == True:
            self['spy6'].hide()
        else:
            self['spy7'].hide()
        if asamba == True:
            self['spy8'].hide()
        else:
            self['spy9'].hide()
        if anfs == True:
            self['spy10'].hide()
        else:
            self['spy11'].hide()

    def getHddtemp(self):
        temperature = 'N/A'
        temperc = 0
        hdd_dev = BhU_find_hdd()
        hddloc = '/dev/' + hdd_dev
        if hdd_dev:
            cmd = 'hddtemp -w ' + hddloc + ' > /tmp/ninfo.tmp'
            rc = system(cmd)
            if fileExists('/tmp/ninfo.tmp'):
                f = open('/tmp/ninfo.tmp', 'r')
                for line in f.readlines():
                    if line.find('WARNING') != -1:
                        continue
                    parts = line.strip().split(':')
                    temperature = parts[2].strip()
                    pos = temperature.find(' ')
                    temperature = temperature[0:pos]
                    if temperature.isdigit():
                        temperc = int(temperature)
                    else:
                        temperature = 'N/A'

                f.close()
                os_remove('/tmp/ninfo.tmp')
        self['hddtempg'].setValue(temperc + 64)
        self.smallmontxt += 'HDD temp: ' + temperature + ' C'

    def KeyRed(self):
        if self.moni_state == 0:
            self.moniShow()
        mytext = ''
        ramused = 0
        ramtot = 0
        swapused = 0
        swaptot = 0
        totalused = 0
        totaltot = 0
        rc = system('free > /tmp/ninfo.tmp')
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'Mem:':
                    ramused = int(int(parts[2]) * 100 / int(parts[1]))
                    mytext += _('Ram in use: ') + str(ramused) + ' % \n'
                    mytext += _('Total: ') + parts[1] + '\t' + _('Used: ') + parts[2] + '\t' + _('Free: ') + parts[3] + '\n'
                elif parts[0] == 'Swap:':
                    swapused = 0
                    if int(parts[1]) > 1:
                        swapused = int(int(parts[2]) * 100 / int(parts[1]))
                    mytext += _('Swap in use: ') + str(swapused) + ' % \n'
                    mytext += _('Total: ') + parts[1] + '\t' + _('Used: ') + parts[2] + '\t' + _('Free: ') + parts[3] + '\n'
                elif parts[0] == 'Total:':
                    totused = int(int(parts[2]) * 100 / int(parts[1]))
                    mytext += _('Total in use: ') + str(totused) + ' % \n'

            f.close()
            os_remove('/tmp/ninfo.tmp')
        count = 0
        if fileExists('/proc/meminfo'):
            f = open('/proc/meminfo', 'r')
            for line in f.readlines():
                mytext += line
                count += 1
                if count == 13:
                    break

            f.close()
        self['moni2'].setText(mytext)

    def KeyGreen(self):
        if self.moni_state == 0:
            self.moniShow()
        rc = system('df > /tmp/ninfo.tmp')
        mytext = ''
        flused = 0
        fltot = 0
        flperc = 0
        cfused = 0
        cftot = 0
        cfperc = 0
        usused = 0
        ustot = 0
        usperc = 0
        hdused = 0
        hdtot = 0
        hdperc = 0
        mountflash = '/'
        if self.extendedFlash == True:
            mountflash = '/usr'
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                meas = 'M'
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == mountflash:
                    if flused:
                        continue
                    flused = parts[totsp - 1]
                    flperc = int(flused.replace('%', ''))
                    fltot = int(parts[totsp - 4])
                    if fltot > 1000000:
                        fltot = fltot / 1000
                        meas = 'Gb'
                    capacity = '%d.%03d ' % (fltot / 1000, fltot % 1000)
                    mytext += _('FLASH: ') + capacity + meas + _('   in use: ') + flused + '\n'
                    mytext += _('Total: ') + parts[totsp - 4] + _('   Used: ') + parts[totsp - 3] + _('   Free: ') + parts[totsp - 2] + '\n\n'
                    fltot = int(parts[totsp - 4])
                    flused = int(parts[totsp - 3])
                if parts[totsp] == '/media/cf':
                    if cfused:
                        continue
                    cfused = parts[totsp - 1]
                    cfperc = int(cfused.replace('%', ''))
                    cftot = int(parts[totsp - 4])
                    if cftot > 1000000:
                        cftot = cftot / 1000
                        meas = 'Gb'
                    capacity = '%d.%03d ' % (cftot / 1000, cftot % 1000)
                    mytext += 'CF: ' + capacity + meas + _('   in use: ') + cfused + '\n'
                    mytext += _('Total: ') + parts[totsp - 4] + _('   Used: ') + parts[totsp - 3] + _('   Free: ') + parts[totsp - 2] + '\n\n'
                    cftot = int(parts[totsp - 4])
                    cfused = int(parts[totsp - 3])
                if parts[totsp] == '/media/usb':
                    if usused:
                        continue
                    usused = parts[totsp - 1]
                    usperc = int(usused.replace('%', ''))
                    ustot = int(parts[totsp - 4])
                    if ustot > 1000000:
                        ustot = ustot / 1000
                        meas = 'Gb'
                    capacity = '%d.%03d ' % (ustot / 1000, ustot % 1000)
                    mytext += _('USB: ') + capacity + meas + _('   in use: ') + usused + '\n'
                    mytext += _('Total: ') + parts[totsp - 4] + _('   Used: ') + parts[totsp - 3] + _('   Free: ') + parts[totsp - 2] + '\n\n'
                    ustot = int(parts[totsp - 4])
                    usused = int(parts[totsp - 3])
                if parts[totsp] == '/media/hdd':
                    if hdused:
                        continue
                    strview = parts[totsp - 1].replace('%', '')
                    if strview.isdigit():
                        hdused = parts[totsp - 1]
                        hdperc = int(hdused.replace('%', ''))
                        hdtot = int(parts[totsp - 4])
                        if hdtot > 1000000:
                            hdtot = hdtot / 1000
                            meas = 'Gb'
                        capacity = '%d.%03d ' % (hdtot / 1000, hdtot % 1000)
                        mytext += _('HDD: ') + capacity + meas + _('   in use: ') + hdused + '\n'
                        mytext += _('Total: ') + parts[totsp - 4] + _('   Used: ') + parts[totsp - 3] + _('   Free: ') + parts[totsp - 2] + '\n\n'
                        hdtot = int(parts[totsp - 4])
                        hdused = int(parts[totsp - 3])

            f.close()
            os_remove('/tmp/ninfo.tmp')
            meas = 'M'
            ftot = fltot + cftot + ustot + hdtot
            fused = int(flused) + int(cfused) + int(usused) + int(hdused)
            ffree = ftot - fused
            fperc = 0
            if ftot > 100:
                fperc = fused * 100 / ftot
            if ftot > 1000000:
                ftot = ftot / 1000
                meas = 'Gb'
            if ftot > 1000000000:
                ftot = ftot / 1000000
                meas = 'Tera'
            ftot = '%d.%03d ' % (ftot / 1000, ftot % 1000)
            ftot += meas
            meas = 'M'
            if fused > 1000000:
                fused = fused / 1000
                meas = 'Gb'
            if fused > 1000000000:
                fused = fused / 1000000
                meas = 'Tera'
            fused = '%d.%03d ' % (fused / 1000, fused % 1000)
            fused += meas
            meas = 'M'
            if ffree > 1000000:
                ffree = ffree / 1000
                meas = 'Gb'
            if ffree > 1000000000:
                ffree = ffree / 1000000
                meas = 'Tera'
            ffree = '%d.%03d ' % (ffree / 1000, ffree % 1000)
            ffree += meas
            mytext += _('Total Space: ') + ftot + _('    in use: ') + str(fperc) + '% \n'
            mytext += _('Total: ') + ftot + _(' Used: ') + fused + _(' Free: ') + ffree
        self['moni2'].setText(mytext)

    def KeyYellow(self):
        if self.moni_state == 0:
            self.moniShow()
        mytext = ''
        count = 0
        if fileExists('/proc/stat'):
            f = open('/proc/stat', 'r')
            for line in f.readlines():
                if line.find('intr') != -1:
                    continue
                if line.find('cpu0') != -1:
                    continue
                mytext += line

            f.close()
        if fileExists('/proc/stat'):
            f = open('/proc/cpuinfo', 'r')
            for line in f.readlines():
                parts = line.strip().split(':')
                strview = parts[0].strip()
                strview2 = ''
                if len(parts) == 3:
                    strview2 = ' ' + parts[2]
                mytext += strview + ':  ' + parts[1] + strview2 + '\n'
                count += 1
                if count == 9:
                    break

            f.close()
        self['moni2'].setText(mytext)

    def KeyBlue(self):
        self.session.open(NabProcInfo)

    def KeyOne(self):
        self.session.open(NabEnsetInfo)

    def KeyTwo(self):
        self.session.open(ServiceInfo)

    def KeyThree(self):
        self.session.open(About)

    def delTimer(self):
        hdd_dev = BhU_find_hdd()
        hddloc = '/dev/' + hdd_dev
        if hdd_dev != '':
            cmd = 'hdparm -y ' + hddloc
            system(cmd)
        del self.activityTimer
        del self.moniTimer


class NabProcInfo(Screen):
    skin = '\n\t<screen position="70,110" size="580,380" title="Black Hole E2 Process Info">\n\t\t<ePixmap position="0,0" pixmap="skin_default/shout_back2.png" size="580,380" alphatest="on" />\n\t\t<widget name="pibartit" zPosition="2" position="10,1" size="560,30" font="Regular;18" valign="center" transparent="1" foregroundColor="white" backgroundColor="white" />\n\t\t<widget name="infotext" position="20,50" size="560,320" font="Regular;18" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['pibartit'] = Label(' Pid \t Uid \t Command')
        self['infotext'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions'], {'ok': self.close,
         'back': self.close,
         'up': self['infotext'].pageUp,
         'left': self['infotext'].pageUp,
         'down': self['infotext'].pageDown,
         'right': self['infotext'].pageDown})
        self.updatetext()

    def updatetext(self):
        strview = ''
        rc = system('ps > /tmp/ninfo.tmp')
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'PID':
                    continue
                strview += line + '\n'

            f.close()
            os_remove('/tmp/ninfo.tmp')
        self['infotext'].setText(strview)


class NabEnsetInfo(Screen):
    skin = '\n\t<screen position="110,95" size="500,405" title="Black Hole E2 Enigma Settings Info">\n\t\t<widget name="infotext" position="10,10" size="480,380" font="Regular;18" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['infotext'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions'], {'ok': self.close,
         'back': self.close,
         'up': self['infotext'].pageUp,
         'left': self['infotext'].pageUp,
         'down': self['infotext'].pageDown,
         'right': self['infotext'].pageDown})
        self.onLayoutFinish.append(self.updatetext)

    def updatetext(self):
        strview = ''
        if fileExists('/etc/enigma2/settings'):
            f = open('/etc/enigma2/settings', 'r')
            for line in f.readlines():
                strview += line

            f.close()
            self['infotext'].setText(strview)
