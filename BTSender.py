#!/usr/bin/env python

#
#  BTSender by Arve and Sander ( Bluetooth Sender )
#  Copyright (C) 2006  Arve Barsnes and Sander Johansen
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#  Sander Johansen <sanderj@ifi.uio.no>
#  Arve Barsnes <arveba@ifi.uio.no>
#

class BlueToothServer:

  def __init__(self):
    self.devices_available = data.Devices()

  def blue_scan(self):

    self.devices_available.reset()
    devices = bluetooth.discover_devices()
    service_name = bluetooth.OBEX_OBJPUSH_CLASS;

    for dev in devices:

      services = bluetooth.find_service(address=dev, uuid=service_name)
      if len(services) > 0:
        self.devices_available += dev

    self.devices_available.event()

if __name__ == '__main__':

  import sys
  import bluetooth
  import os
  import time
  import InfoLib as data

  bts = BlueToothServer()
  
  while 1:
    try:
      bts.blue_scan()
      time.sleep(1)
    except KeyboardInterrupt:
      print "Shutting down..."
      sys.exit()

