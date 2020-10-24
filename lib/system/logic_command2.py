import os
m=object
z=True
r=False
j=None
e=Exception
g=str
p=classmethod
import traceback
import logging
import platform
import subprocess
import threading
import sys
import io
import time
import json
from framework.logger import get_logger
from framework import path_app_root,socketio,logger,py_queue
package_name=__name__.split('.')[0]
class SystemLogicCommand2(m):
 instance_list=[]
 def __init__(self,title,commands,clear=z,wait=r,show_modal=z):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=j
  self.stdout_queue=j
  self.thread=j
  self.send_to_ui_thread=j
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",j,namespace='/framework',broadcast=z)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(z)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except e as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",j,namespace='/framework',broadcast=z)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=z)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=z)
     os.system(command[1])
    else:
     show_command=z
     if command[0]=='hide':
      show_command=r
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=z,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not j:
      self.process.wait()
    time.sleep(1)
  except e as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=z)
    socketio.emit("command_modal_add_text",g(exception),namespace='/framework',broadcast=z)
    socketio.emit("command_modal_add_text",g(traceback.format_exc()),namespace='/framework',broadcast=z)
 def start_communicate(self,current_command,show_command=z):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=r)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while z:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(j)
      break
    queue.put(j)
    time.sleep(1)
   def clct():
    active=z
    while active:
     r=queue.get()
     if r is j:
      break
     try:
      while z:
       r1=queue.get(timeout=0.005)
       if r1 is j:
        active=r
        break
       else:
        r+=r1
     except:
      pass
     if r is not j:
      try:
       r=r.decode('utf-8')
      except e as exception:
       try:
        r=r.decode('cp949')
       except e as exception:
        logger.error('Exception:%s',exception)
        logger.error(traceback.format_exc())
        try:
         r=r.decode('euc-kr')
        except:
         pass
      self.stdout_queue.put(r)
      self.return_log+=r.split('\n')
    self.stdout_queue.put('<END>')
   for tgt in[rdr,clct]:
    th=threading.Thread(target=tgt)
    th.setDaemon(z)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=z)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=z)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=z)
   self.send_to_ui_thread=j
   self.stdout_queue=j
   self.process=j
  if self.send_to_ui_thread is j:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @p
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not j and instance.process.poll()is j:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=z):
      proc.kill()
     instance.process.kill()
   except e as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
