import os
s=object
B=True
W=False
O=None
t=Exception
u=str
H=classmethod
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
 def __init__(self,title,commands,clear=B,wait=W,show_modal=B):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=O
  self.stdout_queue=O
  self.thread=O
  self.send_to_ui_thread=O
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",O,namespace='/framework',broadcast=B)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(B)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except t as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",O,namespace='/framework',broadcast=B)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=B)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=B)
     os.system(command[1])
    else:
     show_command=B
     if command[0]=='hide':
      show_command=W
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=B,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not O:
      self.process.wait()
    time.sleep(1)
  except t as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=B)
    socketio.emit("command_modal_add_text",u(exception),namespace='/framework',broadcast=B)
    socketio.emit("command_modal_add_text",u(traceback.format_exc()),namespace='/framework',broadcast=B)
 def start_communicate(self,current_command,show_command=B):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=W)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while B:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(O)
      break
    queue.put(O)
    time.sleep(1)
   def clct():
    active=B
    while active:
     r=queue.get()
     if r is O:
      break
     try:
      while B:
       r1=queue.get(timeout=0.005)
       if r1 is O:
        active=W
        break
       else:
        r+=r1
     except:
      pass
     if r is not O:
      try:
       r=r.decode('utf-8')
      except t as exception:
       try:
        r=r.decode('cp949')
       except t as exception:
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
    th.setDaemon(B)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=B)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=B)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=B)
   self.send_to_ui_thread=O
   self.stdout_queue=O
   self.process=O
  if self.send_to_ui_thread is O:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @H
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not O and instance.process.poll()is O:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=B):
      proc.kill()
     instance.process.kill()
   except t as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
