import os
w=object
Q=True
a=False
m=None
A=Exception
v=str
I=classmethod
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
class SystemLogicCommand2(w):
 instance_list=[]
 def __init__(self,title,commands,clear=Q,wait=a,show_modal=Q):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=m
  self.stdout_queue=m
  self.thread=m
  self.send_to_ui_thread=m
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",m,namespace='/framework',broadcast=Q)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(Q)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except A as e:
   logger.error('Exception:%s',e)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",m,namespace='/framework',broadcast=Q)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=Q)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=Q)
     os.system(command[1])
    else:
     show_command=Q
     if command[0]=='hide':
      show_command=a
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=Q,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not m:
      self.process.wait()
    time.sleep(1)
  except A as e:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=Q)
    socketio.emit("command_modal_add_text",v(e),namespace='/framework',broadcast=Q)
    socketio.emit("command_modal_add_text",v(traceback.format_exc()),namespace='/framework',broadcast=Q)
 def start_communicate(self,current_command,show_command=Q):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=a)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while Q:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(m)
      break
    queue.put(m)
    time.sleep(1)
   def clct():
    active=Q
    while active:
     r=queue.get()
     if r is m:
      break
     try:
      while Q:
       r1=queue.get(timeout=0.005)
       if r1 is m:
        active=a
        break
       else:
        r+=r1
     except:
      pass
     if r is not m:
      try:
       r=r.decode('utf-8')
      except A as e:
       try:
        r=r.decode('cp949')
       except A as e:
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
    th.setDaemon(Q)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=Q)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=Q)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=Q)
   self.send_to_ui_thread=m
   self.stdout_queue=m
   self.process=m
  if self.send_to_ui_thread is m:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @I
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not m and instance.process.poll()is m:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=Q):
      proc.kill()
     instance.process.kill()
   except A as e:
    logger.error('Exception:%s',e)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
