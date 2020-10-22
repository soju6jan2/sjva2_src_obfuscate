import os
r=object
s=True
a=False
y=None
G=Exception
I=str
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
class SystemLogicCommand2(r):
 instance_list=[]
 def __init__(self,title,commands,clear=s,wait=a,show_modal=s):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=y
  self.stdout_queue=y
  self.thread=y
  self.send_to_ui_thread=y
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",y,namespace='/framework',broadcast=s)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(s)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except G as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",y,namespace='/framework',broadcast=s)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=s)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=s)
     os.system(command[1])
    else:
     show_command=s
     if command[0]=='hide':
      show_command=a
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=s,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not y:
      self.process.wait()
    time.sleep(1)
  except G as e:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=s)
    socketio.emit("command_modal_add_text",I(e),namespace='/framework',broadcast=s)
    socketio.emit("command_modal_add_text",I(traceback.format_exc()),namespace='/framework',broadcast=s)
 def start_communicate(self,current_command,show_command=s):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=a)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while s:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(y)
      break
    queue.put(y)
    time.sleep(1)
   def clct():
    active=s
    while active:
     r=queue.get()
     if r is y:
      break
     try:
      while s:
       r1=queue.get(timeout=0.005)
       if r1 is y:
        active=a
        break
       else:
        r+=r1
     except:
      pass
     if r is not y:
      try:
       r=r.decode('utf-8')
      except G as e:
       try:
        r=r.decode('cp949')
       except G as e:
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
    th.setDaemon(s)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=s)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=s)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=s)
   self.send_to_ui_thread=y
   self.stdout_queue=y
   self.process=y
  if self.send_to_ui_thread is y:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @d
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not y and instance.process.poll()is y:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=s):
      proc.kill()
     instance.process.kill()
   except G as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
