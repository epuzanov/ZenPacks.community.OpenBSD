
import Globals
import os.path
from xml.dom import minidom

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
objxmlPath = os.path.join(os.path.dirname(__file__), 'objects', 'objects.xml')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase


class ZenPack(ZenPackBase):

    newplugins = ('community.snmp.OpenBSD.FanMap',
                  'community.snmp.OpenBSD.PowerSupplyMap',
                  'community.snmp.OpenBSD.TemperatureSensorMap',
                 )

    def install(self, app):
        pcache = []
        xmldoc = minidom.parse(objxmlPath)
        for o in xmldoc.getElementsByTagName('object'):
            lend = {'Report':-1,'RRDTemplate':-2}.get(o.getAttribute('class'),0)
            cpath = o.getAttribute('id').split('/')[3:lend]
            if (cpath in pcache) or (lend == 0):
                continue
            co = self.dmd
            for id in cpath:
                if not hasattr(co, id):
                    newc = co.__class__(str(id))
                    co._setObject(str(id), newc)
                co = getattr(co, id)
            pcache.append(cpath)
        ZenPackBase.install(self, app)
        cpl = list(co.zCollectorPlugins)
        for plugin in self.newplugins:
            if not plugin in cpl:
                cpl.append(plugin)
        if isinstance(co.zCollectorPlugins, tuple):
            cpl = tuple(cpl)
        co._setProperty('zCollectorPlugins', cpl)

    def upgrade(self, app):
        pcache = []
        xmldoc = minidom.parse(objxmlPath)
        for o in xmldoc.getElementsByTagName('object'):
            lend = {'Report':-1,'RRDTemplate':-2}.get(o.getAttribute('class'),0)
            cpath = o.getAttribute('id').split('/')[3:lend]
            if (cpath in pcache) or (lend == 0):
                continue
            co = self.dmd
            for id in cpath:
                if not hasattr(co, id):
                    newc = co.__class__(str(id))
                    co._setObject(str(id), newc)
                co = getattr(co, id)
            pcache.append(cpath)
        ZenPackBase.upgrade(self, app)
        cpl = list(co.zCollectorPlugins)
        for plugin in self.newplugins:
            if not plugin in cpl:
                cpl.append(plugin)
        if isinstance(co.zCollectorPlugins, tuple):
            cpl = tuple(cpl)
        if co.isLocal('zCollectorPlugins'):
            co._delProperty('zCollectorPlugins')
        co._setProperty('zCollectorPlugins', cpl)

    def remove(self, app, leaveObjects=False):
        try:
            co = app.zport.dmd.Devices.getOrganizer('Server/OpenBSD')
            co._delProperty('zCollectorPlugins')
        except KeyError:
            pass
        ZenPackBase.remove(self, app, leaveObjects)
