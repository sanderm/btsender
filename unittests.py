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

import unittest
from InfoLib import *

class TestBDSender(unittest.TestCase):
    """Class for unit tests."""

    def testfilesinit(self):
        files = Files()
        files.log_out= 0
        self.assertEqual(files.file, 0)

    def testappend(self):
        files = Files()
        files.log_out= 0
        files.append("file2", "path")
        self.assertNotEqual(files.file, 0)

    def testdevicesinit(self):
        devices = Devices()
        devices.log_out= 0
        self.assert_(devices.dev == 0 and devices.count == 0)

    def testissending(self):
        devices = Devices()
        devices.log_out= 0
        devices.actually_send_files= 0
        device = Device("AA")
        device.log_out= 0
        device.actually_send_files= 0
        device.last_sent = 1
        device.files.append(File("file3", "files/klovner.jpg"))
        devices.is_sending(device)
        self.assert_(device.last_sent > 0 and device.is_sending == 1)

    def testisfinishedsending(self):
        devices = Devices()
        devices.log_out= 0
        device = Device("AA")
        device.log_out= 0
        devices.is_finished_sending(device)
        self.assertEqual(device.is_sending, 0)

    def testiadd(self):
        devices = Devices()
        devices.log_out= 0
        devices += "AA"
        self.assert_(devices.count > 0)

    def testgetitem(self):
        devices = Devices()
        devices.log_out= 0
        device = Device("AA")
        device.log_out= 0
        devices += "AA"
        tester = devices["AA"]
        self.assertEqual(device.address, tester.address)

    def testsetonline(self):
        devices = Devices()
        devices.log_out= 0
        devices += "AA"
        devices["AA"].online = 0
        devices.set_online("AA")
        self.assertEqual(devices["AA"].online, 1)

    def testdeviceinit(self):
        device = Device("AA")
        device.log_out= 0
        self.assert_(device.online == 1 and device.next == 0 and
                     device.last_sent == 0 and device.is_sending == 0)

    def testfileinit(self):
        file = File("file4", "path")
        self.assert_(file.filename == "file4" and
                     file.filepath == "path" and file.next == 0)

if __name__ == "__main__":
    unittest.main()
