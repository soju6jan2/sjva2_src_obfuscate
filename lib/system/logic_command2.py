import os
C=object
p=True
W=False
M=None
x=Exception
v=str
k=classmethod
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
class SystemLogicCommand2(C):
 instance_list=[]
 def __init__(self,title,commands,clear=p,wait=W,show_modal=p):
  self.title=title
  self.commands=commands
  self.clear=clear
  self.wait=wait
  self.show_modal=show_modal
  self.process=M
  self.stdout_queue=M
  self.thread=M
  self.send_to_ui_thread=M
  self.return_log=[]
  SystemLogicCommand2.instance_list.append(self)
 def start(self):
  try:
   if self.show_modal:
    if self.clear:
     socketio.emit("command_modal_clear",M,namespace='/framework',broadcast=p)
   self.thread=threading.Thread(target=self.execute_thread_function,args=())
   self.thread.setDaemon(p)
   self.thread.start()
   if self.wait:
    time.sleep(1)
    self.thread.join()
    return self.return_log
  except x as exception:
   logger.error('Exception:%s',exception)
   logger.error(traceback.format_exc())
 def execute_thread_function(self):
  try:
   if self.show_modal:
    socketio.emit("loading_hide",M,namespace='/framework',broadcast=p)
   for command in self.commands:
    if command[0]=='msg':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'%s\n\n'%command[1],namespace='/framework',broadcast=p)
    elif command[0]=='system':
     if self.show_modal:
      socketio.emit("command_modal_add_text",'$ %s\n\n'%command[1],namespace='/framework',broadcast=p)
     os.system(command[1])
    else:
     show_command=p
     if command[0]=='hide':
      show_command=W
      command=command[1:]
     self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=p,bufsize=1)
     self.start_communicate(command,show_command=show_command)
     self.send_queue_start()
     if self.process is not M:
      self.process.wait()
    time.sleep(1)
  except x as exception:
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=p)
    socketio.emit("command_modal_add_text",v(exception),namespace='/framework',broadcast=p)
    socketio.emit("command_modal_add_text",v(traceback.format_exc()),namespace='/framework',broadcast=p)
 def start_communicate(self,current_command,show_command=p):
  self.stdout_queue=py_queue.Queue()
  if show_command:
   self.stdout_queue.put('$ %s\n'%' '.join(current_command))
  sout=io.open(self.process.stdout.fileno(),'rb',closefd=W)
  def Pump(stream):
   queue=py_queue.Queue()
   def rdr():
    while p:
     buf=self.process.stdout.read(1)
     if buf:
      queue.put(buf)
     else:
      queue.put(M)
      break
    queue.put(M)
    time.sleep(1)
   def clct():
    active=p
    while active:
     r=queue.get()
     if r is M:
      break
     try:
      while p:
       r1=queue.get(timeout=0.005)
       if r1 is M:
        active=W
        break
       else:
        r+=r1
     except:
      pass
     if r is not M:
      try:
       r=r.decode('utf-8')
      except x as exception:
       try:
        r=r.decode('cp949')
       except x as exception:
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
    th.setDaemon(p)
    th.start()
  Pump(sout)
 def send_queue_start(self):
  def send_to_ui_thread_function():
   if self.show_modal:
    socketio.emit("command_modal_show",self.title,namespace='/framework',broadcast=p)
   while self.stdout_queue:
    line=self.stdout_queue.get()
    if line=='<END>':
     if self.show_modal:
      socketio.emit("command_modal_add_text","\n",namespace='/framework',broadcast=p)
      break
    else:
     if self.show_modal:
      socketio.emit("command_modal_add_text",line,namespace='/framework',broadcast=p)
   self.send_to_ui_thread=M
   self.stdout_queue=M
   self.process=M
  if self.send_to_ui_thread is M:
   self.send_to_ui_thread=threading.Thread(target=send_to_ui_thread_function,args=())
   self.send_to_ui_thread.start()
 @k
 def plugin_unload(cls):
  for instance in cls.instance_list:
   try:
    if instance.process is not M and instance.process.poll()is M:
     import psutil
     process=psutil.Process(instance.process.pid)
     for proc in instance.process.children(recursive=p):
      proc.kill()
     instance.process.kill()
   except x as exception:
    logger.error('Exception:%s',exception)
    logger.error(traceback.format_exc()) 
   finally:
    try:instance.process.kill()
    except:pass
# Created by pyminifier (https://github.com/liftoff/pyminifier)
