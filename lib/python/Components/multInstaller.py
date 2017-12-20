from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from enigma import eConsoleAppContainer, getDesktop
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.config import config
from Downloader import downloadWithProgress
from os import system as os_system, path as os_path, remove as os_remove, popen as os_popen
opkg_busy_filename = '/tmp/.opkg_busy'
desktopSize = getDesktop(0).size()

class TSGetMultiipk(Screen):
    skin_1280 = '\n\t        <screen name="TSGetMultiipk" position="center,center" size="550,115" title="Installing Softcam...">\n\t\t<widget name="activityslider" position="20,50" size="510,20" borderWidth="1" transparent="1" />\n\t\t<widget name="package" position="20,5" size="510,35" font="Regular;18" foregroundColor="foreground" backgroundColor="background" halign="center" valign="center" transparent="1" />\n\t\t<widget name="status" position="20,78" size="510,40" font="Regular;16" foregroundColor="foreground" backgroundColor="background" halign="center" valign="center" transparent="1" />\n\t        </screen>'
    skin_1920 = '    <screen name="TSGetMultiipk" position="center,center" size="860,180" title="Installer">\n        <widget name="activityslider" position="30,65" size="800,30" borderWidth="1" transparent="1" />\n        <widget name="package" position="30,5" size="800,60" font="Regular;26" foregroundColor="foreground" backgroundColor="background" halign="center" valign="center" transparent="1" />\n        <widget name="status" position="30,100" size="800,80" font="Regular;23" foregroundColor="foreground" backgroundColor="background" halign="center" valign="center" transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, installNameList = [], removeNameList = [], installList = [], removeList = [], closetext = '', restart = False, autoclose = False):
        Screen.__init__(self, session)
        self.session = session
        self.installNameList = installNameList
        self.removeNameList = removeNameList
        self.installList = installList
        self.removeList = removeList
        self.autoclose = autoclose
        self.closetext = closetext
        self.restart = restart
        self.count_success = 0
        self.count_failed_remove = 0
        self.count_failed_install = 0
        self.count_removed = 0
        self.errormessage = ''
        self.cache = None
        self.downloader = None
        self.container = eConsoleAppContainer()
        self['activityslider'] = ProgressBar()
        self['activityslider'].setRange((0, 100))
        self['activityslider'].setValue(0)
        self['status'] = Label()
        self['package'] = Label()
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.okClicked,
         'cancel': self.abort}, -1)
        self['status'].setText(_('Waiting to get resouces free...'))
        self.setTitle(_('Connecting') + '...')
        if os_path.exists(opkg_busy_filename):
            self.onCheckClose()
        else:
            self.onLayoutFinish.append(self.startDownload)

    def onCheckClose(self, result = True):
        if os_path.exists(opkg_busy_filename):
            cmd = 'echo\n'
            print '[multInstaller] resources busy...'
            self.container = eConsoleAppContainer()
            self.container.appClosed.append(self.onCheckClose)
            self.container.execute(cmd)
        else:
            self.startDownload()

    def startDownload(self):
        self.currentIndex = 0
        self.count_success = 0
        self.count_failed_remove = 0
        self.count_failed_install = 0
        self.tryNextPackage()

    def getFileType(self, filename):
        fileextension = ''
        print '[TS multInstaller] Installing package with type %s' % fileextension
        if filename.endswith('.tar.bz2') or filename.endswith('.tbz2') or filename.endswith('.tbz'):
            fileextension = '.tar.bz2'
        elif filename.endswith('.tbz'):
            fileextension = '.tbz'
        elif filename.endswith('.tbz2'):
            fileextension = '.tbz2'
        elif filename.endswith('.tar.gz'):
            fileextension = '.tar.gz'
        elif filename.endswith('.tgz'):
            fileextension = '.tgz'
        elif filename.endswith('.ipk'):
            fileextension = '.ipk'
        elif filename.endswith('.zip'):
            fileextension = '.zip'
        return fileextension

    def progress(self, current, total):
        p = int(100 * (float(current) / float(total)))
        self['activityslider'].setValue(p)
        info = _('Downloading') + ' ' + '%d of %d kBytes' % (current / 1024, total / 1024)
        self.setTitle(_('Downloading') + ' ' + str(p) + '%...')
        self['status'].setText(_('Downloading') + '...')

    def responseCompleted(self, data = None):
        print '[TS multInstaller] Download succeeded. '
        self['status'].setText('Installing to root...')
        self.setTitle(_('Installing') + '...')
        self.installpackage(self.target)

    def exit(self):
        self.close(False)

    def responseFailed(self, failure_instance = None, error_message = ''):
        print '[TS multInstaller] Download failed --> %s' % error_message
        self.error_message = error_message
        if error_message == '' and failure_instance is not None:
            self.error_message = failure_instance.getErrorMessage()
        self['status'].setText(self.error_message)
        cmd = "echo '%s' >> /tmp/ipkinstall.log" % self.error_message
        os_system(cmd)
        self.setTitle(_('Download failed'))
        if os_path.exists(self.target):
            os_remove(self.target)
        self.count_failed_install = self.count_failed_install + 1
        self.currentIndex = self.currentIndex + 1
        self.tryNextPackage()

    def abort(self):
        if self.downloader is not None:
            self.downloader.stop
            self['status'].setText(_('Aborting...'))
            if os_path.exists(self.target):
                os_remove(self.target)
            if os_path.exists('/tmp/ipkinstall.log'):
                os_remove('/tmp/ipkinstall.log')
            self.close(False)
        elif self['package'].getText() == _('Terminate'):
            if os_path.exists('/tmp/ipkinstall.log'):
                os_remove('/tmp/ipkinstall.log')
            self.close(False)

    def AbortOnClose(self, result):
        print result
        self.close(False)

    def installpackage(self, filename):
        print '[TS multInstaller] Installing package. '
        if self.fileextension == '.tar.bz2' or self.fileextension == '.tbz2' or self.fileextension == '.tbz':
            self.deflatebz(filename)
        elif self.fileextension == '.tar.gz' or self.fileextension == '.tgz':
            self.destination = self.installNameList[self.currentIndex]
            print '[TS multInstaller] tar.gz destination: %s' % self.destination
            self.deflateTar(filename)
        elif self.fileextension == '.ipk':
            self.deflateIpk(filename)
        elif self.fileextension == '.zip':
            self.deflatezip(filename)
        else:
            return False
        return True

    def deflatebz(self, filename):
        destination = '/'
        os_system('tar -xjvf ' + filename + ' -C ' + destination)

    def deflatezip(self, filename):
        destination = '/'
        os_system('unzip -o ' + filename + ' -d ' + destination)

    def deflateTar(self, filename):
        self.container = eConsoleAppContainer()
        self.destination = '/'
        cmd = "echo 'Configuring %s...' >> /tmp/ipkinstall.log" % filename[5:].replace('.tar.gz', '')
        cmd = cmd + '; tar zxf ' + filename + ' -C ' + self.destination + '  >> /tmp/ipkinstall.log'
        print '[multiInstaller] defalteTar --> cmd = %s' % cmd
        self.container.execute(cmd)
        self.container.appClosed.append(self.deflateOnClosed)
        self.container.dataAvail.append(self.cmdData)
        self['status'].setText(_('Installing to root...'))

    def deflateIpk(self, filename):
        cmd = 'opkg install %s' % self.target
        #cmd = 'opkg install -force-overwrite ' + self.webfile
        print '[multiInstaller] defalteIpk --> cmd = %s' % cmd
        self.container.appClosed.append(self.deflateOnClosed)
        self.container.dataAvail.append(self.cmdData)
        if self.container.execute(cmd):
            self.deflateOnClosed(-1)

    def cmdData(self, data):
        if self.cache is None:
            self.cache = data
        else:
            self.cache += data
        if '\n' in data:
            splitcache = self.cache.split('\n')
            if self.cache[-1] == '\n':
                iteration = splitcache
                self.cache = None
            else:
                iteration = splitcache[:-1]
                self.cache = splitcache[-1]
            for mydata in iteration:
                if mydata != '':
                    cmd = "echo '%s' >> /tmp/ipkinstall.log" % mydata
                    os_system(cmd)
                    if mydata.find('Downloading') == 0:
                        pkg = mydata.split(' ', 5)[1].strip()
                        pkgname = str(os_path.basename(pkg))
                        self.currentpkgname = pkgname.split('_')[0]
                        self['package'].setText(self.currentpkgname)
                        self['status'].setText(_('Downloading') + '...')
                        self.count_success = self.count_success + 1
                    elif mydata.find('Upgrading') == 0:
                        self.currentpkgname = mydata.split(' ', 8)[1].strip()
                        pkgfrom = mydata.split(' ', 8)[5].strip()
                        pkgto = mydata.split(' ', 8)[7].strip()
                        self['package'].setText(self.currentpkgname)
                        self['status'].setText(_('Upgrading from %s to %s') % (pkgfrom, pkgto))
                    elif mydata.find('Installing') == 0:
                        self.currentpkgname = mydata.split(' ', 5)[1].strip()
                        self['package'].setText(self.currentpkgname)
                        self['status'].setText(_('Installing to root...'))
                    elif mydata.find('Removing') == 0:
                        self.currentpkgname = mydata.split(' ', 5)[1].strip()
                        self['package'].setText(self.currentpkgname)
                        self['status'].setText(_('Removing from root...'))
                    elif mydata.find('Configuring') == 0:
                        self.currentpkgname = mydata.split(' ', 2)[1].strip()
                        self['status'].setText('Configuring...')
                    elif mydata.find('No packages removed') == 0:
                        self['status'].setText(mydata)
                        self.errormessage = mydata
                    elif mydata.find('Collected errors:') == 0:
                        self['status'].setText(_('Cannot install package'))
                        self.errormessage = mydata
                    elif mydata.find('An error occurred') == 0:
                        self['status'].setText(_('An error occurred'))
                        self.errormessage = mydata
                    elif mydata.find('Failed to download') == 0:
                        self['status'].setText(_('Failed to download'))
                        self.errormessage = mydata
                    elif mydata.find('opkg_download:') == 0:
                        self['status'].setText(_('opkg_download: ERROR'))
                        self.errormessage = mydata
                    elif mydata.find("    Configuration file '") >= 0:
                        self['package'].setText(mydata.split(" '", 1)[1][:-1])
                        self['status'].setText(mydata.replace('    ', ''))

    def deflateOnClosed(self, retval):
        self.container.appClosed.remove(self.deflateOnClosed)
        self.container.dataAvail.remove(self.cmdData)
        if os_path.exists(self.target):
            os_remove(self.target)
        if self.errormessage == '':
            self.count_success = self.count_success + 1
            if self.currentpkgname.startswith('enigma2-skin-'):
                if not os_path.exists('/tmp/.newskin'):
                    cmd = 'touch /tmp/.newskin'
                    os_system(cmd)
            elif not os_path.exists('/tmp/.restart_e2'):
                cmd = 'touch /tmp/.restart_e2'
                os_system(cmd)
        else:
            self.count_failed_install = self.count_failed_install + 1
        self.currentIndex = self.currentIndex + 1
        self.tryNextPackage()

    def tryNextPackage(self):
        if self.currentIndex < len(self.installList):
            self.fileextension = self.getFileType(self.installList[self.currentIndex])
            pkgname = str(os_path.basename(self.installList[self.currentIndex]))
            self.currentpkgname = pkgname.split('_')[0]
            self['package'].setText(self.currentpkgname)
            self.setTitle(_('Connecting') + '...')
            self['status'].setText(_('Connecting to server....'))
            self.target = '/tmp/' + self.installNameList[self.currentIndex] + self.fileextension
            print '[TS multInstaller] Downloading %s to %s' % (self.installList[self.currentIndex], self.target)
            self.webfile = self.installList[self.currentIndex].strip()
            self.downloader = downloadWithProgress(self.webfile, self.target)
            self.downloader.addProgress(self.progress)
            self.downloader.start().addCallback(self.responseCompleted).addErrback(self.responseFailed)
        elif len(self.removeList) > 0:
            self.currentIndex = 0
            self.removeIpk()
        else:
            if not len(self.removeList) == 0:
                self.setTitle(_('Install') + ' & ' + _('Remove'))
            else:
                self.setTitle(_('Install'))
            if not self.autoclose:
                self['package'].setText(_('Terminate'))
                self['status'].setText(_('%d package(s) installed, %d package(s) removed, %d package(s) failed,\n press ok to see log or cancel to exit.') % (self.count_success, self.count_removed, self.count_failed_install + self.count_failed_remove))
            else:
                if os_path.exists('/tmp/ipkinstall.log'):
                    os_remove('/tmp/ipkinstall.log')
                self.close(False)

    def removeIpk(self):
        self['activityslider'].setValue(100)
        self.setTitle(_('Removing') + '...')
        self['status'].setText(_('Removing from root...'))
        pkgname = str(os_path.basename(self.removeList[self.currentIndex]))
        self.currentpkgname = str(pkgname.split('_')[0]).strip()
        self['package'].setText(self.currentpkgname)
        if pkgname[-7:] == '.tar.gz':
            cmd = 'ls /usr/uninstall | grep Del_%s' % self.currentpkgname
            print '[TS multiInstaller] tar cmd grep --> cmd = %s' % cmd
            script = self.getCmdOutput(cmd)
            script = script.strip()
            cmd = "echo 'Removing %s...' >> /tmp/ipkinstall.log" % ipkbasefile
            cmd = cmd + '; sh /usr/uninstall/%s %s' % (script, ' >> /tmp/ipkinstall.log')
            cmd = cmd + '; rm /usr/uninstall/%s' % script
        else:
            cmd = 'opkg remove  %s' % self.currentpkgname
        print '[TS multInstaller] removeIpk --> cmd = %s' % cmd
        self.container.appClosed.append(self.removeCmdOnclose)
        self.container.dataAvail.append(self.cmdData)
        if self.container.execute(cmd):
            self.removeCmdOnclose(-1)

    def removeCmdOnclose(self, reval):
        self.container.appClosed.remove(self.removeCmdOnclose)
        self.container.dataAvail.remove(self.cmdData)
        if self.errormessage == '':
            self.count_removed = self.count_removed + 1
            if not os_path.exists('/tmp/.restart_e2') and not self.currentpkgname.startswith('enigma2-skin-'):
                cmd = 'touch /tmp/.restart_e2'
                os_system(cmd)
        else:
            self.errormessage = ''
            self.count_failed_remove = self.count_failed_remove + 1
        self.currentIndex = self.currentIndex + 1
        if self.currentIndex < len(self.removeList):
            pkgname = str(os_path.basename(self.removeList[self.currentIndex]))
            self.currentpkgname = pkgname.split('_')[0]
            self['package'].setText(self.currentpkgname)
            self.setTitle(_('Removing') + '...')
            self['status'].setText(_('Removing from root...'))
            self.removeIpk()
        else:
            if not len(self.installList) == 0:
                self.setTitle(_('Install') + ' & ' + _('Remove'))
            else:
                self.setTitle(_('Remove'))
            self['package'].setText(_('Terminate'))
            self['status'].setText(_('%d package(s) installed, %d package(s) removed, %d package(s) failed,\n press ok to see log or cancel to exit.') % (self.count_success, self.count_removed, self.count_failed_remove + self.count_failed_install))

    def okClicked(self):
        if self['package'].getText() == _('Terminate'):
            if os_path.exists('/tmp/ipkinstall.log'):
                cmd = 'cat /tmp/ipkinstall.log'
                title = _('Installer Log')
                self.session.openWithCallback(self.callbackLog, TSConsole, cmd, title)

    def callbackLog(self):
        if os_path.exists('/tmp/ipkinstall.log'):
            os_remove('/tmp/ipkinstall.log')
        if self.count_failed_install + self.count_failed_remove == 0:
            self.close(True)
        else:
            self.close(False)

    def getCmdOutput(self, cmd):
        pipe = os_popen('{ ' + cmd + '; } 2>&1', 'r')
        text = pipe.read()
        pipe.close()
        if text[-1:] == '\n':
            text = text[:-1]
        return text


class TSConsole(Screen):
    skin_1280 = '        \t\n                <screen name="TSConsole" position="center,77" size="920,600" title=""  >\n                <widget name="waiting" position="20,15" zPosition="4" size="880,550" font="Regular;22" transparent="1" halign="center" valign="center" />\t                \n\t\t<widget name="text" position="30,10" size="870,550" font="Regular;20"  transparent="1" zPosition="2"  />\n                </screen>'
    skin_1920 = '    <screen name="TSConsole" position="center,200" size="1300,720" title="TS Console">\n        <widget name="waiting" position="20,15" zPosition="4" size="1260,600" font="Regular;32" transparent="1" halign="center" valign="center" />\n        <widget name="text" position="20,30" size="1260,600" zPosition="2" font="Regular;28" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, cmd, title, info = ''):
        Screen.__init__(self, session)
        self.cmd = cmd
        self.info = info
        self.title = title
        self.text = ''
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions', 'ColorActions'], {'ok': self.close,
         'cancel': self.close,
         'red': self.close,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown,
         'left': self['text'].pageUp,
         'right': self['text'].pageDown}, -1)
        self['waiting'] = Label(info)
        self.onLayoutFinish.append(self.getIpkInfo)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle(self.title)

    def getIpkInfo(self):
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.onGetIpkClose)
        self.container.dataAvail.append(self.cmdData)
        self.container.execute(self.cmd)

    def cmdData(self, data):
        if data:
            self.text = self.text + data
            if self.info == '':
                self['text'].setText(self.text.strip())

    def onGetIpkClose(self, status):
        self.container.appClosed.remove(self.onGetIpkClose)
        self.container.dataAvail.remove(self.cmdData)
        self['waiting'].setText('')
        self['text'].setText(self.text.strip())
