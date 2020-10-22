import os
v=object
i=True
b=False
D=None
V=Exception
K=str
d=classmethod
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
class SystemLogicCommand2(v):
 instance_list=[]
 def __init__(self,title,commands,clear=i,wait=b,show_modal=i):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=D
  self.stdout_queue=D
  self.thread=D
  self.send_to_ui_thread=D
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",D,namespace='/framework',broadcast=i)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(i)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except V as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",D,namespace='/framework',broadcast=i)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=i)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=i)
     os.system(command[1])
    else:
     show_command=i
     if command[0]=='hide':
      show_command=b
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=i,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not D:
      self.process.wait()
    time.sleep(1)
  except V as e:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=i)
    socketio.emit("command_modal_add_text",K(e),namespace='/framework',broadcast=i)
    socketio.emit("command_modal_add_text",K(traceback.format_exc()),namespace='/framework',broadcast=i)
 def start_communicate(self,current_command,show_command=i):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=b)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while i:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(D)
      break
    queue.put(D)
    time.sleep(1)
   def clct():
    active=i
    while active:
     r=queue.get()
     if r is D:
      break
     try:
      while i:
       r1=queue.get(timeout=0.005)
       if r1 is D:
        active=b
        break
       else:
        r+=r1
     except:
      pass
     if r is not D:
      try:
       r=r.decode('utf-8')
      except V as e:
       try:
        r=r.decode('cp949')
       except V as e:
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
    th.setDaemon(i)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=i)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=i)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=i)
   self.send_to_ui_thread=D
   self.stdout_queue=D
   self.process=D
  if self.send_to_ui_thread is D:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @d
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not D and instance.process.poll()is D:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=i):
      proc.kill()
     instance.process.kill()
   except V as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
