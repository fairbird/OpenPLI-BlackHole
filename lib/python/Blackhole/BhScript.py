from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from os import system, listdir

class DeliteScript(Screen):
    skin = '\n\t<screen position="80,100" size="560,410" title="Black Hole Script Panel">\n\t\t<widget source="list" render="Listbox" position="10,10" size="540,300" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t\t<widget name="statuslab" position="10,320" size="540,30" font="Regular;16" valign="center" noWrap="1" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="210,360" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="210,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['statuslab'] = Label('N/A')
        self['key_red'] = Label(_('Execute'))
        self.mlist = []
        self.populateSL()
        self['list'] = List(self.mlist)
        self['list'].onSelectionChanged.append(self.schanged)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.mygo,
         'back': self.close,
         'red': self.mygo})
        self.onLayoutFinish.append(self.refr_sel)

    def refr_sel(self):
        self['list'].index = 1
        self['list'].index = 0

    def populateSL(self):
        myscripts = listdir('/usr/script')
        for fil in myscripts:
            if fil.find('.sh') != -1:
                fil2 = fil[:-3]
                desc = 'N/A'
                f = open('/usr/script/' + fil, 'r')
                for line in f.readlines():
                    if line.find('#DESCRIPTION=') != -1:
                        line = line.strip()
                        desc = line[13:]

                f.close()
                res = (fil2, desc)
                self.mlist.append(res)

    def schanged(self):
        mysel = self['list'].getCurrent()
        if mysel:
            mytext = ' ' + mysel[1]
            self['statuslab'].setText(mytext)

    def mygo(self):
        mysel = self['list'].getCurrent()
        if mysel:
            mysel = mysel[0]
            mysel2 = '/usr/script/' + mysel + '.sh'
            mytitle = 'Black Hole E2 Script: ' + mysel
            self.session.open(Console, title=mytitle, cmdlist=[mysel2])
