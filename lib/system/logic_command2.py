import os
c=object
F=True
l=False
C=None
H=Exception
M=str
T=classmethod
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
class SystemLogicCommand2(c):
 instance_list=[]
 def __init__(self,title,commands,clear=F,wait=l,show_modal=F):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=C
  self.stdout_queue=C
  self.thread=C
  self.send_to_ui_thread=C
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",C,namespace='/framework',broadcast=F)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(F)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except H as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",C,namespace='/framework',broadcast=F)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=F)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=F)
     os.system(command[1])
    else:
     show_command=F
     if command[0]=='hide':
      show_command=l
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=F,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not C:
      self.process.wait()
    time.sleep(1)
  except H as e:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=F)
    socketio.emit("command_modal_add_text",M(e),namespace='/framework',broadcast=F)
    socketio.emit("command_modal_add_text",M(traceback.format_exc()),namespace='/framework',broadcast=F)
 def start_communicate(self,current_command,show_command=F):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=l)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while F:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(C)
      break
    queue.put(C)
    time.sleep(1)
   def clct():
    active=F
    while active:
     r=queue.get()
     if r is C:
      break
     try:
      while F:
       r1=queue.get(timeout=0.005)
       if r1 is C:
        active=l
        break
       else:
        r+=r1
     except:
      pass
     if r is not C:
      try:
       r=r.decode('utf-8')
      except H as e:
       try:
        r=r.decode('cp949')
       except H as e:
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
    th.setDaemon(F)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=F)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=F)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=F)
   self.send_to_ui_thread=C
   self.stdout_queue=C
   self.process=C
  if self.send_to_ui_thread is C:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @T
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not C and instance.process.poll()is C:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=F):
      proc.kill()
     instance.process.kill()
   except H as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
