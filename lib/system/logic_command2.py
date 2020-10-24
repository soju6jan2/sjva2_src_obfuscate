import os
P=object
W=True
U=False
s=None
J=Exception
Y=str
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
class SystemLogicCommand2(P):
 instance_list=[]
 def __init__(self,title,commands,clear=W,wait=U,show_modal=W):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=s
  self.stdout_queue=s
  self.thread=s
  self.send_to_ui_thread=s
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",s,namespace='/framework',broadcast=W)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(W)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except J as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",s,namespace='/framework',broadcast=W)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=W)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=W)
     os.system(command[1])
    else:
     show_command=W
     if command[0]=='hide':
      show_command=U
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=W,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not s:
      self.process.wait()
    time.sleep(1)
  except J as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=W)
    socketio.emit("command_modal_add_text",Y(exception),namespace='/framework',broadcast=W)
    socketio.emit("command_modal_add_text",Y(traceback.format_exc()),namespace='/framework',broadcast=W)
 def start_communicate(self,current_command,show_command=W):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=U)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while W:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(s)
      break
    queue.put(s)
    time.sleep(1)
   def clct():
    active=W
    while active:
     r=queue.get()
     if r is s:
      break
     try:
      while W:
       r1=queue.get(timeout=0.005)
       if r1 is s:
        active=U
        break
       else:
        r+=r1
     except:
      pass
     if r is not s:
      try:
       r=r.decode('utf-8')
      except J as exception:
       try:
        r=r.decode('cp949')
       except J as exception:
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
    th.setDaemon(W)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=W)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=W)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=W)
   self.send_to_ui_thread=s
   self.stdout_queue=s
   self.process=s
  if self.send_to_ui_thread is s:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @p
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not s and instance.process.poll()is s:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=W):
      proc.kill()
     instance.process.kill()
   except J as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
