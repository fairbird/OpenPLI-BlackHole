from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.PluginComponent import plugins
from Components.Sources.List import List
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.config import config, configfile, getConfigListEntry, ConfigInteger, NoSave
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN_IMAGE
from Tools.LoadPixmap import LoadPixmap
from BhAddons import DeliteAddons
from BhScript import DeliteScript
from BhUtils import DeliteGetSkinPath
from operator import itemgetter

class DeliteGreenPanel(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Panel Setup'))
        self['key_green'] = Label(_('Fast Plug'))
        self['key_yellow'] = Label(_('Addons'))
        self['key_blue'] = Label(_('Scripts'))
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.save,
         'back': self.close,
         'red': self.Redc,
         'green': self.Fastplug,
         'yellow': self.Addons,
         'blue': self.NabScript}, -1)

    def save(self):
        self.run()

    def run(self):
        mysel = self['list'].getCurrent()
        if mysel:
            plugin = mysel[3]
            plugin(session=self.session)

    def updateList(self):
        self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
        sorted_dict = {}
        self.list = []
        mylist = []
        if fileExists('/etc/bh_plugins.pos') == False:
            i = 1
            out = open('/etc/bh_plugins.pos', 'w')
            for plugin in self.pluginlist:
                line = '%s:%d\n' % (plugin.name, i)
                out.write(line)
                i += 1

            out.close()
        f = open('/etc/bh_plugins.pos', 'rb')
        for line in f.readlines():
            d = line.split(':', 1)
            if len(d) > 1:
                sorted_dict[d[0].strip()] = int(d[1].strip())
            f.close()

        for plugin in self.pluginlist:
            pos = sorted_dict.get(plugin.name, 99)
            if plugin.icon is None:
                png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/icons/plugin.png'))
            else:
                png = plugin.icon
            res = (plugin.name,
             plugin.description,
             png,
             plugin,
             pos)
            mylist.append(res)

        self.list = sorted(mylist, key=itemgetter(4))
        self['list'].list = self.list

    def Addons(self):
        self.session.open(DeliteAddons)

    def Redc(self):
        self.session.openWithCallback(self.updateList, BhSetupGreen)

    def NabScript(self):
        self.session.open(DeliteScript)

    def Fastplug(self):
        result = ''
        check = False
        myplug = config.delite.fp.value
        for plugin in self.list:
            result = plugin[3].name
            if result == myplug:
                runplug = plugin[3]
                check = True
                break

        if check == True:
            runplug(session=self.session)
        else:
            mybox = self.session.open(MessageBox, _('Fast Plugin not found. You have to setup Fast Plugin before to use this shortcut.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))

    def NotYet(self):
        mybox = self.session.open(MessageBox, _('Function Not Yet Available'), MessageBox.TYPE_INFO)
        mybox.setTitle(_('Info'))


class BhSetupGreen(Screen):
    skin = '\n\t<screen position="center,center" size="390,330" title="Black Hole Green Panel Setup">\n\t\t<widget source="list" render="Listbox" position="10,16" size="370,300" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t{"template": [\n                    \tMultiContentEntryText(pos = (50, 1), size = (320, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                 \tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                    \t],\n                    \t"fonts": [gFont("Regular", 22)],\n                    \t"itemHeight": 36\n                \t}\n            \t\t</convert>\n\t\t</widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = DeliteGetSkinPath()
        mypixmap = mypath + 'icons/plugin_list_setup.png'
        png = LoadPixmap(mypixmap)
        name = _('Reorder plugins list')
        idx = 0
        res = (name, png, idx)
        self.list.append(res)
        mypixmap = mypath + 'icons/fast_plugin_setup.png'
        png = LoadPixmap(mypixmap)
        name = _('Fast Plugin Setup')
        idx = 1
        res = (name, png, idx)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            self.session.open(BhGreenPluginsSetup)
        elif self.sel == 1:
            self.session.open(DeliteSetupFp)


class BhGreenPluginsSetup(Screen, ConfigListScreen):
    skin = '\n\t<screen position="center,center" size="600,400" title="Reorder Plugin List">\n\t\t<widget name="config" position="30,10" size="540,320" scrollbarMode="showOnDemand"/>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="50,350" size="140,40" alphatest="on"/>\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="400,350" size="140,40" alphatest="on"/>\n\t\t<widget name="key_red" position="50,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t\t<widget name="key_green" position="400,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Save'))
        self['key_green'] = Label(_('Cancel'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.savePos,
         'green': self.close,
         'back': self.close})
        self.updateList()

    def updateList(self):
        self.list = []
        mylist = []
        sorted_dict = {}
        f = open('/etc/bh_plugins.pos', 'rb')
        for line in f.readlines():
            d = line.split(':', 1)
            if len(d) > 1:
                sorted_dict[d[0].strip()] = int(d[1].strip())
            f.close()

        self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
        for plugin in self.pluginlist:
            pos = sorted_dict.get(plugin.name, 99)
            res = (plugin.name, pos)
            mylist.append(res)

        mylist2 = sorted(mylist, key=itemgetter(1))
        for x in mylist2:
            item = NoSave(ConfigInteger(limits=(1, 99), default=99))
            item.value = x[1]
            res = getConfigListEntry(x[0], item)
            self.list.append(res)

        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def savePos(self):
        mylist = []
        for x in self['config'].list:
            res = (x[0], x[1].value)
            mylist.append(res)

        mylist2 = sorted(mylist, key=itemgetter(1))
        out = open('/etc/bh_plugins.pos', 'w')
        for x in mylist2:
            line = '%s:%d\n' % (x[0], x[1])
            out.write(line)

        out.close()
        self.session.open(MessageBox, _('Plugins list positions saved.'), MessageBox.TYPE_INFO)
        self.close()


class DeliteSetupFp(Screen):
    skin = '\n\t<screen position="160,115" size="390,370" title="Black Hole Fast Plugin Setup">\n\t\t<widget source="list" render="Listbox" position="10,10" size="370,300" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="115,320" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="115,320" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Set Favourite'))
        self.list = []
        self['list'] = List(self.list)
        self.updateList2()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.save,
         'back': self.close,
         'red': self.save}, -1)

    def updateList2(self):
        self.list = []
        self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
        for plugin in self.pluginlist:
            if plugin.icon is None:
                png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/icons/plugin.png'))
            else:
                png = plugin.icon
            res = (plugin.name, plugin.description, png)
            self.list.append(res)

        self['list'].list = self.list

    def save(self):
        mysel = self['list'].getCurrent()
        if mysel:
            mysel = mysel[0]
            message = _('Fast plugin set to: ') + mysel + '\n' + _('Key: 2x Green')
            mybox = self.session.openWithCallback(self.close, MessageBox, message, MessageBox.TYPE_INFO)
            mybox.setTitle(_('Configuration Saved'))
            config.delite.fp.value = mysel
            config.delite.fp.save()
            configfile.save()


class DeliteGp:

    def __init__(self):
        self['DeliteGp'] = ActionMap(['InfobarSubserviceSelectionActions'], {'DeliteGpshow': self.showDeliteGp})

    def showDeliteGp(self):
        self.session.openWithCallback(self.callNabAction, DeliteGreenPanel)

    def callNabAction(self, *args):
        if len(args):
            actionmap, context, action = args
            actionmap.action(context, action)
