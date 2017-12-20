from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Tools.Directories import resolveFilename, removeDir, SCOPE_CURRENT_SKIN
from Components.Sources.List import List
from Components.Label import Label
from Components.Pixmap import Pixmap
from Tools.LoadPixmap import LoadPixmap
from Screens.MessageBox import MessageBox
from enigma import eConsoleAppContainer, getDesktop
from os import path as os_path, remove as os_remove, listdir as os_listdir
import download
desktopSize = getDesktop(0).size()

class TSilangScreen(Screen):
    skin_1280 = '\n                        <screen name="TSilangScreen"  position="center,77"  title="Language Manager" size="920,600"  >\n                        <widget source="menu" render="Listbox"  position="20,20" size="880,450" scrollbarMode="showOnDemand" zPosition="2" transparent="1"  >\n\t\t\t    <convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t            MultiContentEntryText(pos = (150, 10), size = (490, 30), flags = RT_HALIGN_LEFT, text = 0), # index 1 is the language name,\n\t\t\t\t\t    MultiContentEntryPixmapAlphaBlend(pos = (800, 12), size = (26, 26), png = 3), # index 2 is the pixmap selection\n\t\t\t\t            MultiContentEntryPixmapAlphaBlend(pos = (30, 5), size = (60, 40), png = 2) # index 3 is the pixmap flags\n\t\t\t\t\t],\n\t\t\t\t "fonts": [gFont("Regular", 25)],\n\t\t\t\t "itemHeight": 50\n\t\t\t\t}\n\t\t\t    </convert>\n\t\t        </widget>\n                        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />        \t\n                       \t<eLabel name="ButtonRedtext" text="Close" position="70,548" size="140,44" valign="center" halign="center" zPosition="2"  font="Regular;20" transparent="1" /> \n                        <widget name="ButtonYellowtext" position="490,548" size="140,44" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n                       \t<widget name="ButtonGreentext" position="280,548" size="140,44" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" /> \n                        <widget name="ButtonBluetext" position="700,548" size="140,44" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n\t\t\t<ePixmap name="red" pixmap="/usr/share/enigma2/skin_default/buttons/key_red.png" position="70,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<widget name="ButtonGreen" pixmap="/usr/share/enigma2/skin_default/buttons/key_green.png" position="280,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<widget name="ButtonYellow" pixmap="/usr/share/enigma2/skin_default/buttons/key_yellow.png" position="490,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\t\t\t\t\t\t\n       \t                <widget name="ButtonBlue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/share/enigma2/skin_default/buttons/key_blue.png" transparent="1" alphatest="blend" /> \t                  \n        \t</screen>\n\t\t'
    skin_1920 = '    <screen name="TSilangScreen" position="center,200" size="1300,720" title="Addons Manager">\n        <ePixmap pixmap="/usr/share/enigma2/skin_default/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/share/enigma2/skin_default/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/share/enigma2/skin_default/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/share/enigma2/skin_default/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <widget name="ButtonRedtext" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="ButtonGreentext" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="ButtonYellowtext" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget name="ButtonBluetext" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n        <widget source="menu" render="Listbox" position="20,20" size="1260,600" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (80, 0), size = (1000, 60), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (5, 10), size = (60, 40), png = 2),\n        MultiContentEntryPixmapAlphaBlend(pos = (1190, 17), size = (26, 26), png = 3),\n        ],\n        "fonts": [gFont("Regular", 30)],\n        "itemHeight": 60\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        list = []
        self.langs = []
        self.menuList = []
        self.removing = False
        self.select_all = True
        self['menu'] = List(self.menuList)
        self['ButtonYellow'] = Pixmap()
        self['ButtonYellowtext'] = Label(_('Select all'))
        self['ButtonBlue'] = Pixmap()
        self['ButtonBluetext'] = Label(_('Remove'))
        self['ButtonGreen'] = Pixmap()
        self['ButtonGreentext'] = Label(_('Add'))
        self['ButtonRedtext'] = Label(_('Close'))
        self.removeIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/share/enigma2/skin_default/buttons/remove.png'))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'blue': self.removeLang,
         'yellow': self.selectDeselectAll,
         'green': self.langdownload,
         'red': self.close,
         'ok': self.changeSelection,
         'cancel': self.close}, -2)
        self.removelist = []
        self.languagaes()
        self.createMenu()
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle('Language Manager')

    def languagaes(self):
        self.langs.append([_('English'), 'en', 'EN'])
        self.langs.append([_('Chinese'), 'zh', 'CN'])
        self.langs.append([_('Chineseh'), 'hk', 'HK'])
        self.langs.append([_('Bulgarian'), 'bg', 'BG'])
        self.langs.append([_('German'), 'de', 'DE'])
        self.langs.append([_('Arabic'), 'ar', 'AE'])
        self.langs.append([_('Catalan'), 'ca', 'AD'])
        self.langs.append([_('Croatian'), 'hr', 'HR'])
        self.langs.append([_('Czech'), 'cs', 'CZ'])
        self.langs.append([_('Danish'), 'da', 'DK'])
        self.langs.append([_('Dutch'), 'nl', 'NL'])
        self.langs.append([_('Estonian'), 'et', 'EE'])
        self.langs.append([_('Finnish'), 'fi', 'FI'])
        self.langs.append([_('French'), 'fr', 'FR'])
        self.langs.append([_('Greek'), 'el', 'GR'])
        self.langs.append([_('Hungarian'), 'hu', 'HU'])
        self.langs.append([_('Lithuanian'), 'lt', 'LT'])
        self.langs.append([_('Latvian'), 'lv', 'LV'])
        self.langs.append([_('Icelandic'), 'is', 'IS'])
        self.langs.append([_('Italian'), 'it', 'IT'])
        self.langs.append([_('Norwegian'), 'no', 'NO'])
        self.langs.append([_('Persian'), 'fa', 'IR'])
        self.langs.append([_('Polish'), 'pl', 'PL'])
        self.langs.append([_('Portuguese'), 'pt', 'PT'])
        self.langs.append([_('Brazilian'), 'pt_BR', 'BR'])
        self.langs.append([_('Russian'), 'ru', 'RU'])
        self.langs.append([_('Serbian'), 'sr', 'YU'])
        self.langs.append([_('Slovakian'), 'sk', 'SK'])
        self.langs.append([_('Slovenian'), 'sl', 'SI'])
        self.langs.append([_('Spanish'), 'es', 'ES'])
        self.langs.append([_('Swedish'), 'sv', 'SE'])
        self.langs.append([_('Turkish'), 'tr', 'TR'])
        self.langs.append([_('Ukrainian'), 'uk', 'UA'])
        self.langs.append([_('Frisian'), 'fy', 'x-FY'])

    def getsecondkey(self, name):
        for item in self.langs:
            if name == item[1]:
                print name
                print item
                secondkey = item[2]
                secondkey = secondkey.lower()
                return secondkey

        return 'missing'

    def getlan(Self, key):
        lan = {'bg': 'Bulgarian',
         'hk': 'Chineseh',
         'zh': 'Chinese',
         'fa': 'Persian',
         'en': 'English',
         'de': 'German',
         'ar': 'Arabic',
         'ca': 'Catalan',
         'hr': 'Croatian',
         'cs': 'Czech',
         'da': 'Danish',
         'nl': 'Dutch',
         'et': 'Estonian',
         'fi': 'Finnish',
         'fr': 'French',
         'el': 'Greek',
         'hu': 'Hungarian',
         'lt': 'Lithuanian',
         'lv': 'Latvian',
         'is': 'Icelandic',
         'it': 'Italian',
         'no': 'Norwegian',
         'pl': 'Polish',
         'pt': 'Portuguese',
         'pt_BR': 'Brazilian',
         'ru': 'Russian',
         'sr': 'Serbian',
         'sk': 'Slovakian',
         'sl': 'Slovenian',
         'es': 'Spanish',
         'sv': 'Swedish',
         'tr': 'Turkish',
         'uk': 'Ukrainian',
         'fy': 'Frisian'}
        try:
            return lan[key]
        except:
            return 'Unkown'

    def langdownload(self):
        self.removelist = []
        self.session.openWithCallback(self.createMenu, download.TSilangGroups)

    def selectDeselectAll(self):
        if self.select_all:
            self.selectall()
        else:
            self.deselectall()

    def selectall(self):
        self.removelist = []
        for idx in range(len(self.menuList)):
            if self.menuList[idx][3] == None:
                self.menuList[idx] = (self.menuList[idx][0],
                 self.menuList[idx][1],
                 self.menuList[idx][2],
                 self.removeIcon)
                self.removelist.append(self.menuList[idx][1])

        self['ButtonBluetext'].show()
        self['ButtonYellowtext'].setText(_('Deselect all'))
        self.select_all = False
        self['menu'].updateList(self.menuList)

    def deselectall(self):
        self.removelist = []
        for idx in range(len(self.menuList)):
            if not self.menuList[idx][3] == None:
                self.menuList[idx] = (self.menuList[idx][0],
                 self.menuList[idx][1],
                 self.menuList[idx][2],
                 None)

        self['ButtonBluetext'].hide()
        self['ButtonYellowtext'].setText(_('Select all'))
        self.select_all = True
        self['menu'].updateList(self.menuList)

    def updateRemoveList(self):
        self.removelist = []
        for idx in range(len(self.menuList)):
            if not self.menuList[idx][3] == None:
                self.removelist.append(self.menuList[idx][1])

        if len(self.removelist) > 0:
            self['ButtonBluetext'].show()
            if len(self.removelist) == len(self.menuList):
                self['ButtonYellowtext'].setText(_('Deselect all'))
                self.select_all = False
            else:
                self['ButtonYellowtext'].setText(_('Select all'))
                self.select_all = True
        else:
            self['ButtonBluetext'].hide()
            self['ButtonYellowtext'].setText(_('Select all'))
            self.select_all = True

    def changeSelection(self):
        if not self.removing:
            idx = self['menu'].getIndex()
            name = self.menuList[idx][1]
            flag = self.menuList[idx][2]
            position = self.getlan(name)
            if self.menuList[idx][3] == None:
                self.menuList[idx] = (position,
                 name,
                 flag,
                 self.removeIcon)
            else:
                self.menuList[idx] = (position,
                 name,
                 flag,
                 None)
            self.updateRemoveList()
            self['menu'].updateList(self.menuList)

    def createMenu(self):
        list = []
        self.menuList = []
        self['menu'].setList(self.menuList)
        path = '/usr/share/enigma2/po/'
        self.path = path
        i = 0
        for x in os_listdir(path):
            i = i + 1
            filepath = path + x
            if os_path.exists(filepath):
                lan = self.getlan(x)
                secondkey = self.getsecondkey(x)
                flag = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/share/enigma2/countries/' + secondkey + '.png'))
                self.menuList.append((lan,
                 x.encode('utf-8'),
                 flag,
                 None))

        self.menuList.sort()
        if len(self.removelist) > 0:
            self['ButtonBluetext'].show()
        else:
            self['ButtonBluetext'].hide()
        self['menu'].setList(self.menuList)

    def removeLang(self):
        if not len(self.removelist) == 0:
            self.currentIndex = 0
            self.createMenu()
            self.removing = True
            lang = self.removelist[self.currentIndex]
            if lang == 'pt_BR':
                lang = 'pt-br'
            cmd = 'opkg remove enigma2-language-' + lang
            self.container = eConsoleAppContainer()
            self.container.appClosed.append(self.removeLangClosed)
            self.container.execute(cmd)

    def removeLangClosed(self, status):
        print '[Language manager] status:%s' % status
        path = '/usr/share/enigma2/po/'
        folderpathfile = path + self.removelist[self.currentIndex] + '/LC_MESSAGES/enigma2.mo'
        foldermess = path + self.removelist[self.currentIndex] + '/LC_MESSAGES/'
        folderpath = path + self.removelist[self.currentIndex]
        if os_path.exists(folderpathfile):
            os_remove(folderpathfile)
        if os_path.exists(foldermess):
            removeDir(foldermess)
        if os_path.exists(folderpath):
            removeDir(folderpath)
        self.createMenu()
        self.currentIndex = self.currentIndex + 1
        if self.currentIndex < len(self.removelist):
            lang = self.removelist[self.currentIndex]
            if lang == 'pt_BR':
                lang = 'pt-br'
            cmd = 'opkg remove enigma2-language-' + lang
            self.container = eConsoleAppContainer()
            self.container.appClosed.append(self.removeLangClosed)
            self.container.execute(cmd)
        else:
            self.removelist = []
            self.removing = False
            self.createMenu()
