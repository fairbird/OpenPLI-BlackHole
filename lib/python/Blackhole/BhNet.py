from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Components.Label import Label
from Components.Sources.List import List
from Components.Network import iNetwork
from Tools.Directories import fileExists
from os import system, rename as os_rename, remove as os_remove, chdir
from os.path import isdir
from Plugins.SystemPlugins.NetworkBrowser.NetworkBrowser import NetworkBrowser
from enigma import eServiceCenter, eServiceReference, eTimer

class DeliteOpenvpn(Screen):
    skin = '\n\t<screen position="80,150" size="560,310" title="Black Hole E2 OpenVpn Panel">\n\t\t<widget name="lab1" position="20,20" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab1a" position="170,16" size="370,60" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,90" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labactive" position="170,90" size="250,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab3" position="20,160" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="170,160" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="170,160" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="420,260" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t<widget name="key_blue" position="420,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Vpn Version: '))
        self['lab1a'] = Label(_('OpenVPN Panel - by Black Hole Team.'))
        self['lab2'] = Label(_('Startup Module:'))
        self['labactive'] = Label(_('Inactive'))
        self['lab3'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Start'))
        self['key_green'] = Label(_('Stop'))
        self['key_yellow'] = Label(_('Set Active'))
        self['key_blue'] = Label(_('Show Log'))
        self.my_vpn_active = False
        self.my_vpn_run = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.restartVpn,
         'green': self.stopVpnstop,
         'yellow': self.activateVpn,
         'blue': self.Vpnshowlog})
        self.onLayoutFinish.append(self.updateVpn)

    def activateVpn(self):
        myline = 'AUTOSTART="all"'
        mymess = _('OpenVpn Enabled. Autostart activated.')
        if self.my_vpn_active == True:
            myline = 'AUTOSTART="none"'
            mymess = _('OpenVpn disabled.')
        if fileExists('/usr/bin/openvpn_script.sh'):
            inme = open('/usr/bin/openvpn_script.sh', 'r')
            out = open('/usr/bin/openvpn_script.tmp', 'w')
            for line in inme.readlines():
                if line.find('AUTOSTART="') != -1:
                    line = myline + '\n'
                out.write(line)

            out.close()
            inme.close()
        if fileExists('/usr/bin/openvpn_script.tmp'):
            os_rename('/usr/bin/openvpn_script.tmp', '/usr/bin/openvpn_script.sh')
            system('chmod 0755 /usr/bin/openvpn_script.sh')
        mybox = self.session.open(MessageBox, mymess, MessageBox.TYPE_INFO)
        mybox.setTitle('Info')
        self.updateVpn()

    def restartVpn(self):
        if self.my_vpn_active == False:
            mybox = self.session.open(MessageBox, _('You have to Activate OpenVpn before to start'), MessageBox.TYPE_INFO)
            mybox.setTitle('Info')
        elif self.my_vpn_active == True and self.my_vpn_run == False:
            rc = system('/usr/bin/openvpn_script.sh start')
            rc = system('ps')
            self.updateVpn()
        elif self.my_vpn_active == True and self.my_vpn_run == True:
            rc = system('/usr/bin/openvpn_script.sh restart')
            rc = system('ps')
            self.updateVpn()

    def stopVpnstop(self):
        if self.my_vpn_run == True:
            rc = system('/usr/bin/openvpn_script.sh stop')
            rc = system('ps')
            self.updateVpn()

    def Vpnshowlog(self):
        self.session.open(DeliteVpnLog)

    def updateVpn(self):
        rc = system('ps > /tmp/nvpn.tmp')
        self['labrun'].hide()
        self['labstop'].hide()
        self['labactive'].setText(_('Inactive'))
        self['key_yellow'].setText(_('Set Active'))
        self.my_vpn_active = False
        self.my_vpn_run = False
        if fileExists('/usr/bin/openvpn_script.sh'):
            f = open('/usr/bin/openvpn_script.sh', 'r')
            for line in f.readlines():
                if line.find('AUTOSTART="all"') != -1:
                    self['labactive'].setText(_('Active/Autostart enabled'))
                    self['key_yellow'].setText(_('Deactivate'))
                    self.my_vpn_active = True

            f.close()
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('openvpn') != -1:
                    self.my_vpn_run = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if self.my_vpn_run == True:
            self['labstop'].hide()
            self['labrun'].show()
            self['key_red'].setText(_('Restart'))
        else:
            self['labstop'].show()
            self['labrun'].hide()
            self['key_red'].setText(_('Start'))


class DeliteVpnLog(Screen):
    skin = '\n\t<screen position="80,100" size="560,400" title="Black Hole OpenVpn Log">\n\t\t<widget name="infotext" position="10,10" size="540,380" font="Regular;18" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['infotext'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'up': self['infotext'].pageUp,
         'down': self['infotext'].pageDown})
        strview = ''
        rc = system('tail /etc/openvpn/openvpn.log > /etc/openvpn/tmp.log')
        if fileExists('/etc/openvpn/tmp.log'):
            f = open('/etc/openvpn/tmp.log', 'r')
            for line in f.readlines():
                strview += line

            f.close()
            os_remove('/etc/openvpn/tmp.log')
        self['infotext'].setText(strview)


class DeliteSamba(Screen):
    skin = '\n\t<screen position="150,150" size="420,310" title="Black Hole Samba Panel">\n\t\t<widget name="lab1" position="20,50" size="200,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labactive" position="220,50" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,100" size="200,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="220,100" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="220,100" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Samba Autostart: '))
        self['labactive'] = Label(_('Disabled'))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Start'))
        self['key_green'] = Label(_('Stop'))
        self['key_yellow'] = Label(_('Autostart'))
        self.my_samba_active = False
        self.my_samba_run = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.NSambaStart,
         'green': self.NSambaStop,
         'yellow': self.NSambaset})
        self.onLayoutFinish.append(self.updateSamb)

    def NSambaStart(self):
        if self.my_samba_run == False:
            rc = system('smbd -D')
            rc = system('nmbd -D')
            self.updateSamb()

    def NSambaStop(self):
        if self.my_samba_run == True:
            rc = system('killall -9 nmbd')
            rc = system('killall -9 smbd')
            self.updateSamb()

    def NSambaset(self):
        mymess = _('Samba Autostart Enabled.')
        if fileExists('/etc/network/if-up.d/01samba-start'):
            rc = system('rm -f /etc/network/if-up.d/01samba-start')
            rc = system('rm -f /etc/network/if-down.d/01samba-kill')
            mymess = _('Samba Autostart Disabled.')
        else:
            out = open('/etc/network/if-up.d/01samba-start', 'w')
            strview = '#!/bin/sh\nsmbd -D\nnmbd -D\n'
            out.write(strview)
            out.close()
            system('chmod 0755 /etc/network/if-up.d/01samba-start')
            out = open('/etc/network/if-down.d/01samba-kill', 'w')
            strview = '#!/bin/sh\nkillall -9 smbd\nkillall -9 nmbd\n'
            out.write(strview)
            out.close()
            system('chmod 0755 /etc/network/if-down.d/01samba-kill')
        mybox = self.session.open(MessageBox, mymess, MessageBox.TYPE_INFO)
        mybox.setTitle(_('Info'))
        self.updateSamb()

    def updateSamb(self):
        rc = system('ps > /tmp/nvpn.tmp')
        self['labrun'].hide()
        self['labstop'].hide()
        self['labactive'].setText(_('Disabled'))
        self.my_samba_active = False
        self.my_samba_run = False
        if fileExists('/etc/network/if-up.d/01samba-start'):
            self['labactive'].setText(_('Enabled'))
            self.my_samba_active = True
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('smbd') != -1:
                    self.my_samba_run = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if self.my_samba_run == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()


class DeliteTelnet(Screen):
    skin = '\n\t<screen position="190,150" size="340,310" title="Black Hole Telnet Panel">\n\t\t<widget name="lab1" position="20,30" size="300,60" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="170,150" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="170,150" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="20,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="180,260" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="20,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="180,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('You can disable Telnet Server and use ssh to login to your box.'))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Enable'))
        self['key_green'] = Label(_('Disable'))
        self.my_telnet_active = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.NTelnetStart,
         'green': self.NTelnetStop})
        self.onLayoutFinish.append(self.updateTeln)

    def NTelnetStart(self):
        if self.my_telnet_active == False:
            if fileExists('/etc/inetd.conf'):
                inme = open('/etc/inetd.conf', 'r')
                out = open('/etc/inetd.tmp', 'w')
                for line in inme.readlines():
                    if line.find('telnetd') != -1:
                        line = line.replace('#', '')
                    out.write(line)

                out.close()
                inme.close()
            if fileExists('/etc/inetd.tmp'):
                system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
                rc = system('killall -HUP inetd')
                rc = system('ps')
                mybox = self.session.open(MessageBox, _('Telnet service Enabled.'), MessageBox.TYPE_INFO)
                mybox.setTitle('Info')
                self.updateTeln()

    def NTelnetStop(self):
        if self.my_telnet_active == True:
            if fileExists('/etc/inetd.conf'):
                inme = open('/etc/inetd.conf', 'r')
                out = open('/etc/inetd.tmp', 'w')
                for line in inme.readlines():
                    if line.find('telnetd') != -1:
                        line = '#' + line
                    out.write(line)

                out.close()
                inme.close()
            if fileExists('/etc/inetd.tmp'):
                system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
                rc = system('killall -HUP inetd')
                rc = system('ps')
                mybox = self.session.open(MessageBox, _('Telnet service Disabled.'), MessageBox.TYPE_INFO)
                mybox.setTitle('Info')
                self.updateTeln()

    def updateTeln(self):
        self['labrun'].hide()
        self['labstop'].hide()
        self.my_telnet_active = False
        if fileExists('/etc/inetd.conf'):
            f = open('/etc/inetd.conf', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'telnet':
                    self.my_telnet_active = True

            f.close()
        if self.my_telnet_active == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()


class DeliteFtp(Screen):
    skin = '\n\t<screen position="190,150" size="340,310" title="Black Hole Ftp Panel">\n\t\t<widget name="lab1" position="20,30" size="300,60" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="170,150" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="170,150" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="20,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="180,260" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="20,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="180,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Ftpd service type: Vsftpd server (Very Secure FTP Daemon)'))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Enable'))
        self['key_green'] = Label(_('Disable'))
        self.my_ftp_active = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.NFtpStart,
         'green': self.NFtpStop})
        self.onLayoutFinish.append(self.updateFtp)

    def NFtpStart(self):
        if self.my_ftp_active == False:
            if fileExists('/etc/inetd.conf'):
                inme = open('/etc/inetd.conf', 'r')
                out = open('/etc/inetd.tmp', 'w')
                for line in inme.readlines():
                    if line.find('vsftpd') != -1:
                        line = line.replace('#', '')
                    out.write(line)

                out.close()
                inme.close()
            if fileExists('/etc/inetd.tmp'):
                system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
                rc = system('killall -HUP inetd')
                rc = system('ps')
                mybox = self.session.open(MessageBox, _('Ftp service Enabled.'), MessageBox.TYPE_INFO)
                mybox.setTitle(_('Info'))
                self.updateFtp()

    def NFtpStop(self):
        if self.my_ftp_active == True:
            if fileExists('/etc/inetd.conf'):
                inme = open('/etc/inetd.conf', 'r')
                out = open('/etc/inetd.tmp', 'w')
                for line in inme.readlines():
                    if line.find('vsftpd') != -1:
                        line = '#' + line
                    out.write(line)

                out.close()
                inme.close()
            if fileExists('/etc/inetd.tmp'):
                system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
                rc = system('killall -HUP inetd')
                rc = system('ps')
                mybox = self.session.open(MessageBox, _('Ftp service Disabled.'), MessageBox.TYPE_INFO)
                mybox.setTitle(_('Info'))
                self.updateFtp()

    def updateFtp(self):
        self['labrun'].hide()
        self['labstop'].hide()
        self.my_ftp_active = False
        if fileExists('/etc/inetd.conf'):
            f = open('/etc/inetd.conf', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'ftp':
                    self.my_ftp_active = True

            f.close()
        if self.my_ftp_active == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()


class BhNfsServer(Screen):
    skin = '\n\t<screen position="center,center" size="420,310" title="Black Hole Nfs Server Panel">\n\t\t<widget name="lab1" position="20,50" size="250,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labactive" position="270,50" size="150,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,100" size="250,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="270,100" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="270,100" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Nfs Server Autostart: '))
        self['labactive'] = Label(_('Disabled'))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Start'))
        self['key_green'] = Label(_('Stop'))
        self['key_yellow'] = Label(_('Autostart'))
        self.my_nfs_active = False
        self.my_nfs_run = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.NfsStart,
         'green': self.NfsStop,
         'yellow': self.Nfsset})
        self.onLayoutFinish.append(self.updateNfs)

    def NfsStart(self):
        if self.my_nfs_run == False:
            rc = system('/usr/bin/nfs_server_script.sh start')
            self.updateNfs()

    def NfsStop(self):
        if self.my_nfs_run == True:
            rc = system('/usr/bin/nfs_server_script.sh stop')
            self.updateNfs()

    def Nfsset(self):
        mymess = _('Nfs Autostart Enabled.')
        if fileExists('/etc/rc3.d/S20nfsserver'):
            rc = system('rm -f /etc/rc3.d/S20nfsserver')
            mymess = _('Nfs Autostart Disabled.')
        else:
            system('ln -s /usr/bin/nfs_server_script.sh /etc/rc3.d/S20nfsserver')
        mybox = self.session.open(MessageBox, mymess, MessageBox.TYPE_INFO)
        mybox.setTitle('Info')
        self.updateNfs()

    def updateNfs(self):
        rc = system('ps > /tmp/nvpn.tmp')
        self['labrun'].hide()
        self['labstop'].hide()
        self['labactive'].setText(_('Disabled'))
        self.my_nfs_active = False
        self.my_nfs_run = False
        if fileExists('/etc/rc3.d/S20nfsserver'):
            self['labactive'].setText(_('Enabled'))
            self.my_nfs_active = True
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('rpc.mountd') != -1:
                    self.my_nfs_run = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if self.my_nfs_run == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()


class BhDjmount(Screen):
    skin = '\n\t<screen position="center,center" size="602,305" title="Black Hole UPnP Client Panel">\n\t\t<widget name="lab1" position="20,30" size="580,60" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,150" size="300,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="320,150" size="150,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="320,150" size="150,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="125,260" size="150,30" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="325,260" size="150,30" alphatest="on"/>\n\t\t<widget name="key_red" position="125,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t\t<widget name="key_green" position="325,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('djmount: mount server in /media/upnp'))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Enable'))
        self['key_green'] = Label(_('Disable'))
        self.my_serv_active = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.ServStart,
         'green': self.ServStop})
        self.onLayoutFinish.append(self.updateServ)

    def ServStart(self):
        if self.my_serv_active == False:
            rc = system('ln -s ../init.d/djmount /etc/rc3.d/S20djmount')
            rc = system('/etc/init.d/djmount start')
            mybox = self.session.open(MessageBox, _('UPnP Client Enabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle('Info')
            self.updateServ()

    def ServStop(self):
        if self.my_serv_active == True:
            rc = system('/etc/init.d/djmount stop')
            if fileExists('/etc/rc3.d/S20djmount'):
                os_remove('/etc/rc3.d/S20djmount')
            mybox = self.session.open(MessageBox, _('UPnP Client Disabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            rc = system('sleep 1')
            self.updateServ()

    def updateServ(self):
        self['labrun'].hide()
        self['labstop'].hide()
        rc = system('ps > /tmp/nvpn.tmp')
        self.my_serv_active = False
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('djmount') != -1:
                    self.my_serv_active = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if self.my_serv_active == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()


class BhMediatomb(Screen):
    skin = '\n\t<screen position="center,center" size="602,405" title="Black Hole UPnP Mediatomb Server Panel">\n\t\t<widget name="lab1" position="20,20" size="580,260" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,300" size="300,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="320,300" size="150,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="320,300" size="150,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="125,360" size="150,30" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="325,360" size="150,30" alphatest="on"/>\n\t\t<widget name="key_red" position="125,362" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t\t<widget name="key_green" position="325,362" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        mytext = _('Mediatomb: UPnP media server Black Hole version.\nMediatomb is fully configured for your box and ready to work. Just enable it and play.\nMediatomb include a nice web interface url to manage your media.\n\nMediatomb webif url: http://ip_box:49152\nMediatomb configs: /.mediatomb/config.xml\nMediatomb docs & howto: http://mediatomb.cc/')
        self['lab1'] = Label(mytext)
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Enable'))
        self['key_green'] = Label(_('Disable'))
        self.my_serv_active = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.ServStart,
         'green': self.ServStop})
        self.onLayoutFinish.append(self.updateServ)

    def ServStart(self):
        rc = system('ps > /tmp/nvpn.tmp')
        minidlna_active = False
        f = open('/tmp/nvpn.tmp', 'r')
        for line in f.readlines():
            if line.find('minidlna') != -1:
                minidlna_active = True

        f.close()
        os_remove('/tmp/nvpn.tmp')
        if self.my_serv_active == True:
            self.session.open(MessageBox, _('Mediatomb already up and running.'), MessageBox.TYPE_INFO)
        elif minidlna_active == True:
            self.session.open(MessageBox, _('Sorry you cannot run two UpnP Servers togheter. Please disable minidlna before to run Mediatomb.'), MessageBox.TYPE_INFO)
        else:
            rc = system('ln -s ../init.d/mediatomb /etc/rc3.d/S20mediatomb')
            rc = system('/etc/init.d/mediatomb start')
            mybox = self.session.open(MessageBox, _('Mediatomb Server Enabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            self.updateServ()

    def ServStop(self):
        if self.my_serv_active == True:
            rc = system('/etc/init.d/mediatomb stop')
            if fileExists('/etc/rc3.d/S20mediatomb'):
                os_remove('/etc/rc3.d/S20mediatomb')
            mybox = self.session.open(MessageBox, _('Mediatomb Server Disabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle('Info')
            rc = system('sleep 1')
            self.updateServ()

    def updateServ(self):
        self['labrun'].hide()
        self['labstop'].hide()
        rc = system('ps > /tmp/nvpn.tmp')
        self.my_serv_active = False
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('mediatomb') != -1:
                    self.my_serv_active = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if self.my_serv_active == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()


class BhMinidlna(Screen):
    skin = '\n\t<screen position="center,center" size="602,405" title="Black Hole UPnP Minidlna Server Panel">\n\t\t<widget name="lab1" position="20,20" size="580,260" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,300" size="300,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="320,300" size="150,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="320,300" size="150,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="125,360" size="150,30" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="325,360" size="150,30" alphatest="on"/>\n\t\t<widget name="key_red" position="125,362" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t\t<widget name="key_green" position="325,362" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        mytext = _('Minidlna: UPnP media server Black Hole version.\nMinidlna is fully configured for your box and ready to work. Just enable it and play.\nMinidlna include little web interface.\n\nMinidlna webif url: http://ip_box:8200\nMinidlna config: /etc/minidlna.conf\nMinidlna home site: http://sourceforge.net/projects/minidlna/')
        self['lab1'] = Label(mytext)
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Enable'))
        self['key_green'] = Label(_('Disable'))
        self.my_serv_active = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.ServStart,
         'green': self.ServStop})
        self.onLayoutFinish.append(self.updateServ)

    def ServStart(self):
        rc = system('ps > /tmp/nvpn.tmp')
        mediatomb_active = False
        f = open('/tmp/nvpn.tmp', 'r')
        for line in f.readlines():
            if line.find('mediatomb') != -1:
                mediatomb_active = True

        f.close()
        os_remove('/tmp/nvpn.tmp')
        if self.my_serv_active == True:
            self.session.open(MessageBox, _('Minidlna already up and running.'), MessageBox.TYPE_INFO)
        elif mediatomb_active == True:
            self.session.open(MessageBox, _('Sorry you cannot run two UpnP Servers togheter. Please disable Mediatomb before to run minidlna.'), MessageBox.TYPE_INFO)
        else:
            rc = system('ln -s ../init.d/minidlna /etc/rc3.d/S90minidlna')
            rc = system('/etc/init.d/minidlna start')
            mybox = self.session.open(MessageBox, _('Minidlna Server Enabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            self.updateServ()

    def ServStop(self):
        if self.my_serv_active == True:
            rc = system('/etc/init.d/minidlna stop')
            if fileExists('/etc/rc3.d/S90minidlna'):
                os_remove('/etc/rc3.d/S90minidlna')
            mybox = self.session.open(MessageBox, _('Minidlna Server Disabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            rc = system('sleep 1')
            self.updateServ()

    def updateServ(self):
        self['labrun'].hide()
        self['labstop'].hide()
        rc = system('ps > /tmp/nvpn.tmp')
        self.my_serv_active = False
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('minidlna') != -1:
                    self.my_serv_active = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if self.my_serv_active == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()


class BhTunerServer(Screen):
    skin = '\n\t<screen position="center,center" size="800,505" title="Black Hole Tuner Server Panel">\n\t\t<widget name="lab1" position="10,4" size="780,400" font="Regular;20" transparent="1"/>\n\t\t<widget name="lab2" position="20,400" size="300,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="320,400" size="260,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="320,400" size="260,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="95,450" size="140,40" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="330,450" size="140,40" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="565,450" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="95,450" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="transpBlack" transparent="1"/>\n\t\t<widget name="key_green" position="330,450" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="transpBlack" transparent="1"/>\n\t\t<widget name="key_yellow" position="565,450" zPosition="1" size="140,40" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        mytext = _('This feature will allow you to share the tuners of this box with another Dreambox, a PC, a Ps3 and/or a compatible UPnP device in your home network.\n')
        mytext += _('The server will build a virtual channels list in the folder /media/hdd/tuner on this box.\n')
        mytext += _('You can access the tuner(s) of this box from clients on your internal lan using nfs, cifs, UPnP or any other network mountpoint.\n')
        mytext += _('The tuner of the server (this box) has to be avaliable.')
        mytext += _('This means that if you have ony one tuner in your box you can only stream the channel you are viewing (or any channel you choose if your box is in standby).\n')
        mytext += _('Remember to select the correct Audio track in the audio menu if there is no audio or the wrong language is streaming.\n')
        mytext += _('NOTE: The sever is built, based on your current ip and the current channel list of this box. If you change your ip or your channel list is updated, you will need to rebuild the server database.')
        self['lab1'] = Label(mytext)
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Server Disabled'))
        self['labrun'] = Label(_('Server Enabled'))
        self['key_red'] = Label(_('Build Server'))
        self['key_green'] = Label(_('Disable Server'))
        self['key_yellow'] = Label(_('Close'))
        self.my_serv_active = False
        self.ip = '0.0.0.0'
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.ServStart,
         'green': self.ServStop,
         'yellow': self.close})
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.doServStart)
        self.onClose.append(self.delTimer)
        self.onLayoutFinish.append(self.updateServ)

    def ServStart(self):
        self['lab1'].setText(_('Server building in progress\nPlease wait ...'))
        self.activityTimer.start(10)

    def doServStart(self):
        self.activityTimer.stop()
        ret = system('rm -rf /media/hdd/tuner')
        ifaces = iNetwork.getConfiguredAdapters()
        for iface in ifaces:
            ip = iNetwork.getAdapterAttribute(iface, 'ip')
            ipm = '%d.%d.%d.%d' % (ip[0],
             ip[1],
             ip[2],
             ip[3])
            if ipm != '0.0.0.0':
                self.ip = ipm

        ret = system('mkdir /media/hdd/tuner')
        chdir('/media/hdd/tuner')
        s_type = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)'
        serviceHandler = eServiceCenter.getInstance()
        services = serviceHandler.list(eServiceReference('%s FROM BOUQUET "bouquets.tv" ORDER BY bouquet' % s_type))
        bouquets = services and services.getContent('SN', True)
        count = 1
        for bouquet in bouquets:
            self.poPulate(bouquet, count)
            count += 1

        chdir('/home/root')
        mytext = _('Server avaliable on ip ' + self.ip + ' \n\n')
        mytext += _("To access this box's tuners you can connect via lan or UPnP.\n\n")
        mytext += _('1) To connect via lan you have to mount the /media/hdd folder of this box in the client /media/hdd folder. Then you can access the tuners server channel list from the client Media player -> Harddisk -> tuner.\n')
        mytext += _('2) To connect via UPnP you have to start Mediatomb on this box and then start Djmount on the client. Then you can access the tuners server channel list for the client Media Player -> DLNA -> MediaTomb -> playlists.\n\n')
        mytext += _('NOTE about UPnP: Because UPnP requires alot of memory, you should only use it if you need to access your box from a PS3 or other device that cannot be mounted via Lan. Also, After the server has been built we strongly suggest you delete the Bouquets directory that are not really needed BEFORE you start Mediatomb. This will save alot of memory and resources.')
        self['lab1'].setText(mytext)
        self.session.open(MessageBox, _('Build Complete.'), MessageBox.TYPE_INFO)
        self.updateServ()

    def poPulate(self, bouquet, count):
        n = '%03d_' % count
        name = n + self.cleanName(bouquet[1])
        path = '/media/hdd/tuner/' + name
        system('mkdir ' + path)
        serviceHandler = eServiceCenter.getInstance()
        services = serviceHandler.list(eServiceReference(bouquet[0]))
        channels = services and services.getContent('SN', True)
        count2 = 1
        for channel in channels:
            if not int(channel[0].split(':')[1]) & 64:
                n2 = '%03d_' % count2
                filename = path + '/' + n2 + self.cleanName(channel[1]) + '.m3u'
                try:
                    out = open(filename, 'w')
                except:
                    continue

                out.write('#EXTM3U\n')
                out.write('#EXTINF:-1,' + channel[1] + '\n')
                out.write('http://' + self.ip + ':8001/' + channel[0] + '\n\n')
                out.close()
                count2 += 1

    def cleanName(self, name):
        name = name.replace(' ', '_')
        name = name.replace('\xc2\x86', '').replace('\xc2\x87', '')
        name = name.replace('.', '_')
        name = name.replace('<', '')
        name = name.replace('<', '')
        name = name.replace('/', '')
        return name

    def ServStop(self):
        if self.my_serv_active == True:
            ret = system('rm -rf /media/hdd/tuner')
            mybox = self.session.open(MessageBox, _('Tuner Server disabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            rc = system('sleep 1')
            self.updateServ()

    def updateServ(self):
        self['labrun'].hide()
        self['labstop'].hide()
        self.my_serv_active = False
        if isdir('/media/hdd/tuner'):
            self.my_serv_active = True
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()

    def delTimer(self):
        del self.activityTimer


class BhNetBrowser(Screen):
    skin = '\n\t<screen position="center,center" size="800,520" title="Select Network Interface">\n\t\t<widget source="list" render="Listbox" position="10,10" size="780,460" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n    \t\t<ePixmap pixmap="skin_default/buttons/red.png" position="200,480" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,480" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="200,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_yellow" position="440,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n    \t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Select'))
        self['key_yellow'] = Label(_('Close'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.selectInte,
         'back': self.close,
         'red': self.selectInte,
         'yellow': self.close})
        self.list = []
        self.adapters = [ (iNetwork.getFriendlyAdapterName(x), x) for x in iNetwork.getAdapterList() ]
        for x in self.adapters:
            res = (x[0], x[1])
            self.list.append(res)

        self['list'].list = self.list

    def selectInte(self):
        mysel = self['list'].getCurrent()
        if mysel:
            inter = mysel[1]
            self.session.open(NetworkBrowser, inter, '/usr/lib/enigma2/python/Plugins/SystemPlugins/NetworkBrowser')


class BhPcsc(Screen):
    skin = '\n\t<screen position="center,center" size="602,305" title="Black Hole Pcsc Panel">\n\t\t<widget name="lab1" position="20,30" size="580,60" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="lab2" position="20,150" size="300,30" font="Regular;20" valign="center" transparent="1"/>\n\t\t<widget name="labstop" position="320,150" size="150,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>\n\t\t<widget name="labrun" position="320,150" size="150,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="125,260" size="150,30" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="325,260" size="150,30" alphatest="on"/>\n\t\t<widget name="key_red" position="125,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t\t<widget name="key_green" position="325,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Pcsc service for Usb readers.'))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self['key_red'] = Label(_('Enable'))
        self['key_green'] = Label(_('Disable'))
        self.my_serv_active = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.ServStart,
         'green': self.ServStop})
        self.onLayoutFinish.append(self.updateServ)

    def ServStart(self):
        if self.my_serv_active == False:
            rc = system('ln -s ../init.d/pcscd /etc/rc3.d/S20pcscd')
            rc = system('/etc/init.d/pcscd start')
            mybox = self.session.open(MessageBox, _('Pcsc Enabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            self.updateServ()

    def ServStop(self):
        if self.my_serv_active == True:
            rc = system('/etc/init.d/pcscd stop')
            if fileExists('/etc/rc3.d/S20pcscd'):
                os_remove('/etc/rc3.d/S20pcscd')
            mybox = self.session.open(MessageBox, _('Pcsc Client Disabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            rc = system('sleep 1')
            self.updateServ()

    def updateServ(self):
        self['labrun'].hide()
        self['labstop'].hide()
        rc = system('ps > /tmp/nvpn.tmp')
        self.my_serv_active = False
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('pcscd') != -1:
                    self.my_serv_active = True

            f.close()
            os_remove('/tmp/nvpn.tmp')
        if self.my_serv_active == True:
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()
