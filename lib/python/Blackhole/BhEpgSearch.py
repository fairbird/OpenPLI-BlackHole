from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.EventView import EventViewSimple
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists
from os import remove as os_remove
from ServiceReference import ServiceReference
from enigma import eEPGCache, eTimer

class Nab_EpgSearch(Screen):
    skin = '\n\t<screen position="30,70" size="660,460" title="Black Hole Epg Search">\n\t\t<widget source="list" render="Listbox" position="10,10" size="640,440" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t{"template": [\n              \t\t  MultiContentEntryText(pos = (110, 0), size = (530, 24), font=0, text = 0),\n               \t\t MultiContentEntryText(pos = (110, 24), size = (530, 36), font=1, text = 1),\n               \t\t MultiContentEntryPixmapAlphaTest(pos = (0, 0), size = (100, 60), png = 2),\n                \t],\n                \t"fonts": [gFont("Regular", 24),gFont("Regular", 22)],\n                \t"itemHeight": 60\n                \t}\n            \t\t</convert>\n\t\t</widget>\n\t</screen>'

    def __init__(self, session, cmd):
        Screen.__init__(self, session)
        self.myserv = []
        self['list'] = List([])
        self.epgcache = eEPGCache.getInstance()
        self['actions'] = ActionMap(['WizardActions'], {'ok': self.KeyOk,
         'back': self.close})
        self.menTimer = eTimer()
        self.menTimer.timeout.get().append(self.SearchNot)
        self.onClose.append(self.delTimer)
        self.searchEvent(cmd)

    def searchEvent(self, cmd):
        flist = []
        mycache = []
        idx = 0
        if len(cmd) > 1:
            if fileExists('/etc/nabepgcache'):
                f = open('/etc/nabepgcache', 'r')
                for line in f.readlines():
                    if cmd != line.strip():
                        mycache.append(line.strip())

                f.close()
            mycache.append(cmd)
            if len(mycache) > 10:
                mycache = mycache[1:]
            f1 = open('/etc/nabepgcache', 'w')
            for fil in mycache:
                f1.write(fil + '\n')

            f1.close()
        self.myserv = self.epgcache.search(('IR',
         48,
         eEPGCache.PARTIAL_TITLE_SEARCH,
         cmd,
         1))
        if self.myserv is not None:
            for fil in self.myserv:
                picon = self.find_Picon(fil[1])
                sserv = ServiceReference(fil[1])
                provider = sserv.getServiceName()
                event = self.epgcache.lookupEventId(sserv.ref, int(fil[0]))
                strview = event.getBeginTimeString() + '   ' + provider + '   ' + event.getEventName() + '   (' + '%d min' % (event.getDuration() / 60) + ')'
                ext = event.getShortDescription()
                if len(ext) > 70:
                    ext = ext[:70] + '..'
                res = self.fill_List(strview, ext, picon, idx)
                flist.append(res)
                idx = idx + 1

            self['list'].list = flist
        else:
            self.menTimer.start(100, False)

    def fill_List(self, title, desc, mypixmap, idx):
        png = LoadPixmap(mypixmap)
        return (title,
         desc,
         png,
         idx)

    def find_Picon(self, sname):
        searchPaths = ['/usr/share/enigma2/%s/', '/media/cf/%s/', '/media/usb/%s/']
        pos = sname.rfind(':')
        if pos != -1:
            sname = sname[:pos].rstrip(':').replace(':', '_')
        for path in searchPaths:
            pngname = path % 'picon' + sname + '.png'
            if fileExists(pngname):
                return pngname

        return '/usr/share/enigma2/skin_default/picon_default.png'

    def KeyOk(self):
        myi = self['list'].getCurrent()
        if myi is not None:
            myi = myi[3]
            fil = self.myserv[myi]
            sserv = ServiceReference(fil[1])
            event = self.epgcache.lookupEventId(sserv.ref, int(fil[0]))
            self.session.open(EventViewSimple, event, sserv)

    def SearchNot(self):
        self.menTimer.stop()
        self.session.open(MessageBox, _('Sorry no events found matching to the search criteria.'), MessageBox.TYPE_INFO)

    def delTimer(self):
        del self.menTimer


class Nab_EpgSearchLast(Screen):
    skin = '\n\t<screen position="160,115" size="390,320" title="Black Hole Epg Search History">\n\t\t<widget source="list" render="Listbox" position="10,10" size="370,260" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="115,270" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="115,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        mycache = []
        idx = 0
        if fileExists('/etc/nabepgcache'):
            f = open('/etc/nabepgcache', 'r')
            for line in f.readlines():
                res = (line.strip(), idx)
                mycache.append(res)
                idx = idx + 1

            f.close()
        if len(mycache) > 0:
            mycache.reverse()
        self['list'] = List(mycache)
        self['key_red'] = Label(_('Clear History'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close,
         'red': self.clearCa})

    def KeyOk(self):
        myi = self['list'].getCurrent()
        if myi:
            myi = myi[0]
            self.session.open(Nab_EpgSearch, myi)

    def clearCa(self):
        if fileExists('/etc/nabepgcache'):
            os_remove('/etc/nabepgcache')
        mycache = []
        self['list'].list = mycache
