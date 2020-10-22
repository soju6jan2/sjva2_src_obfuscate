import os
f=object
k=True
C=False
W=None
V=Exception
A=str
O=classmethod
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
class SystemLogicCommand2(f):
 instance_list=[]
 def __init__(self,title,commands,clear=k,wait=C,show_modal=k):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=W
  self.stdout_queue=W
  self.thread=W
  self.send_to_ui_thread=W
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",W,namespace='/framework',broadcast=k)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(k)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except V as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",W,namespace='/framework',broadcast=k)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=k)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=k)
     os.system(command[1])
    else:
     show_command=k
     if command[0]=='hide':
      show_command=C
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=k,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not W:
      self.process.wait()
    time.sleep(1)
  except V as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=k)
    socketio.emit("command_modal_add_text",A(exception),namespace='/framework',broadcast=k)
    socketio.emit("command_modal_add_text",A(traceback.format_exc()),namespace='/framework',broadcast=k)
 def start_communicate(self,current_command,show_command=k):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=C)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while k:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(W)
      break
    queue.put(W)
    time.sleep(1)
   def clct():
    active=k
    while active:
     r=queue.get()
     if r is W:
      break
     try:
      while k:
       r1=queue.get(timeout=0.005)
       if r1 is W:
        active=C
        break
       else:
        r+=r1
     except:
      pass
     if r is not W:
      try:
       r=r.decode('utf-8')
      except V as exception:
       try:
        r=r.decode('cp949')
       except V as exception:
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
    th.setDaemon(k)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=k)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=k)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=k)
   self.send_to_ui_thread=W
   self.stdout_queue=W
   self.process=W
  if self.send_to_ui_thread is W:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @O
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not W and instance.process.poll()is W:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=k):
      proc.kill()
     instance.process.kill()
   except V as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
