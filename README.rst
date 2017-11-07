==============================
ZenPacks.community.OpenBSD
==============================

About
=====

This Monitoring ZenPack provides OpenBSD Environmental monitoring including fans,
temperature sensors end power supplies.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 4.2.5 and Zenoss 5.2.3.


Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `OpenBSD ZenPack <https://www.zenoss.com/product/zenpacks/openbsd>`_.
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.OpenBSD-1.0.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the OpenBSD
ZenPack you should clone the git `repository <https://github.com/epuzanov/ZenPacks.community.OpenBSD>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.OpenBSD.git
        zenpack --link --install ZenPacks.community.OpenBSD
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.

Modeler Plugins
---------------

- **community.snmp.OpenBSD.FanMap** - Fan modeler plugin.
- **community.snmp.OpenBSD.PowerSupplyMap** - Power Supply modeler plugin.
- **community.snmp.OpenBSD.TemperatureSensorMap** - Temperature Sensor modeler
  plugin.

Monitoring Templates
--------------------

- Devices/Server/OpenBSD/Fan
- Devices/Server/OpenBSD/PowerSupply
- Devices/Server/OpenBSD/TemperatureSensor
