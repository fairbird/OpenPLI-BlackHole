from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Label import Label
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_PLUGIN, resolveFilename
from os import path as os_path, statvfs as os_statvfs, system as os_system, remove as os_remove
from enigma import eConsoleAppContainer, getDesktop
from multInstaller import TSGetMultiipk
tslang_changed = '/tmp/.newlang'
opkg_ready_filename = '/tmp/.opkg_ready'
opkg_list_filename = '/tmp/.opkglist'

def getdistrofeed():
    path = '/etc/opkg/all-feed.conf'
    distro = ''
    if os_path.exists(path):
        f = open(path, 'r')
        distro_all = f.readline()
        s = distro_all.split(' ')
        distro = s[2].strip()
        f.close()
    return distro[:-3]


distro_feed = getdistrofeed()
desktopSize = getDesktop(0).size()

def getipkinfos(ipkfile):
    try:
        ipkfile = str(os_path.basename(ipkfile))
        opkgpath = '/var/lib/opkg/info/'
        ipkparts = []
        ipkparts = ipkfile.split('_')
        ipkname = str(ipkparts[0]).strip()
        ipkversion = str(ipkparts[1]).strip()
        ipkfilename = opkgpath + ipkname + '.control'
        s = ipkfile.split('_')
        arch = 'all'
        package = 'Package: %s' % s[0]
        version = 'Version: %s' % ipkversion
        desciption = 'Description: N/A'
        depends = 'Depends: N/A'
        status = 'install'
        metadata = False
        prev = 'N/A'
        if fileExists(ipkfilename):
            f = open(ipkfilename, 'r')
            line = 'dummy'
            while line:
                line = f.readline()
                if line.startswith('Package:'):
                    s = line.split('_')
                    package = s[0]
                if line.startswith('Architecture:'):
                    arch = line.replace('Architecture: ', '')
                if line.startswith('Version:'):
                    version = line
                    ver = getdigitversion(version)
                    ipkversion = getdigitversion(ipkversion)
                    if float(ver) == float(ipkversion):
                        status = 'remove'
                    elif float(ver) > float(ipkversion):
                        status = 'remove'
                    elif float(ver) < float(ipkversion):
                        status = 'update'
                if line.startswith('Description:'):
                    if line.startswith('Description: Additional plugins for Enigma2'):
                        desciption = 'Description: %s' % f.readline().strip()
                    else:
                        desciption = line
                    print '[description] %s' % desciption
                if line.startswith('Depends:'):
                    depends = line

            f.close()
    except:
        s = ipkfile.split('_')
        arch = 'all'
        package = 'Package: %s' % s[0]
        version = 'Version: N/A'
        desciption = 'Description: N/A'
        depends = 'Depends: N/A'
        status = 'install'
        metadata = False
        prev = 'N/A'

    return (arch,
     package.strip(),
     version.strip(),
     desciption.strip(),
     depends.strip(),
     status,
     metadata,
     prev)


def getipkversion(ipkfile):
    try:
        print ipkfile
        opkgpath = '/var/lib/opkg/info/'
        ipkfilename = opkgpath + ipkfile + '.control'
        print ipkfilename
        if fileExists(ipkfilename):
            return 'remove'
        return 'install'
    except:
        return 'install'


def getdigitversion(ipkversionstr):
    tstr = ''
    e = list(ipkversionstr)
    for j in e:
        if j.isdigit():
            tstr = tstr + str(j)

    return tstr


def freespace():
    try:
        diskSpace = os_statvfs('/')
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
        return spacestr
    except:
        return ''


class TSilangGroups(Screen):
    skin_1280 = '\n                <screen  name="TSilangGroups" position="center,77" size="920,600" title=""  >\n\t\t<widget source="list" render="Listbox" position="20,15" size="880,416" scrollbarMode="showOnDemand" transparent="1" zPosition="1" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryPixmapAlphaBlend(pos = (5, 7), size = (18, 18), png = 1), # Status Icon,\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (35, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 23)],\n\t\t\t\t\t"itemHeight": 32\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                </widget>                \t                   \n                <widget name="info" position="20,0" zPosition="1" size="880,550" font="Regular;22" backgroundColor="background" transparent="1" halign="center" valign="center" />\n\t\t<eLabel position="20,470" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t<widget name="fspace" position="20,460" zPosition="4" size="880,80" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n\t\t<eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n        \t</screen>'
    skin_1920 = '    <screen name="TSilangGroups" position="center,200" size="1300,720" title="Addons Manager">\n        <widget name="info" position="20,550" size="1260,40" foregroundColor="yellow" backgroundColor="background" font="Regular;26" valign="center" halign="center" transparent="1" zPosition="1" />\n        <eLabel position="10,590" zPosition="4" size="1280,1" backgroundColor="foreground" />\n        <widget name="fspace" position="40,600" size="300,120" foregroundColor="foreground" backgroundColor="background" font="Regular;26" valign="top" halign="left" transparent="1" zPosition="1" />\n        <widget source="list" render="Listbox" position="20,20" size="1260,520" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (7, 7), size = (26, 26), png = 1),\n        ],\n        "fonts": [gFont("Regular", 30)],\n        "itemHeight": 40\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        self.skin = TSilangGroups.skin
        Screen.__init__(self, session)
        self.greenStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/share/enigma2/skin_default/buttons/green.png'))
        self.yellowStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/share/enigma2/skin_default/buttons/blue.png'))
        self.greyStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/share/enigma2/skin_default/buttons/grey.png'))
        self.list = []
        self['list'] = List([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self.ipkList = []
        self.downloading = False
        self['info'].setText('Getting language packs, please wait..')
        self.downloadxmlpage()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close}, -2)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle('Language download')

    def getfreespace(self):
        fspace = freespace()
        self.freespace = fspace
        self['fspace'].setText(self.freespace)

    def okClicked(self):
        idx = self['list'].getIndex()
        if self.ipkList[idx][1] != self.greenStatus:
            pluginname = self.ipkList[idx][0]
            urlserver = self.ipkList[idx][4]
            self.session.openWithCallback(self.updateInstall, TSGetMultiipk, [pluginname], [], [urlserver], [], '', False, True)

    def downloadxmlpage(self, result = True):
        if os_path.exists(opkg_ready_filename):
           if not os_path.exists(opkg_list_filename):
              print '[update opkg list filename] start'
              cmd = "opkg list | grep -E 'enigma2-language-' > " + opkg_list_filename
              os_system(cmd)
        if not os_path.exists(opkg_ready_filename):
           print '[opkg update] start'
           cmd = 'touch %s ; opkg update' % opkg_ready_filename
           os_system(cmd)
           self['info'].setText('Please wait while language pack is being downloaded...')
           self.container = eConsoleAppContainer()
           self.container.appClosed.append(self.downloadxmlpage)
           self.container.execute(cmd)
        else:
            self.opkglist_filename = '/tmp/.tmplist'
            cmd = "cat /tmp/.opkglist | grep 'enigma2-language-' > /tmp/.tmplist"
            os_system(cmd)
            self._gotPageLoad()

    def errorLoad(self, error):
        print str(error)
        self['info'].setText('Addons Download Failure,No internet connection or server down !')

    def _gotPageLoad(self):
        count = 0
        self.ipkList = []
        fm = open(self.opkglist_filename)
        line = 'dummy'
        sp = []
        while line:
            line = fm.readline()
            if line.startswith('enigma2-language-'):
                sp = line.split(' ')
                arch = 'all'
                url = distro_feed + arch + '/'
                fullname = url + sp[0] + '_' + sp[2] + '_' + arch + '.ipk'
                version = sp[2]
                arch, pkg, ver, desc, dep, processmode, metadata, prev = getipkinfos(sp[0] + '_' + version)
                if count > 0:
                    if pkg == self.ipkList[count - 1][3]:
                        processmode = 'spring'
                item = sp[0]
                if processmode == 'install':
                    count = count + 1
                    self.ipkList.append((item,
                     self.greyStatus,
                     processmode,
                     pkg,
                     fullname))
                elif processmode == 'update':
                    count = count + 1
                    self.ipkList.append((item,
                     self.yellowStatus,
                     processmode,
                     pkg,
                     fullname))
                elif processmode == 'remove':
                    count = count + 1
                    self.ipkList.append((item,
                     self.greenStatus,
                     processmode,
                     pkg,
                     fullname))

        fm.close()
        self.ipkList.sort()
        self['info'].setText('')
        self['list'].setList(self.ipkList)
        self.getfreespace()

    def updateInstall(self, status):
        print '[Language downloader] status: %s' % status
        if os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
        cmd = 'touch ' + tslang_changed
        os_system(cmd)
        idx = self['list'].getIndex()
        item = self.ipkList[idx][0]
        self.ipkList[idx] = (item, self.greenStatus)
        self['list'].updateList(self.ipkList)
        self.getfreespace()

    def updateRemove(self, status):
        print '[Language downloader] status: %s' % status
        idx = self['list'].getIndex()
        item = self.ipkList[idx][0]
        print '[item= %s]' % item
        self.ipkList[idx] = (item, self.greyStatus)
        self['list'].updateList(self.ipkList)
        self.getfreespace()
