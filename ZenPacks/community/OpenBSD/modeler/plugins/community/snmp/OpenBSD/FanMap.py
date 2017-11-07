################################################################################
#
# This program is part of the OpenBSD Zenpack for Zenoss.
# Copyright (C) 2017 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""FanMap

FanMap maps the sensorTable table to fans objects

$Id: FanMap.py,v 1.0 2017/10/31 20:21:42 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class FanMap(SnmpPlugin):
    """Map OpenBSD sensor table to model."""

    maptype = "FanMap"
    modname = "Products.ZenModel.Fan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('sensorTable',
                    '.1.3.6.1.4.1.30155.2.1.2.1',
                    {
                        '.2': 'id',
                        '.3': '_type',
                        '.7': 'state',
                    }
        ),
    )

    states  =  {0:'unspecified',
                1:'ok',
                2:'warn',
                3:'critical',
                4:'unknown'}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, sensor in tabledata.get("sensorTable",{}).iteritems():
            try:
                om = self.objectMap(sensor)
                if int(om._type) != 1: continue
                om.snmpindex = oid.strip('.')
                om.id = self.prepId(om.id)
                om.state = self.states.get(int(om.state), 'unknown')
            except AttributeError:
                continue
            rm.append(om)
        return rm
