import os
s=object
h=True
x=False
z=None
Q=Exception
G=str
A=classmethod
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
class SystemLogicCommand2(s):
 instance_list=[]
 def __init__(self,title,commands,clear=h,wait=x,show_modal=h):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=z
  self.stdout_queue=z
  self.thread=z
  self.send_to_ui_thread=z
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",z,namespace='/framework',broadcast=h)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(h)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except Q as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",z,namespace='/framework',broadcast=h)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=h)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=h)
     os.system(command[1])
    else:
     show_command=h
     if command[0]=='hide':
      show_command=x
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=h,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not z:
      self.process.wait()
    time.sleep(1)
  except Q as e:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=h)
    socketio.emit("command_modal_add_text",G(e),namespace='/framework',broadcast=h)
    socketio.emit("command_modal_add_text",G(traceback.format_exc()),namespace='/framework',broadcast=h)
 def start_communicate(self,current_command,show_command=h):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=x)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while h:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(z)
      break
    queue.put(z)
    time.sleep(1)
   def clct():
    active=h
    while active:
     r=queue.get()
     if r is z:
      break
     try:
      while h:
       r1=queue.get(timeout=0.005)
       if r1 is z:
        active=x
        break
       else:
        r+=r1
     except:
      pass
     if r is not z:
      try:
       r=r.decode('utf-8')
      except Q as e:
       try:
        r=r.decode('cp949')
       except Q as e:
        logger.error('Exception:%s',e)
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
    th.setDaemon(h)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=h)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=h)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=h)
   self.send_to_ui_thread=z
   self.stdout_queue=z
   self.process=z
  if self.send_to_ui_thread is z:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @A
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not z and instance.process.poll()is z:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=h):
      proc.kill()
     instance.process.kill()
   except Q as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
