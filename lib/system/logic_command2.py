import os
h=object
A=True
i=False
f=None
W=Exception
z=str
E=classmethod
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
class SystemLogicCommand2(h):
 instance_list=[]
 def __init__(self,title,commands,clear=A,wait=i,show_modal=A):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=f
  self.stdout_queue=f
  self.thread=f
  self.send_to_ui_thread=f
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",f,namespace='/framework',broadcast=A)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(A)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except W as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",f,namespace='/framework',broadcast=A)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=A)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=A)
     os.system(command[1])
    else:
     show_command=A
     if command[0]=='hide':
      show_command=i
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=A,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not f:
      self.process.wait()
    time.sleep(1)
  except W as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=A)
    socketio.emit("command_modal_add_text",z(exception),namespace='/framework',broadcast=A)
    socketio.emit("command_modal_add_text",z(traceback.format_exc()),namespace='/framework',broadcast=A)
 def start_communicate(self,current_command,show_command=A):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=i)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while A:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(f)
      break
    queue.put(f)
    time.sleep(1)
   def clct():
    active=A
    while active:
     r=queue.get()
     if r is f:
      break
     try:
      while A:
       r1=queue.get(timeout=0.005)
       if r1 is f:
        active=i
        break
       else:
        r+=r1
     except:
      pass
     if r is not f:
      try:
       r=r.decode('utf-8')
      except W as exception:
       try:
        r=r.decode('cp949')
       except W as exception:
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
    th.setDaemon(A)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=A)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=A)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=A)
   self.send_to_ui_thread=f
   self.stdout_queue=f
   self.process=f
  if self.send_to_ui_thread is f:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @E
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not f and instance.process.poll()is f:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=A):
      proc.kill()
     instance.process.kill()
   except W as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
