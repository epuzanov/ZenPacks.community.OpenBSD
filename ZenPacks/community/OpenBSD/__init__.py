
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass


class ZenPack(ZenPackBase):

    newplugins = ('community.snmp.OpenBSD.FanMap',
                  'community.snmp.OpenBSD.PowerSupplyMap',
                  'community.snmp.OpenBSD.TemperatureSensorMap',
                 )

    def install(self, app):
        ZenPackBase.install(self, app)
        try:
            dc = app.zport.dmd.Devices.getOrganizer('Server/OpenBSD')
        except KeyError:
            dc = app.zport.dmd.Devices.getOrganizer('Server')
            manage_addDeviceClass(dc, 'OpenBSD')
            dc = app.zport.dmd.Devices.getOrganizer('Server/OpenBSD')
        cpl = list(getattr(dc, 'zCollectorPlugins'))
        for plugin in self.newplugins:
            if not plugin in cpl: cpl.append(plugin)
        dc.zCollectorPlugins = list(cpl)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        try:
            dc = app.zport.dmd.Devices.getOrganizer('Server/OpenBSD')
        except KeyError:
            dc = app.zport.dmd.Devices.getOrganizer('Server')
            manage_addDeviceClass(dc, 'OpenBSD')
            dc = app.zport.dmd.Devices.getOrganizer('Server/OpenBSD')
        cpl = list(getattr(dc, 'zCollectorPlugins'))
        for plugin in self.newplugins:
            if not plugin in cpl: cpl.append(plugin)
        dc.zCollectorPlugins = list(cpl)

    def remove(self, app, leaveObjects=False):
        try:
            dc = app.zport.dmd.Devices.getOrganizer('Server/OpenBSD')
            cpl = list(getattr(dc, 'zCollectorPlugins'))
            for plugin in self.newplugins:
                if plugin in cpl: cpl.remove(plugin)
            dc.zCollectorPlugins = list(cpl)
        except KeyError:
            pass
        ZenPackBase.remove(self, app, leaveObjects)
