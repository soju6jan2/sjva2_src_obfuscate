import os
z=object
f=True
b=False
m=None
I=Exception
P=str
q=classmethod
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
class SystemLogicCommand2(z):
 instance_list=[]
 def __init__(self,title,commands,clear=f,wait=b,show_modal=f):
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
     socketio.emit("command_modal_clear",m,namespace='/framework',broadcast=f)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(f)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except I as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",m,namespace='/framework',broadcast=f)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=f)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=f)
     os.system(command[1])
    else:
     show_command=f
     if command[0]=='hide':
      show_command=b
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=f,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not m:
      self.process.wait()
    time.sleep(1)
  except I as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=f)
    socketio.emit("command_modal_add_text",P(exception),namespace='/framework',broadcast=f)
    socketio.emit("command_modal_add_text",P(traceback.format_exc()),namespace='/framework',broadcast=f)
 def start_communicate(self,current_command,show_command=f):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=b)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while f:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(m)
      break
    queue.put(m)
    time.sleep(1)
   def clct():
    active=f
    while active:
     r=queue.get()
     if r is m:
      break
     try:
      while f:
       r1=queue.get(timeout=0.005)
       if r1 is m:
        active=b
        break
       else:
        r+=r1
     except:
      pass
     if r is not m:
      try:
       r=r.decode('utf-8')
      except I as exception:
       try:
        r=r.decode('cp949')
       except I as exception:
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
    th.setDaemon(f)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=f)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=f)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=f)
   self.send_to_ui_thread=m
   self.stdout_queue=m
   self.process=m
  if self.send_to_ui_thread is m:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @q
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not m and instance.process.poll()is m:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=f):
      proc.kill()
     instance.process.kill()
   except I as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
