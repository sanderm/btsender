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

import time, os, sys
import pythonussp

# seconds of time between a file is finished and a new file is sent, 
# some delay caused when scanning after devices
time_between_files = 0

# how much time to wait untill stopping a transfer in seconds
sending_timeout= 10000

# send file to remote device (1), or just pretend doing it (0)
actually_send_files = 1

# print file stats regular, time in seconds, 0= disable
log_stats_secs= 30

# print log messages?
log_out = 1

# resend files next time someone comes online
resend_files= 1

# the dir where files to send is located
file_dir = "files"

# log dir
log_dir="logs"

class Files:
  """The class for keeping info about files to send to devices."""

  def __init__(self):
    global files_available, log_out, file_dir, log_dir
    files_available = self
    self.file = 0
    self.log_out= log_out
    self.file_dir= file_dir
    self.log_dir= log_dir
    self.update_files()
    

  def get_stats(self):
    current = self.file
    num_accepted= 0
    num_rejected= 0
    num_ignored= 0
    num_error= 0
    while current != 0:
      #print "loop1"
      (accepted,rejected,ignored,error) =current.get_stats()
      num_accepted += accepted
      num_rejected += rejected
      num_ignored += ignored
      num_error += error
      current = current.next
    return (num_accepted,num_rejected,num_ignored,num_error)

  def update_files(self):

    files = os.listdir(self.file_dir)

    for file in files:
      #print "loop2"
      filename = os.path.basename(file)
      filepath = os.path.join(file_dir,file)
      self.append(filename, filepath)

  def append(self, filename, filepath):
    f= File(filename,filepath)
    if self.log_out != 0:
      print "Added file:", filename

    if self.file == 0:
      self.file = f
    else:
      current = self.file
      while current.next != 0:
        #print "loop3"
        current = current.next
      current.next = f

class File:
  """The class for info about a specific file."""
  def __init__(self, filename, filepath):
    self.filename = filename
    self.filepath = filepath
    self.next = 0
    self.num_accepted= 0
    self.num_rejected= 0
    self.num_ignored= 0
    self.num_error= 0
  def get_stats(self):
    return (self.num_accepted,self.num_rejected,self.num_ignored,self.num_error)

class Devices:
  """The class for keeping the info about the devices."""
  def __init__(self):
    global log_out, actually_send_files, log_stats_secs, log_dir
    self.dev = 0
    self.count = 0
    self.online = ()
    self.log_out= log_out
    self.log_dir= log_dir
    self.actually_send_files= actually_send_files
    self.num_connected= 0
    self.log_stats_secs= log_stats_secs
    self.files_available = Files()
    self.last_stats_print= time.time()
    filename= self.add_date(self.log_dir + "/btsender")
    self.f = open(filename, 'w')

  def event(self):
    self.prune()
    self.check_sending_files()
    if self.log_stats_secs:
      if self.last_stats_print + self.log_stats_secs < time.time():
        self.print_stats()
        self.last_stats_print= time.time()

  def print_stats(self):
    (num_accepted,num_rejected,num_ignored,num_error)= self.files_available.get_stats()
    
    print "Connected:", self.num_connected, "\tAccepted:", num_accepted, "\tRejected:", num_rejected, "\tIgnored:", num_ignored, "\tError:", num_error, "\tOnline now:", self.get_num_online(), "\tSending now:", self.get_num_sending()
    self.f.write("Connected: " + str(self.num_connected) + " \tAccepted: " + str(num_accepted) + " \tRejected: " + str(num_rejected) + " \tIgnored: " + str(num_ignored) + " \tError: " + str(num_error) + " \tOnline now: " + str(self.get_num_online()) + " \tSending now: " + str(self.get_num_sending()) + "\n")
    self.f.flush()

  # returns the current date added to the file name
  def add_date(self,file):
    date= time.strftime("%Y_%m_%d__%H_%M_%S");
    return file + "_" + date + ".txt";

  def log(self,b,msg):
    self.f.write(time.ctime() +  " : " + b.address + " : " + msg + "\n")
    self.f.flush() 
    if self.log_out != 0:
      print time.ctime(), ":", b.address, ":", msg

  def is_connecting(self,b):
    """Current device is connecting."""
    b.online= 1
    b.possible_offline= 0
    self.log(b,"Connecting: " + str(self.num_connected))
    self.try_sending(b)

  def is_online(self,b):
    """Current device is still online."""
    self.try_sending(b)
    
  def is_disconnecting(self,b):
    """Current device is disconnecting."""
    time_connected= int(time.time() - b.connected_time)
    self.log(b,"Disconnecting after " + str(time_connected) + "s")
    b.online= 0
    b.possible_offline= 0
    
  def is_sending(self,b):
    """Is supposed to send a file to current device."""
    global time_between_files
    if b.last_sent == 0:
      last_sent = 0
    else:
      last_sent = int(time.time() - b.last_sent)

    b.sending_file= b.files[0]
    self.log(b,"Sending file " + b.files[0].filename + " after " + str(last_sent) + "s")
    b.last_sent= time.time()
    if self.actually_send_files == 1:
       b.sending_pid= self.handle_fork(b.address + '@', b.files[0].filepath, b.files[0].filename, 60)
    else:
       b.sending_pid= 1

  def handle_fork(self,address, filepath, filename, sec):
    self.f.flush()
    pid= os.fork();
    if pid == 0:
      ret= pythonussp.ussp_call(address, filepath, filename, sec)
      sys.exit(ret)
    else:
      return pid

  def maybe_finished_sending(self,b):
    """Current device is finished reciving a file."""
    child_ended= 0
    if b.last_sent != 0:
      last_sent= int(time.time() - b.last_sent)
    else:
      last_sent= 0

    if self.actually_send_files == 1:
      try:
        (retpid,status)= os.waitpid(b.sending_pid, os.WNOHANG)
      except OSError:
        child_ended= 1
    else:
      retpid= 1
      status= 0

    if child_ended:
      b.sending_file.num_error += 1
      self.log(b,"Transfer killed #" + str(b.sending_file.num_error) + " after " + str(last_sent) + "s")
    else:
      if retpid != 0:
        child_ended= 1
        if os.WIFEXITED(status):
          status_val= os.WEXITSTATUS(status)
          if status_val == 0:
            b.sending_file.num_accepted += 1
            self.log(b,"Transfer finished #" + str(b.sending_file.num_accepted) + " after " + str(last_sent) + "s")
          elif status_val == 1:
            b.sending_file.num_error += 1
            self.log(b,"Transfer error, cant find file #" + str(b.sending_file.num_error) + " after " + str(last_sent) + "s")
          elif status_val == 2:
            b.sending_file.num_error += 1
            self.log(b,"Transfer error, connection refused #" + str(b.sending_file.num_error) + " after " + str(last_sent) + "s")
          elif status_val == 3:
            b.sending_file.num_error += 1
            self.log(b,"Transfer error, under sending file #" + str(b.sending_file.num_error) + " after " + str(last_sent) + "s")
          elif status_val == 4:
            b.sending_file.num_error += 1
            self.log(b,"Transfer error, under getting the response #" + str(b.sending_file.num_error) + " after " + str(last_sent) + "s")
          elif status_val == 5:
            b.sending_file.num_rejected += 1
            self.log(b,"Transfer rejected by user #" + str(b.sending_file.num_rejected) + " after " + str(last_sent) + "s")
          else:
            b.sending_file.num_error += 1
            self.log(b,"Transfer error, unknown #" + str(b.sending_file.num_error) + " after " + str(last_sent) + "s")
        else:
          b.sending_file.num_error += 1
          self.log(b,"Transfer interupted #" + str(b.sending_file.num_error) + " after " + str(last_sent) + "s")
    
      else:
        if last_sent > sending_timeout:
          b.sending_file.num_ignored += 1
          self.log(b,"Transfer timed out #" + str(b.sending_file.num_ignored) + " after " + str(last_sent) + "s")
          os.kill(b.sending_pid, 9)
          child_ended= 1
    
    if child_ended:
      b.sending_pid = 0
      b.last_sent = time.time()
      return 1
    else:
      return 0

  def try_sending(self,b):
    """Send a file when the time is right."""
    global time_between_files

    if (b.last_sent + time_between_files) < time.time() and b.last_sent != -1:
      if len(b.files) > 0:
        self.is_sending(b)
        del b.files[0]
      else:
        self.log(b,"No more files to send")
        b.last_sent = -1

  def __iadd__(self, addr):
    """Add a new device, if it already is added set it to online."""

    b = self[addr]
    if b != 0:
      if b.online:
        if b.sending_pid != 0:
          ready_to_send= self.maybe_finished_sending(b)
        else:
          ready_to_send= 1

        if ready_to_send:
          self.is_online(b)
        b.possible_offline= 0
      else:
        self.is_connecting(b)
        if resend_files:
          b.update_files()

    else:
      b = Device(addr)
      if self.count == 0:
        self.dev = b
        self.count = 1
      else:
        current = self.dev
        while current.next != 0:
          #print "loop4"
          current = current.next
        current.next = b
        self.count += 1
      self.is_connecting(b)
      self.num_connected += 1
    return self

  def reset(self):
    """Set all devices to off."""
    if self.count == 0:
      return
    current = self.dev
    while current != 0:
      #print "loop5"

      # make sure someone who is reciving a file isn't listed
      # as offline, even if the device is offline
      ###
      if current.sending_pid == 0 and current.online:
        current.possible_offline = 1
      current = current.next

  def check_sending_files(self):
    current = self.dev
    while current != 0:
      #print "loop6"
      if current.sending_pid != 0:
        self.maybe_finished_sending(current)
      current = current.next

  def get_num_online(self):
    online= 0
    current = self.dev
    while current != 0:
      #print "loop7"
      if current.online:
        online += 1
      current = current.next
    return online

  def get_num_sending(self):
    sending= 0
    current = self.dev
    while current != 0:
      #print "loop7"
      if current.online and current.sending_pid != 0:
        sending += 1
      current = current.next
    return sending
    

  def prune(self):
    """Delete all devices possible offline."""
    # update the first pointer if elements first is deleted
    while self.count != 0 and self.dev.possible_offline:
      #print "loop8"
      self.is_disconnecting(self.dev)
      #if resend_files:
      #  self.dev = self.dev.next
      #  self.count -= 1

    current = self.dev
    if current != 0:
      # delete all other devices set to off
      while current.next != 0:
        #print "loop9"
        if current.next.possible_offline:
          if current.next.online == 1:
            self.is_disconnecting(current.next)
            #if resend_files:
            #  current.next = current.next.next
            #  self.count -= 1
        current = current.next

  def __getitem__(self, i):
    """Return device with address i if it exists."""
    if self.count == 0:
      return 0
    current = self.dev
    while current != 0:
      #print "loop10"
      if current.address == i:
        return current
      current= current.next
    return 0

  def set_possible_offline(self,addr):
    """Set a device to online."""
    current = self.dev
    while current != 0:
      #print "loop11"
      if current.address == addr and current.online:
        current.possible_offline= 1
        return
      current = current.next


class Device:
  """The class for info about a specific device."""

  def __init__(self, address):
    self.address = address
    self.next = 0
    self.online = 1
    self.possible_offline= 0
    self.last_sent = 0
    self.connected_time = time.time()
    self.sending_pid = 0
    self.sending_file= 0
    self.files= []               # should be updated with pointers to files not sent
    self.update_files()

  def update_files(self):
    print "updating"
    global files_available
    self.files= []
    current = files_available.file
    while current != 0:
      #print "loop12"
      self.files.append(current)
      current = current.next

