################################################################################
#
# This program is part of the OpenBSD Zenpack for Zenoss.
# Copyright (C) 2017 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""genuaDeviceMap

genuaDeviceMap map mib elements from GENUA-MIB to get hw and os
products.

$Id: genuaDeviceMap.py,v 1.0 2017/10/31 20:21:42 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
import re

class genuaDeviceMap(SnmpPlugin):
    """Map mib elements from GENUA-MIB to get hw and os
    products.
    """

    maptype = "genuaDeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.3717.2.3.1.0' : 'setHWProductKey',
        '.1.3.6.1.4.1.3717.2.3.2.0' : 'setOSProductKey',
        '.1.3.6.1.4.1.3717.2.3.3.0' : '_release',
        '.1.3.6.1.4.1.3717.2.3.4.0' : '_patch',
        '.1.3.6.1.4.1.3717.2.3.5.0' : 'setHWTag',
        '.1.3.6.1.4.1.3717.2.3.6.0' : 'setHWSerialNumber',
        })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        try:
            from Products.DataCollector.plugins.DataMaps import MultiArgs
            om.setHWProductKey = MultiArgs(om.setHWProductKey, "genua")
            om.setOSProductKey = MultiArgs(om.setOSProductKey, "genua")
        except:
            om.setHWProductKey = "genua %s"%(om.setHWProductKey)
            om.setOSProductKey = "genua %s"%(om.setOSProductKey)
        return om


